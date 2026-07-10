# Perfil de Dados — `credit_card_transactions-ibm_v2.parquet`

- **Arquivo:** `datasets/ibm_fraud/credit_card_transactions-ibm_v2.parquet`
- **Linhas:** 24.386.900 • **Colunas:** 15
- **Gerado em:** 2026-07-09 20:12 (por `explorar_dados.py`)

## Resumo geral

| Coluna | Tipo lógico | % ausentes | Nº distintos | Cardinalidade | Categórica? | Moda | Flags |
|--------|-------------|-----------:|-------------:|---------------|:-----------:|------|-------|
| `User` | inteiro | 0,00% | 2.000 | alta | — | 486 | — |
| `Card` | inteiro | 0,00% | 9 | baixa | ✅ | 0 | categorica_card_baixa |
| `Year` | inteiro | 0,00% | 30 | media | ✅ | 2019 | categorica_card_media |
| `Month` | inteiro | 0,00% | 12 | media | ✅ | 1 | categorica_card_media |
| `Day` | inteiro | 0,00% | 31 | media | ✅ | 21 | categorica_card_media |
| `Time` | temporal | 0,00% | 1.440 | alta | — | 12:31:00 | — |
| `Amount` | texto | 0,00% | 98.953 | alta | — | $80.00 | texto_numerico |
| `Use Chip` | texto | 0,00% | 3 | baixa | ✅ | Swipe Transaction | categorica_card_baixa |
| `Merchant Name` | inteiro | 0,00% | 100.343 | alta | — | 1799189980464955940 | — |
| `Merchant City` | texto | 0,00% | 13.429 | alta | ✅ | ONLINE | categorica_card_alta |
| `Merchant State` | texto | 11,1569% | 223 | alta | ✅ | CA | categorica_card_alta |
| `Zip` | decimal | 11,8020% | 27.321 | alta | — | 98516.0 | — |
| `MCC` | inteiro | 0,00% | 109 | alta | — | 5411 | — |
| `Errors?` | texto | 98,4072% | 23 | media | ✅ | Insufficient Balance | muitos_ausentes, categorica_card_media |
| `Is Fraud?` | boolean | 0,00% | 2 | baixa | ✅ | False | categorica_card_baixa |

## Candidatas a categórica por cardinalidade

### Baixa cardinalidade (2–10 distintos) — ideal para **one-hot encoding**
- `Card` — 9 distintos _(inteiro)_
- `Use Chip` — 3 distintos _(texto)_
- `Is Fraud?` — 2 distintos _(boolean)_

### Média cardinalidade (11–50 distintos) — considerar **ordinal/target encoding**
- `Year` — 30 distintos _(inteiro)_
- `Month` — 12 distintos _(inteiro)_
- `Day` — 31 distintos _(inteiro)_
- `Errors?` — 23 distintos _(texto)_

### Alta cardinalidade (>50 distintos) — **encoding especial** (frequency/target/hashing)
- `Merchant City` — 13.429 distintos _(texto)_
- `Merchant State` — 223 distintos _(texto)_

## Detalhamento por coluna

### `User`  —  _inteiro_
- Preenchidos: 24.386.900 / 24.386.900 (ausentes: 0 = 0,00%)
- Distintos: 2.000 (0,0082% dos preenchidos)
- Moda: `486` (82.355× = 0,3377%)
- Min / Máx: 0,00 / 1.999,00 (amplitude 1.999,00)
- Média: 1.001,02 • Desvio-padrão: 569,4612 • Coef. variação: 0,5689
- Percentis: p1=17,00 | p5=97,00 | p25=510,00 | p50=1.006,00 | p75=1.477,00 | p95=1.893,00 | p99=1.978,00
- IQR: 967,00 • Outliers (regra 1,5·IQR): 0 (0,00%)
- Assimetria: -0,0222 • Curtose: -1,1483
- Zeros: 19.963 (0,0819%) • Negativos: 0

### `Card`  —  _inteiro_
- Preenchidos: 24.386.900 / 24.386.900 (ausentes: 0 = 0,00%)
- Distintos: 9 (0,00% dos preenchidos)
- Moda: `0` (8.696.411× = 35,6602%)
- Min / Máx: 0,00 / 8,00 (amplitude 8,00)
- Média: 1,3514 • Desvio-padrão: 1,4072 • Coef. variação: 1,0413
- Percentis: p1=0,00 | p5=0,00 | p25=0,00 | p50=1,00 | p75=2,00 | p95=4,00 | p99=5,00
- IQR: 2,00 • Outliers (regra 1,5·IQR): 228.296 (0,9361%)
- Assimetria: 1,0486 • Curtose: 0,7085
- Zeros: 8.696.411 (35,6602%) • Negativos: 0
- Categorias (9): `0` (35,6600%), `1` (26,6300%), `2` (17,6600%), `3` (11,4400%), `4` (5,3700%), `5` (2,3100%), `6` (0,7200%), `7` (0,1900%), `8` (0,0200%)

### `Year`  —  _inteiro_
- Preenchidos: 24.386.900 / 24.386.900 (ausentes: 0 = 0,00%)
- Distintos: 30 (0,0001% dos preenchidos)
- Moda: `2019` (1.723.938× = 7,0691%)
- Min / Máx: 1.991,00 / 2.020,00 (amplitude 29,00)
- Média: 2.011,96 • Desvio-padrão: 5,1059 • Coef. variação: 0,0025
- Percentis: p1=1.999,00 | p5=2.003,00 | p25=2.008,00 | p50=2.013,00 | p75=2.016,00 | p95=2.019,00 | p99=2.020,00
- IQR: 8,00 • Outliers (regra 1,5·IQR): 50.341 (0,2064%)
- Assimetria: -0,5602 • Curtose: -0,2966
- Zeros: 0 (0,00%) • Negativos: 0

### `Month`  —  _inteiro_
- Preenchidos: 24.386.900 / 24.386.900 (ausentes: 0 = 0,00%)
- Distintos: 12 (0,00% dos preenchidos)
- Moda: `1` (2.142.220× = 8,7843%)
- Min / Máx: 1,00 / 12,00 (amplitude 11,00)
- Média: 6,5251 • Desvio-padrão: 3,4724 • Coef. variação: 0,5322
- Percentis: p1=1,00 | p5=1,00 | p25=3,00 | p50=7,00 | p75=10,00 | p95=12,00 | p99=12,00
- IQR: 7,00 • Outliers (regra 1,5·IQR): 0 (0,00%)
- Assimetria: -0,0177 • Curtose: -1,2205
- Zeros: 0 (0,00%) • Negativos: 0
- Categorias (12): `1` (8,7800%), `12` (8,6300%), `10` (8,5100%), `8` (8,4900%), `7` (8,4100%), `11` (8,3100%), `5` (8,3000%), `9` (8,2300%), `3` (8,2100%), `6` (8,1200%), `2` (8,0400%), `4` (7,9600%)

### `Day`  —  _inteiro_
- Preenchidos: 24.386.900 / 24.386.900 (ausentes: 0 = 0,00%)
- Distintos: 31 (0,0001% dos preenchidos)
- Moda: `21` (813.404× = 3,3354%)
- Min / Máx: 1,00 / 31,00 (amplitude 30,00)
- Média: 15,7181 • Desvio-padrão: 8,7941 • Coef. variação: 0,5595
- Percentis: p1=1,00 | p5=2,00 | p25=8,00 | p50=16,00 | p75=23,00 | p95=29,00 | p99=31,00
- IQR: 15,00 • Outliers (regra 1,5·IQR): 0 (0,00%)
- Assimetria: 0,0066 • Curtose: -1,1927
- Zeros: 0 (0,00%) • Negativos: 0

### `Time`  —  _temporal_
- Preenchidos: 24.386.900 / 24.386.900 (ausentes: 0 = 0,00%)
- Distintos: 1.440 (0,0059% dos preenchidos)
- Moda: `12:31:00` (30.604× = 0,1255%)
- Min: 00:00:00 • Máx: 23:59:00

### `Amount`  —  _texto_
- Preenchidos: 24.386.900 / 24.386.900 (ausentes: 0 = 0,00%)
- Distintos: 98.953 (0,4058% dos preenchidos)
- Moda: `$80.00` (250.984× = 1,0292%)
- Comprimento (min/máx/média/desvio): 5,00 / 9,00 / 5,9658 / 0,6363
- Vazias: 0 (0,00%)
- Aparência numérica: 24.386.900 (100,00%)

### `Use Chip`  —  _texto_
- Preenchidos: 24.386.900 / 24.386.900 (ausentes: 0 = 0,00%)
- Distintos: 3 (0,00% dos preenchidos)
- Moda: `Swipe Transaction` (15.386.082× = 63,0916%)
- Comprimento (min/máx/média/desvio): 16,00 / 18,00 / 16,8534 / 0,5896
- Vazias: 0 (0,00%)
- Aparência numérica: 0 (0,00%)
- Categorias (3): `Swipe Transaction` (63,0900%), `Chip Transaction` (25,7800%), `Online Transaction` (11,1300%)

### `Merchant Name`  —  _inteiro_
- Preenchidos: 24.386.900 / 24.386.900 (ausentes: 0 = 0,00%)
- Distintos: 100.343 (0,4115% dos preenchidos)
- Moda: `1799189980464955940` (1.130.230× = 4,6346%)
- Min / Máx: -9.222.899.435.637.403.648,00 / 9.223.291.803.303.717.888,00 (amplitude 18.446.191.238.941.122.560,00)
- Média: -476.922.962.771.994.624,00 • Desvio-padrão: 4.758.939.870.684.041.216,00 • Coef. variação: -9,9784
- Percentis: p1=-8.821.071.778.930.380.800,00 | p5=-7.146.670.748.125.201.408,00 | p25=-4.500.542.936.415.012.352,00 | p50=-794.676.495.118.551.552,00 | p75=3.189.517.333.335.617.024,00 | p95=7.461.959.004.246.117.376,00 | p99=8.919.682.822.789.039.104,00
- IQR: 7.690.060.269.750.629.376,00 • Outliers (regra 1,5·IQR): 0 (0,00%)
- Assimetria: 0,2043 • Curtose: -1,0591
- Zeros: 0 (0,00%) • Negativos: 12.990.428

### `Merchant City`  —  _texto_
- Preenchidos: 24.386.900 / 24.386.900 (ausentes: 0 = 0,00%)
- Distintos: 13.429 (0,0551% dos preenchidos)
- Moda: `ONLINE` (2.720.821× = 11,1569%)
- Comprimento (min/máx/média/desvio): 3,00 / 26,00 / 8,5812 / 2,7443
- Vazias: 0 (0,00%)
- Aparência numérica: 0 (0,00%)

### `Merchant State`  —  _texto_
- Preenchidos: 21.666.079 / 24.386.900 (ausentes: 2.720.821 = 11,1569%)
- Distintos: 223 (0,0010% dos preenchidos)
- Moda: `CA` (2.591.830× = 11,9626%)
- Comprimento (min/máx/média/desvio): 2,00 / 32,00 / 2,0376 / 0,5043
- Vazias: 0 (0,00%)
- Aparência numérica: 0 (0,00%)

### `Zip`  —  _decimal_
- Preenchidos: 21.508.765 / 24.386.900 (ausentes: 2.878.135 = 11,8020%)
- Distintos: 27.321 (0,1270% dos preenchidos)
- Moda: `98516.0` (55.679× = 0,2589%)
- Min / Máx: 501,00 / 99.928,00 (amplitude 99.427,00)
- Média: 50.956,44 • Desvio-padrão: 29.397,07 • Coef. variação: 0,5769
- Percentis: p1=2.110,00 | p5=7.202,00 | p25=28.374,00 | p50=46.742,00 | p75=77.564,00 | p95=95.670,00 | p99=98.404,00
- IQR: 49.190,00 • Outliers (regra 1,5·IQR): 0 (0,00%)
- Assimetria: 0,1030 • Curtose: -1,2675
- Zeros: 0 (0,00%) • Negativos: 0

### `MCC`  —  _inteiro_
- Preenchidos: 24.386.900 / 24.386.900 (ausentes: 0 = 0,00%)
- Distintos: 109 (0,0004% dos preenchidos)
- Moda: `5411` (2.860.738× = 11,7306%)
- Min / Máx: 1.711,00 / 9.402,00 (amplitude 7.691,00)
- Média: 5.561,17 • Desvio-padrão: 879,3154 • Coef. variação: 0,1581
- Percentis: p1=3.596,00 | p5=4.121,00 | p25=5.300,00 | p50=5.499,00 | p75=5.812,00 | p95=7.538,00 | p99=8.049,00
- IQR: 512,00 • Outliers (regra 1,5·IQR): 4.059.356 (16,6456%)
- Assimetria: 1,1852 • Curtose: 3,5368
- Zeros: 0 (0,00%) • Negativos: 0

### `Errors?`  —  _texto_
- Preenchidos: 388.431 / 24.386.900 (ausentes: 23.998.469 = 98,4072%)
- Distintos: 23 (0,0059% dos preenchidos)
- Moda: `Insufficient Balance` (242.783× = 62,5035%)
- Comprimento (min/máx/média/desvio): 7,00 / 51,00 / 16,8355 / 5,0191
- Vazias: 0 (0,00%)
- Aparência numérica: 0 (0,00%)
- Categorias (23): `Insufficient Balance` (62,5000%), `Bad PIN` (15,1700%), `Technical Glitch` (12,4000%), `Bad Card Number` (3,4300%), `Bad CVV` (2,7600%), `Bad Expiration` (2,7600%), `Bad Zipcode` (0,5400%), `Bad PIN,Insufficient Balance` (0,1500%), `Insufficient Balance,Technical Glitch` (0,1200%), `Bad PIN,Technical Glitch` (0,0300%), `Bad Card Number,Insufficient Balance` (0,0300%), `Bad CVV,Insufficient Balance` (0,0200%), `Bad Expiration,Insufficient Balance` (0,0200%), `Bad Card Number,Bad CVV` (0,0200%), `Bad Card Number,Bad Expiration` (0,0100%) …

### `Is Fraud?`  —  _boolean_
- Preenchidos: 24.386.900 / 24.386.900 (ausentes: 0 = 0,00%)
- Distintos: 2 (0,00% dos preenchidos)
- Moda: `False` (24.357.143× = 99,8780%)
- True: 29.757 (0,1220%) • False: 24.357.143 (99,8780%)
- Razão de desbalanceamento (maior/menor): 818,5300
- Categorias (2): `False` (99,8800%), `True` (0,1200%)
