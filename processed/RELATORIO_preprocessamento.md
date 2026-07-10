# Relatório de Pré-processamento — Etapa (c)

Gerado por `preprocessar.py` a partir de `config_preprocessamento.yaml`.
Transformadores ajustados **somente no treino** (sem data leakage).

## heart × knn

- **Amostragem:** {'metodo': 'nenhuma'}
- **Linhas** (após amostragem): 918 → treino 642 / teste 276
- **Numéricas:** `Age`, `RestingBP`, `Cholesterol`, `MaxHR`, `Oldpeak`
- **Categóricas:** `Sex`, `ChestPainType`, `RestingECG`, `ExerciseAngina`, `ST_Slope`, `FastingBS`
- **Descartadas (config):** —
- **Descartadas (>limiar ausência):** —
- **Ausentes:** numéricos = `mediana`, categóricos = `moda`
- **Normalização:** `zscore` • **Encoding:** `onehot`
- **Features de saída:** 21
- **Distribuição da classe (treino):** {1: 355, 0: 287}
- **Arquivos:** `processed/heart_knn_treino.parquet`, `..._teste.parquet`, `..._preprocessador.pkl`

## heart × arvore

- **Amostragem:** {'metodo': 'nenhuma'}
- **Linhas** (após amostragem): 918 → treino 642 / teste 276
- **Numéricas:** `Age`, `RestingBP`, `Cholesterol`, `MaxHR`, `Oldpeak`
- **Categóricas:** `Sex`, `ChestPainType`, `RestingECG`, `ExerciseAngina`, `ST_Slope`, `FastingBS`
- **Descartadas (config):** —
- **Descartadas (>limiar ausência):** —
- **Ausentes:** numéricos = `mediana`, categóricos = `moda`
- **Normalização:** `nenhuma` • **Encoding:** `ordinal`
- **Features de saída:** 11
- **Distribuição da classe (treino):** {1: 355, 0: 287}
- **Arquivos:** `processed/heart_arvore_treino.parquet`, `..._teste.parquet`, `..._preprocessador.pkl`

## heart × mlp

- **Amostragem:** {'metodo': 'nenhuma'}
- **Linhas** (após amostragem): 918 → treino 642 / teste 276
- **Numéricas:** `Age`, `RestingBP`, `Cholesterol`, `MaxHR`, `Oldpeak`
- **Categóricas:** `Sex`, `ChestPainType`, `RestingECG`, `ExerciseAngina`, `ST_Slope`, `FastingBS`
- **Descartadas (config):** —
- **Descartadas (>limiar ausência):** —
- **Ausentes:** numéricos = `mediana`, categóricos = `moda`
- **Normalização:** `zscore` • **Encoding:** `onehot`
- **Features de saída:** 21
- **Distribuição da classe (treino):** {1: 355, 0: 287}
- **Arquivos:** `processed/heart_mlp_treino.parquet`, `..._teste.parquet`, `..._preprocessador.pkl`

## fraude × knn

- **Amostragem:** {'metodo': 'undersample', 'ratio_neg_por_pos': 5, 'random_state': 42}
- **Linhas** (após amostragem): 178,542 → treino 124,979 / teste 53,563
- **Numéricas:** `Amount`
- **Categóricas:** `Use Chip`, `Merchant State`, `MCC`, `Year`, `Month`
- **Descartadas (config):** `User`, `Card`, `Merchant Name`, `Merchant City`, `Zip`, `Day`, `Time`, `Errors?`
- **Descartadas (>limiar ausência):** —
- **Ausentes:** numéricos = `mediana`, categóricos = `moda`
- **Normalização:** `zscore` • **Encoding:** `onehot`
- **Features de saída:** 280
- **Distribuição da classe (treino):** {0: 104149, 1: 20830}
- **Arquivos:** `processed/fraude_knn_treino.parquet`, `..._teste.parquet`, `..._preprocessador.pkl`

## fraude × arvore

- **Amostragem:** {'metodo': 'undersample', 'ratio_neg_por_pos': 5, 'random_state': 42}
- **Linhas** (após amostragem): 178,542 → treino 124,979 / teste 53,563
- **Numéricas:** `Amount`
- **Categóricas:** `Use Chip`, `Merchant State`, `MCC`, `Year`, `Month`
- **Descartadas (config):** `User`, `Card`, `Merchant Name`, `Merchant City`, `Zip`, `Day`, `Time`, `Errors?`
- **Descartadas (>limiar ausência):** —
- **Ausentes:** numéricos = `mediana`, categóricos = `moda`
- **Normalização:** `nenhuma` • **Encoding:** `ordinal`
- **Features de saída:** 6
- **Distribuição da classe (treino):** {0: 104149, 1: 20830}
- **Arquivos:** `processed/fraude_arvore_treino.parquet`, `..._teste.parquet`, `..._preprocessador.pkl`

## fraude × mlp

- **Amostragem:** {'metodo': 'undersample', 'ratio_neg_por_pos': 5, 'random_state': 42}
- **Linhas** (após amostragem): 178,542 → treino 124,979 / teste 53,563
- **Numéricas:** `Amount`
- **Categóricas:** `Use Chip`, `Merchant State`, `MCC`, `Year`, `Month`
- **Descartadas (config):** `User`, `Card`, `Merchant Name`, `Merchant City`, `Zip`, `Day`, `Time`, `Errors?`
- **Descartadas (>limiar ausência):** —
- **Ausentes:** numéricos = `mediana`, categóricos = `moda`
- **Normalização:** `zscore` • **Encoding:** `onehot`
- **Features de saída:** 280
- **Distribuição da classe (treino):** {0: 104149, 1: 20830}
- **Arquivos:** `processed/fraude_mlp_treino.parquet`, `..._teste.parquet`, `..._preprocessador.pkl`
