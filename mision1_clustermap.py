"""
Mision 1 - Tarea 1.2: Clustermap Normalizado (Z-score) - Perfiles de Paises 2023
Identifica agrupaciones naturales con linkage 'ward' y normalizacion por columnas.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('global_esg_risk.csv')
df_2023 = df[df['Year'] == 2023].copy()

numeric_cols = [
    'CO2_Emissions_Per_Capita',
    'Average_Credit_Score_Corporate',
    'GDP_Per_Capita',
    'Trade_Connectivity_Index',
]

# Usar ISO_Code como indice (clustermap admite ~150 filas pero el yticklabels se ve apretado)
data = df_2023.set_index('ISO_Code')[numeric_cols]

g = sns.clustermap(
    data,
    z_score=1,                # normalizar columnas (Z-score por feature)
    method='ward',
    cmap='RdBu_r',
    center=0,
    figsize=(10, 22),
    yticklabels=True,
    xticklabels=True,
    cbar_kws={'label': 'Z-score (normalizado por columna)'},
    dendrogram_ratio=(0.12, 0.05),
)

g.ax_heatmap.set_xticklabels(
    g.ax_heatmap.get_xticklabels(), rotation=30, ha='right', fontsize=10,
)
g.ax_heatmap.tick_params(axis='y', labelsize=6)

g.fig.suptitle(
    'Clustermap Z-score 2023 | Perfiles ESG de 150 Paises\nLinkage: Ward  -  Distancia: Euclidiana',
    fontsize=14, fontweight='bold', y=1.00,
)

plt.savefig('clustermap_2023.png', dpi=300, bbox_inches='tight')
print('Guardado: clustermap_2023.png')

# Imprimir paises por cluster usando fcluster para soportar el analisis
from scipy.cluster.hierarchy import fcluster
import numpy as np

# Z-score manual para fcluster (sns ya lo hizo internamente pero no expone el linkage post-norm)
data_z = (data - data.mean()) / data.std()
from scipy.cluster.hierarchy import linkage
Z = linkage(data_z.values, method='ward')
clusters = fcluster(Z, t=4, criterion='maxclust')
out = pd.DataFrame({'ISO': data.index, 'Cluster': clusters})
out = out.merge(df_2023[['ISO_Code', 'Country'] + numeric_cols],
                left_on='ISO', right_on='ISO_Code')
print('\nResumen por cluster (4 grupos forzados):')
print(out.groupby('Cluster')[numeric_cols].mean().round(2))
print('\nEjemplos por cluster:')
for c in sorted(out['Cluster'].unique()):
    sample = out[out['Cluster'] == c]['Country'].head(5).tolist()
    print(f'  Cluster {c}: {sample}')
