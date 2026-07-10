#!/usr/bin/env python3
"""
Profiler / escaneador de dados — Etapa (b) Exploração dos dados.

Lê um ou mais arquivos (.parquet ou .csv), descobre o schema, classifica o
tipo lógico de cada coluna e calcula métricas de qualidade adequadas a cada
tipo. Gera, para cada base:
  - um relatório Markdown em  profiles/<nome>_perfil.md
  - um JSON estruturado em     profiles/<nome>_perfil.json
e imprime um resumo no terminal.

Usa DuckDB para calcular tudo via SQL direto sobre o arquivo (sem carregar a
base inteira na memória), então funciona bem até na base de fraude (24M linhas).

Uso:
  python3 explorar_dados.py                      # escaneia datasets/**/*.parquet
  python3 explorar_dados.py caminho/arquivo.parquet [outro.csv ...]
"""
import os
import sys
import json
import glob
import datetime
import duckdb

PROJECT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(PROJECT, "profiles")

# ---------------------------------------------------------------------------
# Classificação de tipos
# ---------------------------------------------------------------------------
def classify(duckdb_type: str) -> str:
    """Mapeia o tipo físico do DuckDB para um 'tipo lógico' da nossa análise."""
    t = duckdb_type.upper()
    if t.startswith("BOOL"):
        return "boolean"
    if t.startswith(("TIMESTAMP", "DATE", "TIME", "INTERVAL")):
        return "temporal"
    if t.startswith(("TINYINT", "SMALLINT", "INTEGER", "BIGINT", "HUGEINT",
                     "UTINYINT", "USMALLINT", "UINTEGER", "UBIGINT", "UHUGEINT")):
        return "inteiro"
    if t.startswith(("FLOAT", "DOUBLE", "REAL", "DECIMAL", "NUMERIC")):
        return "decimal"
    if t.startswith(("VARCHAR", "CHAR", "TEXT", "STRING")):
        return "texto"
    return "outro"


NUMERIC = ("inteiro", "decimal")
# regex (RE2) p/ detectar texto com "cara de número": opcional $, sinal, dígitos, decimal
NUMERIC_LOOKING = r"\$?\s*-?[0-9]+([.,][0-9]+)?"

# Limiares de cardinalidade (ajustáveis). Baseados no nº ABSOLUTO de valores distintos,
# que é o que importa para o custo de encoding em ML.
CARD_BAIXA_MAX = 10   # baixa:  2..10   -> ideal para one-hot encoding
CARD_MEDIA_MAX = 50   # média:  11..50  -> ordinal / target encoding
#                       alta:   > 50    -> encoding especial (frequency/target/hashing)


def nivel_cardinalidade(n_distinct, non_null):
    """Classifica a cardinalidade da coluna em faixas."""
    if n_distinct <= 1:
        return "constante"
    if non_null and n_distinct == non_null:
        return "unica"          # todos os valores diferentes (ID / texto livre)
    if n_distinct <= CARD_BAIXA_MAX:
        return "baixa"
    if n_distinct <= CARD_MEDIA_MAX:
        return "media"
    return "alta"


def eh_categorica(lt, nivel):
    """Decide se a coluna é candidata a categórica, dado tipo lógico e cardinalidade."""
    if nivel in ("constante", "unica"):
        return False
    if lt in ("texto", "boolean"):
        return True                     # texto/booleano são categóricos por natureza
    if lt == "inteiro":
        return nivel in ("baixa", "media")   # códigos inteiros de baixa/média cardinalidade
    if lt == "decimal":
        return nivel == "baixa"         # decimal só é categórico se tiver pouquíssimos valores
    return False


def q(name: str) -> str:
    """Escapa um identificador de coluna para o SQL."""
    return '"' + name.replace('"', '""') + '"'


def relation(path: str) -> str:
    esc = path.replace("'", "''")
    if path.lower().endswith(".csv"):
        return f"read_csv_auto('{esc}', sample_size=-1)"
    return f"read_parquet('{esc}')"


# ---------------------------------------------------------------------------
# Perfil de uma coluna
# ---------------------------------------------------------------------------
def profile_column(con, rel, name, dtype, total):
    lt = classify(dtype)
    col = q(name)
    d = {"coluna": name, "tipo_fisico": dtype, "tipo_logico": lt}

    # ---- métricas universais ----
    non_null, n_missing, n_distinct = con.execute(
        f"SELECT count({col}), count(*) - count({col}), count(DISTINCT {col}) FROM {rel}"
    ).fetchone()
    d["n_total"] = total
    d["n_preenchidos"] = non_null
    d["n_ausentes"] = n_missing
    d["pct_ausentes"] = round(100 * n_missing / total, 4) if total else None
    d["n_distintos"] = n_distinct
    d["pct_distintos"] = round(100 * n_distinct / non_null, 4) if non_null else None
    nivel = nivel_cardinalidade(n_distinct, non_null)
    d["nivel_cardinalidade"] = nivel
    d["candidata_categorica"] = eh_categorica(lt, nivel)

    # moda (valor mais frequente)
    moda = con.execute(
        f"SELECT {col} AS v, count(*) AS c FROM {rel} WHERE {col} IS NOT NULL "
        f"GROUP BY 1 ORDER BY c DESC, 1 LIMIT 1"
    ).fetchone()
    if moda:
        d["moda"] = str(moda[0])
        d["moda_freq"] = moda[1]
        d["moda_pct"] = round(100 * moda[1] / non_null, 4) if non_null else None

    # top categorias (se cardinalidade baixa)
    if 1 <= n_distinct <= 25:
        tops = con.execute(
            f"SELECT {col} AS v, count(*) AS c FROM {rel} WHERE {col} IS NOT NULL "
            f"GROUP BY 1 ORDER BY c DESC, 1"
        ).fetchall()
        d["categorias"] = [
            {"valor": str(v), "n": c, "pct": round(100 * c / non_null, 2)}
            for v, c in tops
        ]

    # ---- métricas por tipo ----
    if lt in NUMERIC:
        (mn, mx, media, desvio, quantis, assimetria, curtose,
         n_zeros, n_neg) = con.execute(
            f"""SELECT min({col}), max({col}), avg({col}), stddev_samp({col}),
                       quantile_cont({col}, [0.01,0.05,0.25,0.5,0.75,0.95,0.99]),
                       skewness({col}), kurtosis({col}),
                       sum(CASE WHEN {col} = 0 THEN 1 ELSE 0 END),
                       sum(CASE WHEN {col} < 0 THEN 1 ELSE 0 END)
                FROM {rel}"""
        ).fetchone()
        mn = _num(mn); mx = _num(mx)
        d["min"] = mn
        d["max"] = mx
        d["amplitude"] = (mx - mn) if (mn is not None and mx is not None) else None
        d["media"] = _num(media)
        d["desvio_padrao"] = _num(desvio)
        d["coef_variacao"] = (
            round(desvio / media, 4) if (desvio is not None and media not in (None, 0)) else None
        )
        if quantis:
            p = [_num(x) for x in quantis]
            d["percentis"] = dict(zip(["p1", "p5", "p25", "p50", "p75", "p95", "p99"], p))
            d["mediana"] = p[3]
            iqr = p[4] - p[2] if (p[4] is not None and p[2] is not None) else None
            d["iqr"] = iqr
            if iqr is not None:
                lo, hi = p[2] - 1.5 * iqr, p[4] + 1.5 * iqr
                n_out = con.execute(
                    f"SELECT sum(CASE WHEN {col} < {lo} OR {col} > {hi} THEN 1 ELSE 0 END) FROM {rel}"
                ).fetchone()[0] or 0
                d["outliers_iqr"] = int(n_out)
                d["pct_outliers"] = round(100 * n_out / non_null, 4) if non_null else None
                d["limites_outlier"] = {"inferior": round(lo, 4), "superior": round(hi, 4)}
        d["assimetria"] = _num(assimetria)
        d["curtose"] = _num(curtose)
        d["n_zeros"] = int(n_zeros or 0)
        d["pct_zeros"] = round(100 * (n_zeros or 0) / non_null, 4) if non_null else None
        d["n_negativos"] = int(n_neg or 0)

    elif lt == "texto":
        mn, mx, media, desvio, n_vazias, n_numlike = con.execute(
            f"""SELECT min(length({col})), max(length({col})),
                       avg(length({col})), stddev_samp(length({col})),
                       sum(CASE WHEN length(trim({col})) = 0 THEN 1 ELSE 0 END),
                       sum(CASE WHEN regexp_full_match(trim({col}), '{NUMERIC_LOOKING}') THEN 1 ELSE 0 END)
                FROM {rel} WHERE {col} IS NOT NULL"""
        ).fetchone()
        d["comprimento"] = {
            "min": _num(mn), "max": _num(mx),
            "media": _num(media), "desvio_padrao": _num(desvio),
        }
        d["n_vazias"] = int(n_vazias or 0)
        d["pct_vazias"] = round(100 * (n_vazias or 0) / non_null, 4) if non_null else None
        d["n_aparencia_numerica"] = int(n_numlike or 0)
        d["pct_aparencia_numerica"] = round(100 * (n_numlike or 0) / non_null, 4) if non_null else None

    elif lt == "boolean":
        n_true, n_false = con.execute(
            f"""SELECT sum(CASE WHEN {col} THEN 1 ELSE 0 END),
                       sum(CASE WHEN NOT {col} THEN 1 ELSE 0 END)
                FROM {rel} WHERE {col} IS NOT NULL"""
        ).fetchone()
        n_true, n_false = int(n_true or 0), int(n_false or 0)
        d["n_true"] = n_true
        d["n_false"] = n_false
        d["pct_true"] = round(100 * n_true / non_null, 4) if non_null else None
        d["pct_false"] = round(100 * n_false / non_null, 4) if non_null else None
        maior, menor = max(n_true, n_false), min(n_true, n_false)
        d["razao_desbalanceamento"] = round(maior / menor, 2) if menor else None

    elif lt == "temporal":
        mn, mx = con.execute(f"SELECT min({col}), max({col}) FROM {rel}").fetchone()
        d["min"] = str(mn)
        d["max"] = str(mx)

    # ajuste: texto com "cara de número" é número mal tipado, não categórico
    texto_numerico = (lt == "texto" and (d.get("pct_aparencia_numerica") or 0) >= 90)
    if texto_numerico:
        d["candidata_categorica"] = False

    # ---- flags automáticas ----
    flags = []
    if nivel == "constante":
        flags.append("constante")
    if nivel == "unica":
        flags.append("possivel_id")
    if d.get("pct_ausentes", 0) and d["pct_ausentes"] >= 50:
        flags.append("muitos_ausentes")
    if d["candidata_categorica"]:
        flags.append(f"categorica_card_{nivel}")
    if texto_numerico:
        flags.append("texto_numerico")
    d["flags"] = flags
    return d


def _num(x):
    """Converte Decimal/None de forma segura para float/None."""
    if x is None:
        return None
    try:
        f = float(x)
        return f if f == f else None  # descarta NaN
    except (TypeError, ValueError):
        return x


# ---------------------------------------------------------------------------
# Perfil de uma base inteira
# ---------------------------------------------------------------------------
def profile_dataset(path):
    con = duckdb.connect()
    rel = relation(path)
    total = con.execute(f"SELECT count(*) FROM {rel}").fetchone()[0]
    schema = con.execute(f"DESCRIBE SELECT * FROM {rel}").fetchall()
    cols = []
    for row in schema:
        name, dtype = row[0], row[1]
        try:
            cols.append(profile_column(con, rel, name, dtype, total))
        except Exception as e:  # noqa: BLE001 - não deixa uma coluna quebrar tudo
            cols.append({"coluna": name, "tipo_fisico": dtype,
                         "tipo_logico": classify(dtype), "erro": str(e), "flags": ["erro"]})
    con.close()
    return {"arquivo": path, "n_linhas": total, "n_colunas": len(cols), "colunas": cols}


# ---------------------------------------------------------------------------
# Formatação / saída
# ---------------------------------------------------------------------------
def fmt(x):
    if x is None:
        return "—"
    if isinstance(x, bool):
        return "Sim" if x else "Não"
    if isinstance(x, int):
        return f"{x:,}".replace(",", ".")
    if isinstance(x, float):
        if x != x:
            return "—"
        s = f"{x:,.2f}" if (abs(x) >= 1000 or x == int(x)) else f"{x:,.4f}"
        return s.replace(",", "X").replace(".", ",").replace("X", ".")  # pt-BR
    return str(x)


def to_markdown(profile):
    name = os.path.basename(profile["arquivo"])
    gerado = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    L = [f"# Perfil de Dados — `{name}`", ""]
    L.append(f"- **Arquivo:** `{profile['arquivo']}`")
    L.append(f"- **Linhas:** {fmt(profile['n_linhas'])} • **Colunas:** {profile['n_colunas']}")
    L.append(f"- **Gerado em:** {gerado} (por `explorar_dados.py`)")
    L.append("")

    # tabela resumo
    L.append("## Resumo geral")
    L.append("")
    L.append("| Coluna | Tipo lógico | % ausentes | Nº distintos | Cardinalidade | Categórica? | Moda | Flags |")
    L.append("|--------|-------------|-----------:|-------------:|---------------|:-----------:|------|-------|")
    for c in profile["colunas"]:
        cat = "✅" if c.get("candidata_categorica") else "—"
        L.append(
            f"| `{c['coluna']}` | {c.get('tipo_logico','')} "
            f"| {fmt(c.get('pct_ausentes'))}% | {fmt(c.get('n_distintos'))} "
            f"| {c.get('nivel_cardinalidade','')} | {cat} "
            f"| {c.get('moda','—')} | {', '.join(c.get('flags', [])) or '—'} |"
        )
    L.append("")

    # agrupamento por cardinalidade (candidatas a categórica)
    L.append("## Candidatas a categórica por cardinalidade")
    L.append("")
    grupos = {
        "baixa": (f"Baixa cardinalidade (2–{CARD_BAIXA_MAX} distintos) — ideal para **one-hot encoding**", []),
        "media": (f"Média cardinalidade ({CARD_BAIXA_MAX + 1}–{CARD_MEDIA_MAX} distintos) — considerar **ordinal/target encoding**", []),
        "alta": (f"Alta cardinalidade (>{CARD_MEDIA_MAX} distintos) — **encoding especial** (frequency/target/hashing)", []),
    }
    for c in profile["colunas"]:
        if c.get("candidata_categorica") and c.get("nivel_cardinalidade") in grupos:
            grupos[c["nivel_cardinalidade"]][1].append(c)
    for nivel in ("baixa", "media", "alta"):
        titulo, itens = grupos[nivel]
        L.append(f"### {titulo}")
        if itens:
            for c in itens:
                L.append(f"- `{c['coluna']}` — {fmt(c['n_distintos'])} distintos _({c.get('tipo_logico')})_")
        else:
            L.append("- _(nenhuma)_")
        L.append("")
    outras = [c for c in profile["colunas"] if c.get("nivel_cardinalidade") in ("unica", "constante")]
    if outras:
        L.append("### Fora do escopo categórico (ID única / constante)")
        for c in outras:
            L.append(f"- `{c['coluna']}` — {c.get('nivel_cardinalidade')} ({fmt(c['n_distintos'])} distintos)")
        L.append("")

    # detalhes por coluna
    L.append("## Detalhamento por coluna")
    for c in profile["colunas"]:
        L.append("")
        L.append(f"### `{c['coluna']}`  —  _{c.get('tipo_logico','')}_")
        if c.get("erro"):
            L.append(f"- ⚠️ erro ao processar: {c['erro']}")
            continue
        L.append(f"- Preenchidos: {fmt(c['n_preenchidos'])} / {fmt(c['n_total'])} "
                 f"(ausentes: {fmt(c['n_ausentes'])} = {fmt(c['pct_ausentes'])}%)")
        L.append(f"- Distintos: {fmt(c['n_distintos'])} ({fmt(c.get('pct_distintos'))}% dos preenchidos)")
        if "moda" in c:
            L.append(f"- Moda: `{c['moda']}` ({fmt(c['moda_freq'])}× = {fmt(c.get('moda_pct'))}%)")

        lt = c.get("tipo_logico")
        if lt in NUMERIC:
            L.append(f"- Min / Máx: {fmt(c.get('min'))} / {fmt(c.get('max'))} "
                     f"(amplitude {fmt(c.get('amplitude'))})")
            L.append(f"- Média: {fmt(c.get('media'))} • Desvio-padrão: {fmt(c.get('desvio_padrao'))} "
                     f"• Coef. variação: {fmt(c.get('coef_variacao'))}")
            p = c.get("percentis", {})
            if p:
                L.append("- Percentis: " + " | ".join(f"{k}={fmt(v)}" for k, v in p.items()))
                L.append(f"- IQR: {fmt(c.get('iqr'))} • Outliers (regra 1,5·IQR): "
                         f"{fmt(c.get('outliers_iqr'))} ({fmt(c.get('pct_outliers'))}%)")
            L.append(f"- Assimetria: {fmt(c.get('assimetria'))} • Curtose: {fmt(c.get('curtose'))}")
            L.append(f"- Zeros: {fmt(c.get('n_zeros'))} ({fmt(c.get('pct_zeros'))}%) "
                     f"• Negativos: {fmt(c.get('n_negativos'))}")

        elif lt == "texto":
            comp = c.get("comprimento", {})
            L.append(f"- Comprimento (min/máx/média/desvio): {fmt(comp.get('min'))} / "
                     f"{fmt(comp.get('max'))} / {fmt(comp.get('media'))} / {fmt(comp.get('desvio_padrao'))}")
            L.append(f"- Vazias: {fmt(c.get('n_vazias'))} ({fmt(c.get('pct_vazias'))}%)")
            L.append(f"- Aparência numérica: {fmt(c.get('n_aparencia_numerica'))} "
                     f"({fmt(c.get('pct_aparencia_numerica'))}%)")

        elif lt == "boolean":
            L.append(f"- True: {fmt(c.get('n_true'))} ({fmt(c.get('pct_true'))}%) • "
                     f"False: {fmt(c.get('n_false'))} ({fmt(c.get('pct_false'))}%)")
            L.append(f"- Razão de desbalanceamento (maior/menor): {fmt(c.get('razao_desbalanceamento'))}")

        elif lt == "temporal":
            L.append(f"- Min: {c.get('min')} • Máx: {c.get('max')}")

        if c.get("categorias"):
            cats = c["categorias"][:15]
            L.append(f"- Categorias ({len(c['categorias'])}): " +
                     ", ".join(f"`{k['valor']}` ({fmt(k['pct'])}%)" for k in cats)
                     + (" …" if len(c["categorias"]) > 15 else ""))
    L.append("")
    return "\n".join(L)


def print_console(profile):
    print(f"\n=== {os.path.basename(profile['arquivo'])} "
          f"({fmt(profile['n_linhas'])} linhas × {profile['n_colunas']} colunas) ===")
    for c in profile["colunas"]:
        flags = f"  [{', '.join(c['flags'])}]" if c.get("flags") else ""
        cat = "cat" if c.get("candidata_categorica") else "   "
        print(f"  {c['coluna']:<20} {c.get('tipo_logico',''):<9} "
              f"distintos={fmt(c.get('n_distintos')):>9}  card={c.get('nivel_cardinalidade',''):<9} {cat}"
              f"  ausentes={fmt(c.get('pct_ausentes'))}%{flags}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(argv):
    paths = argv[1:]
    if not paths:
        paths = sorted(glob.glob(os.path.join(PROJECT, "datasets", "**", "*.parquet"),
                                 recursive=True))
    if not paths:
        print("Nenhum arquivo encontrado. Passe caminhos ou coloque parquet em datasets/.")
        return 1

    os.makedirs(OUT_DIR, exist_ok=True)
    for path in paths:
        if not os.path.exists(path):
            print(f"[pular] não encontrado: {path}")
            continue
        prof = profile_dataset(path)
        print_console(prof)
        base = os.path.splitext(os.path.basename(path))[0]
        with open(os.path.join(OUT_DIR, f"{base}_perfil.md"), "w") as f:
            f.write(to_markdown(prof))
        with open(os.path.join(OUT_DIR, f"{base}_perfil.json"), "w") as f:
            json.dump(prof, f, ensure_ascii=False, indent=2)
        print(f"  -> profiles/{base}_perfil.md  e  profiles/{base}_perfil.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
