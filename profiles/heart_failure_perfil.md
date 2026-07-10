# Perfil de Dados — `heart_failure.parquet`

- **Arquivo:** `datasets/heart/heart_failure.parquet`
- **Linhas:** 918 • **Colunas:** 12
- **Gerado em:** 2026-07-09 20:12 (por `explorar_dados.py`)

## Resumo geral

| Coluna | Tipo lógico | % ausentes | Nº distintos | Cardinalidade | Categórica? | Moda | Flags |
|--------|-------------|-----------:|-------------:|---------------|:-----------:|------|-------|
| `Age` | inteiro | 0,00% | 50 | media | ✅ | 54 | categorica_card_media |
| `Sex` | texto | 0,00% | 2 | baixa | ✅ | M | categorica_card_baixa |
| `ChestPainType` | texto | 0,00% | 4 | baixa | ✅ | ASY | categorica_card_baixa |
| `RestingBP` | inteiro | 0,00% | 67 | alta | — | 120 | — |
| `Cholesterol` | inteiro | 0,00% | 222 | alta | — | 0 | — |
| `FastingBS` | inteiro | 0,00% | 2 | baixa | ✅ | 0 | categorica_card_baixa |
| `RestingECG` | texto | 0,00% | 3 | baixa | ✅ | Normal | categorica_card_baixa |
| `MaxHR` | inteiro | 0,00% | 119 | alta | — | 150 | — |
| `ExerciseAngina` | texto | 0,00% | 2 | baixa | ✅ | N | categorica_card_baixa |
| `Oldpeak` | decimal | 0,00% | 53 | alta | — | 0.0 | — |
| `ST_Slope` | texto | 0,00% | 3 | baixa | ✅ | Flat | categorica_card_baixa |
| `HeartDisease` | inteiro | 0,00% | 2 | baixa | ✅ | 1 | categorica_card_baixa |

## Candidatas a categórica por cardinalidade

### Baixa cardinalidade (2–10 distintos) — ideal para **one-hot encoding**
- `Sex` — 2 distintos _(texto)_
- `ChestPainType` — 4 distintos _(texto)_
- `FastingBS` — 2 distintos _(inteiro)_
- `RestingECG` — 3 distintos _(texto)_
- `ExerciseAngina` — 2 distintos _(texto)_
- `ST_Slope` — 3 distintos _(texto)_
- `HeartDisease` — 2 distintos _(inteiro)_

### Média cardinalidade (11–50 distintos) — considerar **ordinal/target encoding**
- `Age` — 50 distintos _(inteiro)_

### Alta cardinalidade (>50 distintos) — **encoding especial** (frequency/target/hashing)
- _(nenhuma)_

## Detalhamento por coluna

### `Age`  —  _inteiro_
- Preenchidos: 918 / 918 (ausentes: 0 = 0,00%)
- Distintos: 50 (5,4466% dos preenchidos)
- Moda: `54` (51× = 5,5556%)
- Min / Máx: 28,00 / 77,00 (amplitude 49,00)
- Média: 53,5109 • Desvio-padrão: 9,4326 • Coef. variação: 0,1763
- Percentis: p1=32,00 | p5=37,00 | p25=47,00 | p50=54,00 | p75=60,00 | p95=68,00 | p99=74,00
- IQR: 13,00 • Outliers (regra 1,5·IQR): 0 (0,00%)
- Assimetria: -0,1959 • Curtose: -0,3861
- Zeros: 0 (0,00%) • Negativos: 0

### `Sex`  —  _texto_
- Preenchidos: 918 / 918 (ausentes: 0 = 0,00%)
- Distintos: 2 (0,2179% dos preenchidos)
- Moda: `M` (725× = 78,9760%)
- Comprimento (min/máx/média/desvio): 1,00 / 1,00 / 1,00 / 0,00
- Vazias: 0 (0,00%)
- Aparência numérica: 0 (0,00%)
- Categorias (2): `M` (78,9800%), `F` (21,0200%)

### `ChestPainType`  —  _texto_
- Preenchidos: 918 / 918 (ausentes: 0 = 0,00%)
- Distintos: 4 (0,4357% dos preenchidos)
- Moda: `ASY` (496× = 54,0305%)
- Comprimento (min/máx/média/desvio): 2,00 / 3,00 / 2,9499 / 0,2183
- Vazias: 0 (0,00%)
- Aparência numérica: 0 (0,00%)
- Categorias (4): `ASY` (54,0300%), `NAP` (22,1100%), `ATA` (18,8500%), `TA` (5,0100%)

### `RestingBP`  —  _inteiro_
- Preenchidos: 918 / 918 (ausentes: 0 = 0,00%)
- Distintos: 67 (7,2985% dos preenchidos)
- Moda: `120` (132× = 14,3791%)
- Min / Máx: 0,00 / 200,00 (amplitude 200,00)
- Média: 132,3965 • Desvio-padrão: 18,5142 • Coef. variação: 0,1398
- Percentis: p1=95,00 | p5=106,00 | p25=120,00 | p50=130,00 | p75=140,00 | p95=160,00 | p99=180,00
- IQR: 20,00 • Outliers (regra 1,5·IQR): 28 (3,0501%)
- Assimetria: 0,1798 • Curtose: 3,2713
- Zeros: 1 (0,1089%) • Negativos: 0

### `Cholesterol`  —  _inteiro_
- Preenchidos: 918 / 918 (ausentes: 0 = 0,00%)
- Distintos: 222 (24,1830% dos preenchidos)
- Moda: `0` (172× = 18,7364%)
- Min / Máx: 0,00 / 603,00 (amplitude 603,00)
- Média: 198,7996 • Desvio-padrão: 109,3841 • Coef. variação: 0,5502
- Percentis: p1=0,00 | p5=0,00 | p25=173,2500 | p50=223,00 | p75=267,00 | p95=331,3000 | p99=411,4900
- IQR: 93,7500 • Outliers (regra 1,5·IQR): 183 (19,9346%)
- Assimetria: -0,6101 • Curtose: 0,1182
- Zeros: 172 (18,7364%) • Negativos: 0

### `FastingBS`  —  _inteiro_
- Preenchidos: 918 / 918 (ausentes: 0 = 0,00%)
- Distintos: 2 (0,2179% dos preenchidos)
- Moda: `0` (704× = 76,6885%)
- Min / Máx: 0,00 / 1,00 (amplitude 1,00)
- Média: 0,2331 • Desvio-padrão: 0,4230 • Coef. variação: 1,8147
- Percentis: p1=0,00 | p5=0,00 | p25=0,00 | p50=0,00 | p75=0,00 | p95=1,00 | p99=1,00
- IQR: 0,00 • Outliers (regra 1,5·IQR): 214 (23,3115%)
- Assimetria: 1,2645 • Curtose: -0,4020
- Zeros: 704 (76,6885%) • Negativos: 0
- Categorias (2): `0` (76,6900%), `1` (23,3100%)

### `RestingECG`  —  _texto_
- Preenchidos: 918 / 918 (ausentes: 0 = 0,00%)
- Distintos: 3 (0,3268% dos preenchidos)
- Moda: `Normal` (552× = 60,1307%)
- Comprimento (min/máx/média/desvio): 2,00 / 6,00 / 4,6100 / 1,7369
- Vazias: 0 (0,00%)
- Aparência numérica: 0 (0,00%)
- Categorias (3): `Normal` (60,1300%), `LVH` (20,4800%), `ST` (19,3900%)

### `MaxHR`  —  _inteiro_
- Preenchidos: 918 / 918 (ausentes: 0 = 0,00%)
- Distintos: 119 (12,9630% dos preenchidos)
- Moda: `150` (43× = 4,6841%)
- Min / Máx: 60,00 / 202,00 (amplitude 142,00)
- Média: 136,8094 • Desvio-padrão: 25,4603 • Coef. variação: 0,1861
- Percentis: p1=77,1700 | p5=96,00 | p25=120,00 | p50=138,00 | p75=156,00 | p95=178,00 | p99=186,00
- IQR: 36,00 • Outliers (regra 1,5·IQR): 2 (0,2179%)
- Assimetria: -0,1444 • Curtose: -0,4482
- Zeros: 0 (0,00%) • Negativos: 0

### `ExerciseAngina`  —  _texto_
- Preenchidos: 918 / 918 (ausentes: 0 = 0,00%)
- Distintos: 2 (0,2179% dos preenchidos)
- Moda: `N` (547× = 59,5861%)
- Comprimento (min/máx/média/desvio): 1,00 / 1,00 / 1,00 / 0,00
- Vazias: 0 (0,00%)
- Aparência numérica: 0 (0,00%)
- Categorias (2): `N` (59,5900%), `Y` (40,4100%)

### `Oldpeak`  —  _decimal_
- Preenchidos: 918 / 918 (ausentes: 0 = 0,00%)
- Distintos: 53 (5,7734% dos preenchidos)
- Moda: `0.0` (368× = 40,0871%)
- Min / Máx: -2,6000 / 6,2000 (amplitude 8,8000)
- Média: 0,8874 • Desvio-padrão: 1,0666 • Coef. variação: 1,2020
- Percentis: p1=-0,5000 | p5=0,00 | p25=0,00 | p50=0,6000 | p75=1,5000 | p95=3,00 | p99=4,00
- IQR: 1,5000 • Outliers (regra 1,5·IQR): 16 (1,7429%)
- Assimetria: 1,0229 • Curtose: 1,2031
- Zeros: 368 (40,0871%) • Negativos: 13

### `ST_Slope`  —  _texto_
- Preenchidos: 918 / 918 (ausentes: 0 = 0,00%)
- Distintos: 3 (0,3268% dos preenchidos)
- Moda: `Flat` (460× = 50,1089%)
- Comprimento (min/máx/média/desvio): 2,00 / 4,00 / 3,1394 / 0,9908
- Vazias: 0 (0,00%)
- Aparência numérica: 0 (0,00%)
- Categorias (3): `Flat` (50,1100%), `Up` (43,0300%), `Down` (6,8600%)

### `HeartDisease`  —  _inteiro_
- Preenchidos: 918 / 918 (ausentes: 0 = 0,00%)
- Distintos: 2 (0,2179% dos preenchidos)
- Moda: `1` (508× = 55,3377%)
- Min / Máx: 0,00 / 1,00 (amplitude 1,00)
- Média: 0,5534 • Desvio-padrão: 0,4974 • Coef. variação: 0,8989
- Percentis: p1=0,00 | p5=0,00 | p25=0,00 | p50=1,00 | p75=1,00 | p95=1,00 | p99=1,00
- IQR: 1,00 • Outliers (regra 1,5·IQR): 0 (0,00%)
- Assimetria: -0,2151 • Curtose: -1,9580
- Zeros: 410 (44,6623%) • Negativos: 0
- Categorias (2): `1` (55,3400%), `0` (44,6600%)
