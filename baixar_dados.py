#!/usr/bin/env python3
"""
Baixa as bases do Kaggle e converte para Parquet nos caminhos esperados pelo projeto.

Requer o token da API do Kaggle configurado:
  - ~/.kaggle/kaggle.json, OU
  - variáveis de ambiente KAGGLE_USERNAME e KAGGLE_KEY.

Uso:
  python3 baixar_dados.py
"""
import os
import sys
import glob
import shutil
import tempfile
import subprocess

import duckdb

PROJECT = os.path.dirname(os.path.abspath(__file__))

# slug do Kaggle -> pasta destino + renomeações de arquivo (csv_base -> parquet_final)
BASES = [
    {
        "slug": "ealtman2019/credit-card-transactions",
        "destino": os.path.join(PROJECT, "datasets", "ibm_fraud"),
        "renomear": {},  # mantém os nomes originais
    },
    {
        "slug": "fedesoriano/heart-failure-prediction",
        "destino": os.path.join(PROJECT, "datasets", "heart"),
        "renomear": {"heart": "heart_failure"},  # heart.csv -> heart_failure.parquet
    },
]


def baixar_kaggle(slug, pasta_tmp):
    print(f"  baixando {slug} ...", flush=True)
    subprocess.run(
        ["kaggle", "datasets", "download", "-d", slug, "-p", pasta_tmp, "--unzip"],
        check=True,
    )


def csv_para_parquet(csv, parquet):
    con = duckdb.connect()
    esc_csv, esc_pq = csv.replace("'", "''"), parquet.replace("'", "''")
    con.execute(
        f"COPY (SELECT * FROM read_csv_auto('{esc_csv}', sample_size=-1)) "
        f"TO '{esc_pq}' (FORMAT PARQUET, COMPRESSION ZSTD)"
    )
    n = con.execute(f"SELECT COUNT(*) FROM read_parquet('{esc_pq}')").fetchone()[0]
    con.close()
    return n


def main():
    for base in BASES:
        print(f"== {base['slug']} ==")
        os.makedirs(base["destino"], exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp:
            try:
                baixar_kaggle(base["slug"], tmp)
            except FileNotFoundError:
                sys.exit("ERRO: CLI 'kaggle' não encontrada. Rode: pip install kaggle")
            except subprocess.CalledProcessError:
                sys.exit("ERRO: download falhou. Verifique seu token do Kaggle (~/.kaggle/kaggle.json).")

            for csv in sorted(glob.glob(os.path.join(tmp, "*.csv"))):
                base_nome = os.path.splitext(os.path.basename(csv))[0]
                final = base["renomear"].get(base_nome, base_nome)
                parquet = os.path.join(base["destino"], final + ".parquet")
                n = csv_para_parquet(csv, parquet)
                print(f"  -> {os.path.relpath(parquet, PROJECT)}  ({n:,} linhas)")
    print("\nConcluído. Dados prontos em datasets/.")


if __name__ == "__main__":
    main()
