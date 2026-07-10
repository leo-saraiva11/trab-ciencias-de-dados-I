# Resultados — Comparação de Classificadores (Etapa d/e)

Métricas calculadas no conjunto de **teste** (holdout 70/30 estratificado).
Cada algoritmo usou seu pré-processamento próprio (ver etapa c).

## Fórmulas das métricas

Sendo VP/VN/FP/FN = verdadeiros/falsos positivos/negativos:
- **Acurácia** = (VP+VN) / (VP+VN+FP+FN)
- **Precisão** = VP / (VP+FP)
- **Recall (Revocação)** = VP / (VP+FN)
- **F1-score** = 2 · (Precisão · Recall) / (Precisão + Recall)
- **ROC-AUC** = área sob a curva ROC (TPR × FPR em vários limiares)

## Base: heart

| Algoritmo | Parametrização | Acurácia | Precisão | Recall | F1 | ROC-AUC | Treino (s) |
|-----------|----------------|---------:|---------:|-------:|---:|--------:|-----------:|
| knn | k=3 (uniforme) | 0.873 | 0.888 | 0.882 | 0.885 | 0.912 | 0.00 |
| knn | k=11 (ponderado por distância) | 0.880 | 0.900 | 0.882 | 0.891 | 0.941 | 0.00 |
| arvore | gini, profundidade=5 | 0.837 | 0.842 | 0.869 | 0.855 | 0.860 | 0.00 |
| arvore | entropy, profundidade ilimitada | 0.812 | 0.848 | 0.804 | 0.826 | 0.882 | 0.00 |
| mlp | 1 camada oculta (50) | 0.851 | 0.868 | 0.863 | 0.866 | 0.917 | 0.33 |
| mlp | 2 camadas ocultas (100,50) | 0.830 | 0.879 | 0.804 | 0.840 | 0.884 | 0.63 |

- **Melhor F1:** knn (k=11 (ponderado por distância)) = 0.891
- **Melhor ROC-AUC:** knn (k=11 (ponderado por distância)) = 0.941

## Base: fraude

| Algoritmo | Parametrização | Acurácia | Precisão | Recall | F1 | ROC-AUC | Treino (s) |
|-----------|----------------|---------:|---------:|-------:|---:|--------:|-----------:|
| knn | k=3 (uniforme) | 0.955 | 0.889 | 0.836 | 0.862 | 0.951 | 0.21 |
| knn | k=11 (ponderado por distância) | 0.958 | 0.912 | 0.829 | 0.868 | 0.972 | 0.21 |
| arvore | gini, profundidade=5 | 0.936 | 0.854 | 0.743 | 0.795 | 0.927 | 0.20 |
| arvore | entropy, profundidade ilimitada | 0.956 | 0.885 | 0.842 | 0.863 | 0.950 | 0.39 |
| mlp | 1 camada oculta (50) | 0.968 | 0.916 | 0.888 | 0.902 | 0.990 | 128.51 |
| mlp | 2 camadas ocultas (100,50) | 0.964 | 0.890 | 0.892 | 0.891 | 0.988 | 114.40 |

- **Melhor F1:** mlp (1 camada oculta (50)) = 0.902
- **Melhor ROC-AUC:** mlp (1 camada oculta (50)) = 0.990
