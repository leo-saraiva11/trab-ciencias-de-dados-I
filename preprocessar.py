#!/usr/bin/env python3
"""
Motor de PRÉ-PROCESSAMENTO — Etapa (c).

Lê `config_preprocessamento.yaml` e processa cada base de dados aplicando um
pré-processamento DIFERENTE por algoritmo (KNN, Árvore de Decisão, MLP):
  - tratamento de valores ausentes (imputação/remoção) — configurável;
  - normalização/re-escala dos numéricos (z-score, min-max, robust) — configurável;
  - encoding dos categóricos (one-hot, ordinal, frequency, target) — configurável.

Boa prática (anti data leakage): faz o split treino/teste ANTES e ajusta todos
os transformadores SOMENTE no treino, aplicando depois ao teste.

Saídas em processed/:
  <base>_<perfil>_treino.parquet, <base>_<perfil>_teste.parquet
  <base>_<perfil>_preprocessador.pkl   (transformador ajustado, p/ etapa d)
  RELATORIO_preprocessamento.md        (o que foi aplicado — insumo do relatório)

Uso:
  python3 preprocessar.py                          # todas as bases × todos os perfis
  python3 preprocessar.py --dataset heart          # só heart, todos os perfis
  python3 preprocessar.py --dataset heart --perfil knn
"""
import os
import sys
import argparse
import pickle

import numpy as np
import pandas as pd
import duckdb
import yaml

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (StandardScaler, MinMaxScaler, RobustScaler,
                                   OneHotEncoder, OrdinalEncoder, TargetEncoder)
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split

PROJECT = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(PROJECT, "config_preprocessamento.yaml")
OUT_DIR = os.path.join(PROJECT, "processed")


# ---------------------------------------------------------------------------
# Conversões específicas de coluna (registro nome -> função)
# ---------------------------------------------------------------------------
def monetario_para_float(serie):
    """'$134.09' -> 134.09 (remove tudo que não for dígito, ponto ou sinal)."""
    limpo = serie.astype(str).str.replace(r"[^0-9.\-]", "", regex=True)
    return pd.to_numeric(limpo, errors="coerce")


CONVERSOES = {"monetario_para_float": monetario_para_float}


# ---------------------------------------------------------------------------
# Encoder de frequência (não existe pronto no sklearn)
# ---------------------------------------------------------------------------
class FrequencyEncoder(BaseEstimator, TransformerMixin):
    """Substitui cada categoria pela sua frequência relativa observada no treino."""

    def fit(self, X, y=None):
        Xdf = pd.DataFrame(X).reset_index(drop=True)
        self.n_features_in_ = Xdf.shape[1]
        self.mapas_ = [Xdf.iloc[:, j].value_counts(normalize=True).to_dict()
                       for j in range(Xdf.shape[1])]
        return self

    def transform(self, X):
        Xdf = pd.DataFrame(X).reset_index(drop=True)
        out = np.zeros(Xdf.shape, dtype=float)
        for j in range(Xdf.shape[1]):
            out[:, j] = Xdf.iloc[:, j].map(self.mapas_[j]).fillna(0.0).values
        return out

    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            input_features = [f"x{j}" for j in range(self.n_features_in_)]
        return np.asarray([f"{f}" for f in input_features], dtype=object)


# ---------------------------------------------------------------------------
# Fábricas de transformadores a partir da configuração
# ---------------------------------------------------------------------------
def make_scaler(nome):
    return {
        "zscore": StandardScaler(),
        "minmax": MinMaxScaler(),
        "robust": RobustScaler(),
        "nenhuma": "passthrough",
    }[nome]


def make_encoder(nome, random_state=42):
    if nome == "onehot":
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    if nome == "ordinal":
        return OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    if nome == "frequency":
        return FrequencyEncoder()
    if nome == "target":
        return TargetEncoder(random_state=random_state)
    raise ValueError(f"encoding desconhecido: {nome}")


def make_num_imputer(cfg):
    estrat = cfg.get("numericos", "mediana")
    mapa = {"media": "mean", "mediana": "median"}
    if estrat in mapa:
        return SimpleImputer(strategy=mapa[estrat])
    if estrat == "constante":
        return SimpleImputer(strategy="constant", fill_value=cfg.get("constante_num", 0))
    return None   # remover_coluna / remover_linhas tratados no driver


def make_cat_imputer(cfg):
    estrat = cfg.get("categoricos", "moda")
    if estrat == "moda":
        return SimpleImputer(strategy="most_frequent")
    if estrat == "constante":
        return SimpleImputer(strategy="constant",
                             fill_value=cfg.get("constante_cat", "DESCONHECIDO"))
    return None


# ---------------------------------------------------------------------------
# Carga dos dados (com amostragem via DuckDB p/ bases grandes)
# ---------------------------------------------------------------------------
def _qi(nome):
    return '"' + str(nome).replace('"', '""') + '"'


def _lit(v):
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def carregar_dados(ds_cfg):
    path = os.path.join(PROJECT, ds_cfg["arquivo"])
    alvo = ds_cfg["alvo"]
    manter = list(dict.fromkeys(ds_cfg["numericas"] + ds_cfg["categoricas"] + [alvo]))
    cols_sql = ", ".join(_qi(c) for c in manter)
    base = f"read_parquet('{path.replace(chr(39), chr(39) * 2)}')"
    con = duckdb.connect()

    amos = ds_cfg.get("amostragem", {}) or {}
    metodo = amos.get("metodo", "nenhuma")
    seed = amos.get("random_state", 42)

    if metodo == "undersample":
        contagem = con.execute(
            f'SELECT {_qi(alvo)} AS t, COUNT(*) c FROM {base} GROUP BY 1'
        ).fetchall()
        minoria = min(contagem, key=lambda r: r[1])
        n_min = minoria[1]
        n_maj = int(amos.get("ratio_neg_por_pos", 5)) * n_min
        sql = (
            f"SELECT {cols_sql} FROM {base} WHERE {_qi(alvo)} = {_lit(minoria[0])} "
            f"UNION ALL "
            f"SELECT {cols_sql} FROM (SELECT {cols_sql} FROM {base} "
            f"WHERE {_qi(alvo)} <> {_lit(minoria[0])}) "
            f"USING SAMPLE reservoir({n_maj} ROWS) REPEATABLE ({seed})"
        )
    elif metodo == "aleatoria":
        n = int(amos.get("n", 100000))
        sql = f"SELECT {cols_sql} FROM {base} USING SAMPLE reservoir({n} ROWS) REPEATABLE ({seed})"
    else:  # nenhuma
        sql = f"SELECT {cols_sql} FROM {base}"

    df = con.execute(sql).fetchdf()
    con.close()

    # conversões específicas de coluna (ex.: Amount "$" -> float)
    for col, fname in (ds_cfg.get("conversoes") or {}).items():
        if col in df.columns:
            df[col] = CONVERSOES[fname](df[col])

    # valores que representam ausência -> NaN
    for col, valores in (ds_cfg.get("valores_como_ausentes") or {}).items():
        if col in df.columns:
            df[col] = df[col].replace(list(valores), np.nan)

    return df


# ---------------------------------------------------------------------------
# Construção do ColumnTransformer conforme o perfil
# ---------------------------------------------------------------------------
def construir_preprocessador(perfil, num_cols, cat_cols):
    aus = perfil.get("ausentes", {})
    transformers = []

    if num_cols:
        num_imp = make_num_imputer(aus)
        passos = []
        if num_imp is not None:
            passos.append(("imputador", num_imp))
        passos.append(("normalizador", make_scaler(perfil.get("normalizacao", "nenhuma"))))
        transformers.append(("num", Pipeline(passos), num_cols))

    encoding = perfil.get("encoding", "onehot")
    if cat_cols and encoding != "nenhuma":
        cat_imp = make_cat_imputer(aus)
        passos = []
        if cat_imp is not None:
            passos.append(("imputador", cat_imp))
        passos.append(("encoder", make_encoder(encoding)))
        transformers.append(("cat", Pipeline(passos), cat_cols))

    return ColumnTransformer(transformers, remainder="drop",
                             verbose_feature_names_out=True)


def _limpar_nomes(nomes):
    return [n.split("__", 1)[1] if n.startswith(("num__", "cat__")) else n for n in nomes]


# ---------------------------------------------------------------------------
# Processa uma combinação (base × perfil)
# ---------------------------------------------------------------------------
def processar(ds_key, perfil_key, cfg):
    ds_cfg = cfg["datasets"][ds_key]
    perfil = cfg["perfis"][perfil_key]
    split_cfg = cfg.get("split", {})

    df = carregar_dados(ds_cfg)
    alvo = ds_cfg["alvo"]
    num_cols = [c for c in ds_cfg["numericas"] if c in df.columns]
    cat_cols = [c for c in ds_cfg["categoricas"] if c in df.columns]

    y = df[alvo]
    if y.dtype == bool:
        y = y.astype(int)

    aus = perfil.get("ausentes", {})
    log = {"base": ds_key, "perfil": perfil_key,
           "linhas_total": len(df), "descartadas_config": list(ds_cfg.get("descartar", [])),
           "descartadas_por_ausencia": [], "amostragem": ds_cfg.get("amostragem", {})}

    # remover_linhas: descarta linhas com ausência nas colunas afetadas
    if aus.get("numericos") == "remover_linhas":
        df = df.dropna(subset=num_cols)
    if aus.get("categoricos") == "remover_linhas":
        df = df.dropna(subset=cat_cols)
    y = df[alvo].astype(int) if df[alvo].dtype == bool else df[alvo]

    # remover_coluna: tira as colunas do conjunto de features
    if aus.get("numericos") == "remover_coluna":
        num_cols = []
    if aus.get("categoricos") == "remover_coluna":
        cat_cols = []

    X = df[num_cols + cat_cols]

    # split treino/teste (estratificado)
    estrat = y if split_cfg.get("estratificado", True) else None
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=split_cfg.get("test_size", 0.3),
        random_state=split_cfg.get("random_state", 42), stratify=estrat)

    # descarte automático de colunas com ausência acima do limiar (medido no TREINO)
    limiar = aus.get("descartar_coluna_acima_de", 1.0)
    frac_na = X_tr.isna().mean()
    a_descartar = [c for c in X_tr.columns if frac_na[c] > limiar]
    if a_descartar:
        log["descartadas_por_ausencia"] = [f"{c} ({frac_na[c]*100:.1f}%)" for c in a_descartar]
        num_cols = [c for c in num_cols if c not in a_descartar]
        cat_cols = [c for c in cat_cols if c not in a_descartar]
        X_tr = X_tr[num_cols + cat_cols]
        X_te = X_te[num_cols + cat_cols]

    # constrói, ajusta NO TREINO e transforma
    pre = construir_preprocessador(perfil, num_cols, cat_cols)
    Xtr_t = pre.fit_transform(X_tr, y_tr)
    Xte_t = pre.transform(X_te)
    feats = _limpar_nomes(list(pre.get_feature_names_out()))

    # monta DataFrames de saída (features + alvo) e salva
    os.makedirs(OUT_DIR, exist_ok=True)
    tr_df = pd.DataFrame(Xtr_t, columns=feats); tr_df[alvo] = y_tr.values
    te_df = pd.DataFrame(Xte_t, columns=feats); te_df[alvo] = y_te.values
    _salvar_parquet(tr_df, os.path.join(OUT_DIR, f"{ds_key}_{perfil_key}_treino.parquet"))
    _salvar_parquet(te_df, os.path.join(OUT_DIR, f"{ds_key}_{perfil_key}_teste.parquet"))
    try:
        with open(os.path.join(OUT_DIR, f"{ds_key}_{perfil_key}_preprocessador.pkl"), "wb") as f:
            pickle.dump(pre, f)
    except Exception as e:  # noqa: BLE001
        log["aviso_pickle"] = str(e)

    log.update({
        "num_cols": num_cols, "cat_cols": cat_cols,
        "n_treino": len(tr_df), "n_teste": len(te_df),
        "n_features_saida": len(feats), "features_saida": feats,
        "normalizacao": perfil.get("normalizacao"), "encoding": perfil.get("encoding"),
        "ausentes_num": aus.get("numericos"), "ausentes_cat": aus.get("categoricos"),
        "dist_classe_treino": y_tr.value_counts().to_dict(),
    })
    return log


def _salvar_parquet(df, caminho):
    con = duckdb.connect()
    con.register("t", df)
    esc = caminho.replace("'", "''")
    con.execute(f"COPY t TO '{esc}' (FORMAT PARQUET, COMPRESSION ZSTD)")
    con.close()


# ---------------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------------
def imprimir(log):
    print(f"\n=== {log['base']} × {log['perfil']} "
          f"(norm={log['normalizacao']}, encoding={log['encoding']}) ===")
    print(f"  linhas (após amostragem): {log['linhas_total']:,}  "
          f"-> treino {log['n_treino']:,} / teste {log['n_teste']:,}")
    print(f"  numéricas: {log['num_cols']}")
    print(f"  categóricas: {log['cat_cols']}")
    if log["descartadas_por_ausencia"]:
        print(f"  descartadas (>limiar ausência): {log['descartadas_por_ausencia']}")
    print(f"  ausentes: num={log['ausentes_num']} / cat={log['ausentes_cat']}")
    print(f"  features de saída: {log['n_features_saida']}")
    print(f"  distribuição classe (treino): {log['dist_classe_treino']}")


def escrever_relatorio(logs, caminho):
    L = ["# Relatório de Pré-processamento — Etapa (c)", "",
         "Gerado por `preprocessar.py` a partir de `config_preprocessamento.yaml`.",
         "Transformadores ajustados **somente no treino** (sem data leakage).", ""]
    for log in logs:
        L.append(f"## {log['base']} × {log['perfil']}")
        L.append("")
        L.append(f"- **Amostragem:** {log['amostragem']}")
        L.append(f"- **Linhas** (após amostragem): {log['linhas_total']:,} "
                 f"→ treino {log['n_treino']:,} / teste {log['n_teste']:,}")
        L.append(f"- **Numéricas:** {', '.join(f'`{c}`' for c in log['num_cols']) or '—'}")
        L.append(f"- **Categóricas:** {', '.join(f'`{c}`' for c in log['cat_cols']) or '—'}")
        L.append(f"- **Descartadas (config):** {', '.join(f'`{c}`' for c in log['descartadas_config']) or '—'}")
        L.append(f"- **Descartadas (>limiar ausência):** "
                 f"{', '.join(log['descartadas_por_ausencia']) or '—'}")
        L.append(f"- **Ausentes:** numéricos = `{log['ausentes_num']}`, categóricos = `{log['ausentes_cat']}`")
        L.append(f"- **Normalização:** `{log['normalizacao']}` • **Encoding:** `{log['encoding']}`")
        L.append(f"- **Features de saída:** {log['n_features_saida']}")
        L.append(f"- **Distribuição da classe (treino):** {log['dist_classe_treino']}")
        L.append(f"- **Arquivos:** `processed/{log['base']}_{log['perfil']}_treino.parquet`, "
                 f"`..._teste.parquet`, `..._preprocessador.pkl`")
        L.append("")
    with open(caminho, "w") as f:
        f.write("\n".join(L))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", help="chave da base (ex.: heart, fraude)")
    ap.add_argument("--perfil", help="chave do perfil (ex.: knn, arvore, mlp)")
    ap.add_argument("--config", default=CONFIG)
    args = ap.parse_args(argv[1:])

    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    bases = [args.dataset] if args.dataset else list(cfg["datasets"].keys())
    perfis = [args.perfil] if args.perfil else list(cfg["perfis"].keys())

    logs = []
    for ds in bases:
        for pf in perfis:
            try:
                log = processar(ds, pf, cfg)
                imprimir(log)
                logs.append(log)
            except Exception as e:  # noqa: BLE001
                print(f"\n[ERRO] {ds} × {pf}: {e}")
                raise

    if logs:
        os.makedirs(OUT_DIR, exist_ok=True)
        rel = os.path.join(OUT_DIR, "RELATORIO_preprocessamento.md")
        escrever_relatorio(logs, rel)
        print(f"\nRelatório: processed/RELATORIO_preprocessamento.md")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
