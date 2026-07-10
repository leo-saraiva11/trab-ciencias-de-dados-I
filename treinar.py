#!/usr/bin/env python3
"""
Treinamento e avaliação dos classificadores — Etapa (d/e).

Para cada base (heart, fraude) e cada algoritmo (KNN, Árvore, MLP), treina todas
as parametrizações definidas em `config_modelos.yaml` usando os dados já
pré-processados com o perfil correspondente (processed/<base>_<algo>_treino/teste).

Avalia no conjunto de TESTE com várias métricas e produz:
  - resultados/resultados.csv          (tabela completa)
  - resultados/RELATORIO_resultados.md (tabela + melhor por base — insumo do relatório)

Uso:
  python3 treinar.py                       # todas as bases × todos os modelos
  python3 treinar.py --dataset heart       # só heart
  python3 treinar.py --dataset heart --model knn
"""
import os
import sys
import time
import argparse

import warnings
import numpy as np
import pandas as pd
import duckdb
import yaml

warnings.filterwarnings("ignore")   # silencia ConvergenceWarning do MLP, etc.
np.seterr(all="ignore")             # silencia RuntimeWarning de overflow/matmul (numpy 2.0)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score)

PROJECT = os.path.dirname(os.path.abspath(__file__))
PROC_DIR = os.path.join(PROJECT, "processed")
OUT_DIR = os.path.join(PROJECT, "resultados")
CFG_MODELOS = os.path.join(PROJECT, "config_modelos.yaml")
CFG_PREP = os.path.join(PROJECT, "config_preprocessamento.yaml")

REGISTRO = {
    "KNeighborsClassifier": KNeighborsClassifier,
    "DecisionTreeClassifier": DecisionTreeClassifier,
    "MLPClassifier": MLPClassifier,
}


def carregar_parquet(caminho):
    return duckdb.connect().execute(
        f"SELECT * FROM read_parquet('{caminho.replace(chr(39), chr(39)*2)}')").fetchdf()


def instanciar(classe_nome, params):
    cls = REGISTRO[classe_nome]
    params = dict(params)
    if classe_nome == "KNeighborsClassifier" and "n_jobs" not in params:
        params["n_jobs"] = -1   # paraleliza (alta dimensionalidade na base de fraude)
    return cls(**params)


def calcular_metricas(y_true, y_pred, y_score):
    return {
        "acuracia": accuracy_score(y_true, y_pred),
        "precisao": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_score) if y_score is not None else np.nan,
    }


def treinar_um(base, algo, classe_nome, param, alvo):
    tr = carregar_parquet(os.path.join(PROC_DIR, f"{base}_{algo}_treino.parquet"))
    te = carregar_parquet(os.path.join(PROC_DIR, f"{base}_{algo}_teste.parquet"))
    Xtr, ytr = tr.drop(columns=[alvo]), tr[alvo].astype(int)
    Xte, yte = te.drop(columns=[alvo]), te[alvo].astype(int)

    modelo = instanciar(classe_nome, param["params"])
    t0 = time.perf_counter()
    modelo.fit(Xtr, ytr)
    t_treino = time.perf_counter() - t0

    y_pred = modelo.predict(Xte)
    try:
        y_score = modelo.predict_proba(Xte)[:, 1]
    except Exception:  # noqa: BLE001
        y_score = None

    met = calcular_metricas(yte, y_pred, y_score)
    met.update({"base": base, "algoritmo": algo, "parametrizacao": param["nome"],
                "tempo_treino_s": round(t_treino, 2), "n_features": Xtr.shape[1],
                "n_treino": len(Xtr), "n_teste": len(Xte)})
    return met


# ---------------------------------------------------------------------------
def escrever_relatorio(df, caminho):
    ordem = ["base", "algoritmo", "parametrizacao", "acuracia", "precisao",
             "recall", "f1", "roc_auc", "tempo_treino_s"]
    df = df[ordem + [c for c in df.columns if c not in ordem]]

    L = ["# Resultados — Comparação de Classificadores (Etapa d/e)", "",
         "Métricas calculadas no conjunto de **teste** (holdout 70/30 estratificado).",
         "Cada algoritmo usou seu pré-processamento próprio (ver etapa c).", ""]

    L.append("## Fórmulas das métricas")
    L.append("")
    L.append("Sendo VP/VN/FP/FN = verdadeiros/falsos positivos/negativos:")
    L.append("- **Acurácia** = (VP+VN) / (VP+VN+FP+FN)")
    L.append("- **Precisão** = VP / (VP+FP)")
    L.append("- **Recall (Revocação)** = VP / (VP+FN)")
    L.append("- **F1-score** = 2 · (Precisão · Recall) / (Precisão + Recall)")
    L.append("- **ROC-AUC** = área sob a curva ROC (TPR × FPR em vários limiares)")
    L.append("")

    for base in df["base"].unique():
        sub = df[df["base"] == base].copy()
        L.append(f"## Base: {base}")
        L.append("")
        L.append("| Algoritmo | Parametrização | Acurácia | Precisão | Recall | F1 | ROC-AUC | Treino (s) |")
        L.append("|-----------|----------------|---------:|---------:|-------:|---:|--------:|-----------:|")
        for _, r in sub.iterrows():
            L.append(f"| {r['algoritmo']} | {r['parametrizacao']} "
                     f"| {r['acuracia']:.3f} | {r['precisao']:.3f} | {r['recall']:.3f} "
                     f"| {r['f1']:.3f} | {r['roc_auc']:.3f} | {r['tempo_treino_s']:.2f} |")
        melhor_f1 = sub.loc[sub["f1"].idxmax()]
        melhor_auc = sub.loc[sub["roc_auc"].idxmax()]
        L.append("")
        L.append(f"- **Melhor F1:** {melhor_f1['algoritmo']} ({melhor_f1['parametrizacao']}) "
                 f"= {melhor_f1['f1']:.3f}")
        L.append(f"- **Melhor ROC-AUC:** {melhor_auc['algoritmo']} ({melhor_auc['parametrizacao']}) "
                 f"= {melhor_auc['roc_auc']:.3f}")
        L.append("")

    with open(caminho, "w") as f:
        f.write("\n".join(L))


# ---------------------------------------------------------------------------
def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", help="chave da base (heart, fraude)")
    ap.add_argument("--model", help="chave do modelo (knn, arvore, mlp)")
    args = ap.parse_args(argv[1:])

    with open(CFG_MODELOS) as f:
        cfg = yaml.safe_load(f)
    with open(CFG_PREP) as f:
        alvos = {k: v["alvo"] for k, v in yaml.safe_load(f)["datasets"].items()}

    bases = [args.dataset] if args.dataset else list(alvos.keys())
    modelos = [args.model] if args.model else list(cfg["modelos"].keys())

    linhas = []
    for base in bases:
        for algo in modelos:
            mcfg = cfg["modelos"][algo]
            for param in mcfg["parametrizacoes"]:
                tr_path = os.path.join(PROC_DIR, f"{base}_{algo}_treino.parquet")
                if not os.path.exists(tr_path):
                    print(f"[pular] falta {os.path.basename(tr_path)} — rode preprocessar.py")
                    continue
                print(f"treinando {base} × {algo} × {param['nome']} ...", flush=True)
                res = treinar_um(base, algo, mcfg["classe"], param, alvos[base])
                print(f"    acc={res['acuracia']:.3f} f1={res['f1']:.3f} "
                      f"auc={res['roc_auc']:.3f} ({res['tempo_treino_s']:.1f}s)")
                linhas.append(res)

    if not linhas:
        print("Nada treinado.")
        return 1

    df = pd.DataFrame(linhas)
    os.makedirs(OUT_DIR, exist_ok=True)
    df.to_csv(os.path.join(OUT_DIR, "resultados.csv"), index=False)
    escrever_relatorio(df, os.path.join(OUT_DIR, "RELATORIO_resultados.md"))
    print("\n-> resultados/resultados.csv e resultados/RELATORIO_resultados.md")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
