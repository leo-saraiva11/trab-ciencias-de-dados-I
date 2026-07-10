# Trabalho Final — Ciência de Dados (UFU): Comparação de Classificadores

Comparação de três classificadores — **KNN**, **Árvore de Decisão** e **MLP** (rede
neural) — em duas bases de dados reais e bem diferentes:

- **IBM Credit Card Fraud** (transações de cartão, base grande e desbalanceada);
- **Heart Failure Prediction** (dados clínicos, base pequena e balanceada).

> Disciplina: Ciência de Dados — Sistemas de Informação — UFU — Profa. Elaine Ribeiro Faria.

## Estrutura do projeto

| Arquivo / pasta | O que é |
|-----------------|---------|
| `baixar_dados.py` | Baixa as bases do Kaggle e converte para Parquet |
| `explorar_dados.py` | Perfil/exploração automática das bases (etapa b) → `profiles/` |
| `preprocessar.py` + `config_preprocessamento.yaml` | Pré-processamento por algoritmo (etapa c) → `processed/` |
| `treinar.py` + `config_modelos.yaml` | Treino e avaliação dos 3 algoritmos (etapa d/e) → `resultados/` |
| `insumos_relatorio.md` | **Documento consolidado** — base para o relatório final |
| `Trabalho-CD.pdf` | Enunciado do trabalho |
| `datasets/` | Dados brutos — **não versionados** (baixe com `baixar_dados.py`) |

## Pré-requisitos

- Python 3.9+
- Dependências: `pip install -r requirements.txt`
- **Token da API do Kaggle:** acesse <https://www.kaggle.com/settings> → seção *API* →
  *Create New API Token* e salve o `kaggle.json` em `~/.kaggle/kaggle.json`
  (ou defina as variáveis `KAGGLE_USERNAME` e `KAGGLE_KEY`).

## Como reproduzir (pipeline completo)

```bash
pip install -r requirements.txt
python3 baixar_dados.py       # 1) baixa as bases do Kaggle e converte p/ Parquet (datasets/)
python3 explorar_dados.py     # 2) exploração  -> profiles/
python3 preprocessar.py       # 3) pré-processamento -> processed/
python3 treinar.py            # 4) treino/avaliação  -> resultados/
```

Os resultados finais estão em `insumos_relatorio.md` (seções 3 e 4) e em
`resultados/RELATORIO_resultados.md`.

## ⚠️ Avisos

- **Nunca** faça commit do seu `kaggle.json` ou do token — o `.gitignore` já bloqueia.
- Os dados brutos (`datasets/`) e artefatos grandes (`processed/*.parquet`, `*.pkl`)
  não vão para o repositório; são regenerados pelos scripts acima.
- Entendam o código antes da apresentação (exigência do enunciado).
