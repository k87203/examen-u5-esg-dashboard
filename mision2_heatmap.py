"""
Mision 2 - Tarea 2.1: Heatmap de Correlacion de Pearson (Seaborn)
Mascara triangular superior + anotacion de pares con |r| > 0.85.
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('global_esg_risk.csv')

numeric_cols = [
    'CO2_Emissions_Per_Capita',
    'Average_Credit_Score_Corporate',
    'GDP_Per_Capita',
    'Trade_Connectivity_Index',
    'Year',
]

corr = df[numeric_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))

sns.set_theme(style='white', context='talk')
fig, ax = plt.subplots(figsize=(11, 9))

sns.heatmap(
    corr,
    mask=mask,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    vmin=-1, vmax=1, center=0,
    square=True,
    linewidths=0.5,
    cbar_kws={'shrink': 0.75, 'label': 'Coeficiente de Pearson'},
    ax=ax,
)

# Sobre-anotacion: agrega '*' a celdas con |r| > 0.85 (sin alterar fmt='.2f')
for i in range(corr.shape[0]):
    for j in range(corr.shape[1]):
        if mask[i, j] or i == j:
            continue
        if abs(corr.iat[i, j]) > 0.85:
            ax.text(
                j + 0.5, i + 0.78, '*',
                ha='center', va='center',
                color='black', fontsize=22, fontweight='bold',
            )

ax.set_title(
    'Matriz de Correlacion de Pearson | Variables ESG Globales\n* = multicolinealidad severa (|r| > 0.85)',
    fontsize=14, fontweight='bold', pad=15,
)
plt.xticks(rotation=30, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('heatmap_correlacion.png', dpi=300, bbox_inches='tight')
print('Guardado: heatmap_correlacion.png')
print('\nMatriz de correlacion:')
print(corr.round(3))

# Identificar el par con mayor correlacion absoluta (excluyendo diagonal)
pairs = []
for i in range(len(corr)):
    for j in range(i + 1, len(corr)):
        pairs.append((corr.index[i], corr.columns[j], corr.iat[i, j]))
pairs.sort(key=lambda x: abs(x[2]), reverse=True)
print('\nTop 5 pares por |correlacion|:')
for a, b, v in pairs[:5]:
    flag = '  <-- MULTICOLINEALIDAD' if abs(v) > 0.85 else ''
    print(f'  {a} ~ {b}: r = {v:.3f}{flag}')
