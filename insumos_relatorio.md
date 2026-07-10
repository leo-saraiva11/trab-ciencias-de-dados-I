# Insumos para o Relatório Final — Comparação de Classificadores

> **Disciplina:** Ciência de Dados — Sistemas de Informação — UFU
> **Professora:** Elaine Ribeiro Faria
> **Tema:** Comparação de Classificadores
>
> Documento de trabalho (vivo) para juntar os insumos do relatório final. Vai
> sendo preenchido conforme o trabalho avança. Ao final, vira a base para gerar
> o PDF de entrega.

**Cabeçalho da entrega:**
- Leonardo Rodrigues Oliveira Saraiva — 12321BSI284
- Murilo de Melo Barbosa Santos — 12321BSI245
- Vitor Costa Andrade — 12321BSI255

---

## 0. Checklist do enunciado

| # | Requisito | Status |
|---|-----------|--------|
| a | Escolher **2 bases públicas** + citar fonte/link | ✅ Feito |
| b | **Exploração** dos dados (atributos, tipos, ausentes, classe, balanceamento) | ✅ Feito |
| c | **Pré-processamento** (justificado por base) | ✅ Feito (seção 2.3) |
| d | **3 algoritmos** de classificação (≥1 não visto em aula) | ✅ Feito (seção 2.4) |
| e | **Split treino/teste** + **≥2 métricas** + **≥2 parametrizações** por algoritmo | ✅ Feito (seções 2.5–2.7 e 3) |
| — | Discussão de resultados + tabela-resumo | ✅ Feito (seções 3 e 4) |
| — | **Declaração de uso de LLMs** (qual, onde, prompt) | ✅ Feito (seção 5) |
| — | Escrever o texto do relatório e gerar o PDF | ⬜ A fazer (juntar com este material) |

---

## 1. Bases de dados escolhidas

Ambas as bases foram baixadas do Kaggle e convertidas para **Parquet** (formato
colunar, compactado com ZSTD) para carregamento rápido. Estão em `datasets/`.

### 1.1. Base #1 — IBM Credit Card Fraud Detection

| Campo | Valor |
|-------|-------|
| **Nome** | Credit Card Transactions (IBM — dados sintéticos, TabFormer) |
| **Fonte / link** | https://www.kaggle.com/datasets/ealtman2019/credit-card-transactions |
| **Licença** | Other (Kaggle) |
| **Nº de instâncias** | **24.386.900** |
| **Nº de atributos** | 15 (14 preditores + 1 classe) |
| **Atributo classe** | `Is Fraud?` (booleano) |
| **Balanceamento** | ❌ **Fortemente desbalanceado** — 99,878% não-fraude vs **0,122% fraude** (29.757 casos) |
| **Arquivo** | `datasets/ibm_fraud/credit_card_transactions-ibm_v2.parquet` (186 MB) |

**Atributos e tipos:**

| Atributo | Tipo | Descrição | Ausentes |
|----------|------|-----------|----------|
| `User` | inteiro | ID do usuário | 0% |
| `Card` | inteiro | ID do cartão do usuário | 0% |
| `Year` | inteiro | Ano da transação | 0% |
| `Month` | inteiro | Mês da transação | 0% |
| `Day` | inteiro | Dia da transação | 0% |
| `Time` | hora (HH:MM) | Horário da transação | 0% |
| `Amount` | texto (`$134.09`) | Valor — vem com `$`, precisa virar número | 0% |
| `Use Chip` | categórico | Swipe / Chip / Online Transaction | 0% |
| `Merchant Name` | inteiro (hash) | Identificador do comerciante (não é o nome real) | 0% |
| `Merchant City` | texto | Cidade do comerciante | 0% |
| `Merchant State` | texto | Estado do comerciante | **11,16%** |
| `Zip` | numérico | CEP do comerciante | **11,80%** |
| `MCC` | inteiro | Merchant Category Code (categoria do comércio) | 0% |
| `Errors?` | texto | Erro na transação (ex.: Bad PIN) | **98,41%** |
| `Is Fraud?` | booleano | **CLASSE** — a transação é fraude? | 0% |

**Observações relevantes p/ pré-processamento:**
- `Amount` é texto por causa do `$` → converter para float.
- `Merchant Name` é um hash numérico, não uma string legível.
- Ausentes concentrados em `Errors?` (quase tudo nulo → provavelmente descartar),
  `Merchant State` e `Zip` (transações online não têm local físico).
- Base **imensa e muito desbalanceada** → provável necessidade de **amostragem**
  e/ou técnicas de balanceamento (ex.: undersampling, `class_weight`).
- Arquivos auxiliares (opcionais, para enriquecer): `sd254_cards.parquet` (cartões),
  `sd254_users.parquet` (usuários), `User0_credit_card_transactions.parquet` (amostra).

### 1.2. Base #2 — Heart Failure Prediction

| Campo | Valor |
|-------|-------|
| **Nome** | Heart Failure Prediction |
| **Fonte / link** | https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction |
| **Licença** | ODbL-1.0 |
| **Nº de instâncias** | **918** |
| **Nº de atributos** | 12 (11 preditores + 1 classe) |
| **Atributo classe** | `HeartDisease` (0 = não, 1 = sim) |
| **Balanceamento** | ✅ **Balanceado** — 55,3% (classe 1) vs 44,7% (classe 0) |
| **Arquivo** | `datasets/heart/heart_failure.parquet` (8,9 KB) |

**Atributos e tipos:**

| Atributo | Tipo | Descrição | Ausentes |
|----------|------|-----------|----------|
| `Age` | inteiro | Idade do paciente | 0% |
| `Sex` | categórico | Sexo (M / F) | 0% |
| `ChestPainType` | categórico | Tipo de dor no peito (ASY / ATA / NAP / TA) | 0% |
| `RestingBP` | inteiro | Pressão arterial em repouso (mmHg) | 0% |
| `Cholesterol` | inteiro | Colesterol sérico (mg/dl) | 0% |
| `FastingBS` | inteiro (0/1) | Glicemia em jejum > 120 mg/dl | 0% |
| `RestingECG` | categórico | ECG em repouso (Normal / ST / LVH) | 0% |
| `MaxHR` | inteiro | Frequência cardíaca máxima atingida | 0% |
| `ExerciseAngina` | categórico | Angina induzida por exercício (Y / N) | 0% |
| `Oldpeak` | decimal | Depressão do segmento ST | 0% |
| `ST_Slope` | categórico | Inclinação do segmento ST (Up / Flat / Down) | 0% |
| `HeartDisease` | inteiro (0/1) | **CLASSE** — presença de doença cardíaca | 0% |

**Observações relevantes p/ pré-processamento:**
- Sem valores ausentes explícitos, **mas há "0 disfarçado de ausente"**:
  `Cholesterol == 0` em **172 linhas** e `RestingBP == 0` em **1 linha**
  (valores fisiologicamente impossíveis → imputar pela mediana ou remover).
- 5 atributos categóricos → precisam de **encoding** (one-hot ou label).
- 6 atributos numéricos em escalas diferentes → precisam de **normalização/padronização**
  (importante para KNN, SVM, regressão logística).

### 1.3. Por que essas duas bases combinam

As bases fazem um **bom contraste** para a comparação de classificadores:

| Aspecto | Base #1 (Fraude) | Base #2 (Cardíaca) |
|---------|------------------|--------------------|
| Tamanho | Muito grande (24M) | Pequena (918) |
| Balanceamento | Extremamente desbalanceado | Balanceado |
| Tipos de atributo | Numérico + categórico + texto | Numérico + categórico |
| Desafio principal | Escala + desbalanceamento | Encoding + "0 ausente" |

Isso permite discutir como os mesmos algoritmos se comportam em cenários
bem diferentes (ver seção de discussão).

---

## 2. Metodologia

### 2.1. Ferramentas, linguagem e pacotes

- **Linguagem:** Python 3.
- **Pacotes:** `scikit-learn` 1.6 (modelos, pré-processamento e métricas),
  `pandas` (manipulação), `DuckDB` (leitura/escrita eficiente de Parquet),
  `PyYAML` (arquivos de configuração), `numpy`.
- **Formato dos dados:** Parquet (colunar, compactado com ZSTD).
- **Scripts do projeto** (todos autorais, feitos para este trabalho):
  - `explorar_dados.py` — exploração/perfil automático das bases (etapa b);
  - `preprocessar.py` + `config_preprocessamento.yaml` — pré-processamento (etapa c);
  - `treinar.py` + `config_modelos.yaml` — treino e avaliação (etapas d/e).
- **Relatórios gerados automaticamente:** `profiles/` (exploração),
  `processed/RELATORIO_preprocessamento.md` e `resultados/RELATORIO_resultados.md`.

### 2.2. Exploração dos dados (etapa b)

Um profiler automático (`explorar_dados.py`) calcula, para cada coluna, métricas
de qualidade por tipo: numéricas (min, máx, média, desvio, percentis, IQR,
outliers, assimetria, curtose), textuais (comprimento, % com aparência numérica),
cardinalidade (baixa/média/alta) e % de valores ausentes. Principais achados que
guiaram o pré-processamento:

- **Fraude:** classe `Is Fraud?` com apenas **0,122%** de fraudes (fortemente
  desbalanceada); `Errors?` **98,4%** ausente; `Amount` armazenado como texto
  (`$134.09`); `Merchant State`/`Zip` ~11% ausentes; IDs de alta cardinalidade
  (`Merchant Name` ≈ 100 mil valores).
- **Cardíaca:** classe `HeartDisease` balanceada (**55/45**); `Cholesterol` com
  **172 zeros** e `RestingBP` com **1 zero** (fisiologicamente impossíveis →
  tratados como ausentes).

### 2.3. Pré-processamento aplicado (etapa c)

O pré-processamento foi **ajustado somente no conjunto de treino** e aplicado ao
teste (evita *data leakage*). **Cada algoritmo recebeu um pré-processamento
próprio**, justificado pela natureza do algoritmo:

| Algoritmo | Valores ausentes | Normalização | Encoding categórico | Justificativa |
|-----------|------------------|--------------|---------------------|---------------|
| **KNN** | num.: mediana; cat.: moda | **Z-score** | **One-hot** | é baseado em distância → exige features na mesma escala; one-hot evita ordem artificial |
| **Árvore** | num.: mediana; cat.: moda | **Nenhuma** | **Ordinal** | é invariante à escala; ordinal mantém a dimensionalidade baixa |
| **MLP** | num.: mediana; cat.: moda | **Z-score** | **One-hot** | treino por gradiente é sensível à escala → padronização é essencial |

Tratamentos específicos por base:

- **Cardíaca:** `Cholesterol == 0` e `RestingBP == 0` convertidos para ausente e
  imputados pela **mediana** (calculada no treino).
- **Fraude:** `Amount` convertido de texto para número (`$134.09` → `134.09`);
  descartadas colunas de ID de alta cardinalidade (`User`, `Card`,
  `Merchant Name`, `Merchant City`, `Zip`, `Time`, `Day`) e a coluna `Errors?`
  (98% ausente); aplicado **undersampling** da classe majoritária na proporção
  **5 não-fraudes : 1 fraude** (a base original de 24M linhas é inviável e
  degeneraria a acurácia). Resultado: 178.542 linhas.

Toda a configuração é parametrizável no `config_preprocessamento.yaml`
(normalização: `zscore`/`minmax`/`robust`/`nenhuma`; encoding:
`onehot`/`ordinal`/`frequency`/`target`/`nenhuma`; ausentes:
`media`/`mediana`/`constante`/`remover_*`).

### 2.4. Algoritmos de classificação

Foram usados **3 algoritmos** (implementações do scikit-learn):

**a) KNN — K-Nearest Neighbors** *(clássico, visto em aula — usado como baseline)*
1. Armazena todos os exemplos de treino (aprendizado "preguiçoso", sem modelo explícito);
2. para classificar um novo ponto, calcula a distância (euclidiana) a todos os exemplos;
3. seleciona os **K** vizinhos mais próximos;
4. atribui a classe majoritária entre eles (opcionalmente ponderada pelo inverso da distância).

**b) Árvore de Decisão** *(visto em aula)*
1. Escolhe o atributo/limiar que melhor separa as classes (menor impureza — **Gini** ou **entropia/ganho de informação**);
2. divide os dados nesse ponto, criando ramos;
3. repete recursivamente em cada ramo até um critério de parada (profundidade máxima, mínimo de amostras por folha, folha pura);
4. cada folha recebe a classe majoritária; a predição percorre a árvore da raiz até a folha.

**c) MLP — Perceptron de Múltiplas Camadas (rede neural)** ⭐ *(algoritmo NÃO visto em aula)*

Rede neural *feedforward* treinada por retropropagação. Passos:
1. **Arquitetura:** camada de entrada (1 neurônio por atributo), uma ou mais **camadas ocultas** e camada de saída (probabilidade da classe);
2. **Inicialização** aleatória dos pesos e vieses;
3. **Propagação direta (forward):** cada neurônio calcula `z = Σ(wᵢ·xᵢ) + b` e aplica uma **função de ativação** (ReLU nas ocultas, logística na saída);
4. **Cálculo do erro** entre a saída prevista e a real por uma **função de perda** (entropia cruzada / log-loss);
5. **Retropropagação (backpropagation):** calcula o gradiente da perda em relação a cada peso, propagando o erro da saída para as camadas anteriores pela **regra da cadeia**;
6. **Atualização dos pesos** por um otimizador (**Adam**, padrão no scikit-learn), na direção que reduz a perda, controlada pela taxa de aprendizado;
7. **Repete** (forward + backprop) por várias épocas até convergir (`max_iter` ou tolerância).

### 2.5. Estratégia de divisão treino/teste

**Holdout estratificado 70% treino / 30% teste** (`train_test_split` com
`stratify` no atributo classe e `random_state=42`), preservando a proporção das
classes em ambos os conjuntos.

### 2.6. Medidas de avaliação e fórmulas

Sendo VP/VN = verdadeiros positivos/negativos e FP/FN = falsos positivos/negativos:

- **Acurácia** = (VP + VN) / (VP + VN + FP + FN)
- **Precisão** = VP / (VP + FP)
- **Recall (Revocação)** = VP / (VP + FN)
- **F1-score** = 2 · (Precisão · Recall) / (Precisão + Recall)
- **ROC-AUC** = área sob a curva ROC (Taxa de Verdadeiros Positivos × Taxa de Falsos Positivos em vários limiares)

> **Por que mais de uma métrica:** na base de fraude (desbalanceada) a **acurácia
> sozinha engana** — por isso F1 e ROC-AUC são os critérios principais de comparação.

### 2.7. Parametrizações testadas (≥2 por algoritmo)

| Algoritmo | Parametrização 1 | Parametrização 2 |
|-----------|------------------|------------------|
| **KNN** | K=3, voto uniforme | K=11, ponderado por distância |
| **Árvore** | critério Gini, profundidade máx. 5 | critério Entropia, profundidade ilimitada (mín. 5 amostras/folha) |
| **MLP** | 1 camada oculta (50 neurônios), ReLU | 2 camadas ocultas (100, 50), ReLU, α=0,001 |

---

## 3. Resultados

Métricas no conjunto de **teste** (holdout 70/30 estratificado). 🏆 = melhor da base.

### 3.1. Base Cardíaca (918 instâncias, balanceada)

| Algoritmo | Parametrização | Acurácia | Precisão | Recall | F1 | ROC-AUC |
|-----------|----------------|---------:|---------:|-------:|---:|--------:|
| **KNN** | **k=11, distância** | 0,880 | 0,900 | 0,882 | **0,891** 🏆 | **0,941** 🏆 |
| KNN | k=3, uniforme | 0,873 | 0,888 | 0,882 | 0,885 | 0,912 |
| MLP | 1 camada (50) | 0,851 | 0,868 | 0,863 | 0,866 | 0,917 |
| Árvore | entropy, prof. ilimitada | 0,812 | 0,848 | 0,804 | 0,826 | 0,882 |
| Árvore | gini, prof.=5 | 0,837 | 0,842 | 0,869 | 0,855 | 0,860 |
| MLP | 2 camadas (100,50) | 0,830 | 0,879 | 0,804 | 0,840 | 0,884 |

### 3.2. Base Fraude (178.542 instâncias após undersampling 5:1)

| Algoritmo | Parametrização | Acurácia | Precisão | Recall | F1 | ROC-AUC |
|-----------|----------------|---------:|---------:|-------:|---:|--------:|
| **MLP** | **1 camada (50)** | 0,968 | 0,916 | 0,888 | **0,902** 🏆 | **0,990** 🏆 |
| MLP | 2 camadas (100,50) | 0,964 | 0,890 | 0,892 | 0,891 | 0,988 |
| KNN | k=11, distância | 0,958 | 0,912 | 0,829 | 0,868 | 0,972 |
| KNN | k=3, uniforme | 0,955 | 0,889 | 0,836 | 0,862 | 0,951 |
| Árvore | entropy, prof. ilimitada | 0,956 | 0,885 | 0,842 | 0,863 | 0,950 |
| Árvore | gini, prof.=5 | 0,936 | 0,854 | 0,743 | 0,795 | 0,927 |

*(Fonte dos números: `resultados/resultados.csv` e `resultados/RELATORIO_resultados.md`.)*

---

## 4. Discussão dos Resultados

- **Melhor algoritmo em cada base:**
  - **Cardíaca → KNN (k=11, ponderado por distância):** F1 = 0,891 e ROC-AUC = 0,941.
  - **Fraude → MLP (1 camada oculta):** F1 = 0,902 e ROC-AUC = 0,990.

- **Algoritmo mais consistente nas duas bases:** o **KNN (k=11)** — foi o melhor na
  cardíaca e o 3º na fraude (ROC-AUC 0,972, muito próximo do topo). O **MLP** só se
  destacou na base **grande**.

- **Interpretação (tamanho da base importa):** na base **pequena** (918 exemplos),
  o **KNN** — simples e sem muitos parâmetros — superou o MLP, que tende a
  *overfitting*/subaproveitamento com poucos dados. Na base **grande** (≈178 mil), o
  **MLP** teve volume de dados suficiente para aprender fronteiras de decisão
  complexas e liderou. A **Árvore de Decisão** foi a mais fraca nas duas
  (embora competitiva na fraude com entropia e profundidade ilimitada).

- **Efeito da parametrização:** no KNN, **K maior (11) com voto ponderado** superou
  K=3 nas duas bases (mais robusto a ruído). No MLP, a rede **mais simples (1 camada)**
  superou a mais profunda — mais camadas não ajudaram e ainda custaram mais treino.

- **Métrica importa:** na fraude, a Árvore (gini) tem acurácia 0,936 mas F1 de apenas
  **0,795** — confirma que **acurácia isolada engana** em base desbalanceada.

- **Custo computacional:** KNN e Árvore treinam em **frações de segundo**; o MLP na
  fraude levou **~2 minutos** por configuração — um *trade-off* entre desempenho e custo.

### Tabela-resumo (melhor configuração por algoritmo, por base — critério F1)

| Base | KNN | Árvore | MLP | Vencedor |
|------|----:|-------:|----:|----------|
| Cardíaca (F1) | **0,891** | 0,855 | 0,866 | **KNN** |
| Fraude (F1) | 0,868 | 0,863 | **0,902** | **MLP** |

---

## 5. Uso de LLMs *(declaração obrigatória — enunciado item 2.e)*

> ⚠️ O enunciado exige declarar o uso de LLMs (qual, em que parte, e o prompt).
> Não declarar (ou usar sem citar) = nota zero.

**LLM utilizada:** Claude (modelo Opus 4.8), via a ferramenta **Claude Code**.

| Etapa do trabalho | Como a LLM foi usada | Prompt (resumo) |
|-------------------|----------------------|-----------------|
| Obtenção das bases | Baixar os datasets do Kaggle e converter para Parquet | "Baixe esse dataset e coloque no meu diretório" / "quero apenas o dataset em .parquet" |
| Escolha da 2ª base | Sugerir base de classificação fácil e adequada ao trabalho | "procure outro dataset fácil no Kaggle para meu trabalho universitário" |
| Exploração (etapa b) | Gerar o `explorar_dados.py` (perfil por coluna, cardinalidade) | "crie um código de escaneamento… métricas de qualidade por tipo… separar categóricos por baixa/média/alta cardinalidade" |
| Pré-processamento (etapa c) | Gerar `preprocessar.py` + `config_preprocessamento.yaml` | "pré-processamento diferente por algoritmo… z-score, tratar ausentes… yaml configurável (normalização, encoding, ausentes)" |
| Treino/avaliação (etapa d/e) | Gerar `treinar.py` + `config_modelos.yaml` e executar KNN, Árvore e MLP | "cria/pegue da internet os algoritmos KNN, MLP, Árvore de decisão para treinar nos dois datasets" |
| Organização | Consolidar os resultados neste documento de insumos | "consolida tudo no insumos_relatorio.md" |

> **Importante (regra do enunciado, item 3.b/3.e):** o código e os resultados
> precisam ser **compreendidos pelo grupo** antes da apresentação — a interpretação
> e o entendimento dos algoritmos são parte da avaliação. Este documento resume o
> raciocínio; revisem cada script antes da entrega/prova.

---

*Última atualização: etapas b, c, d e e concluídas — falta redigir o texto final e gerar o PDF.*
