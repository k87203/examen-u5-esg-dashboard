"""
Mision 1 - Tarea 1.1: KDE Bivariado por decadas
Distribucion de Average_Credit_Score_Corporate por decada (2000s/2010s/2020s)
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('global_esg_risk.csv')

def decade_label(y):
    if y < 2010:
        return '2000s'
    if y < 2020:
        return '2010s'
    return '2020s'

df['Decade'] = df['Year'].apply(decade_label)

# Estadisticos por decada para anotacion
stats = df.groupby('Decade')['Average_Credit_Score_Corporate'].agg(['mean', 'std']).round(1)

sns.set_theme(style='whitegrid', context='talk')
fig, ax = plt.subplots(figsize=(12, 7))

sns.kdeplot(
    data=df,
    x='Average_Credit_Score_Corporate',
    hue='Decade',
    fill=True,
    common_norm=False,
    alpha=0.4,
    linewidth=2,
    palette='colorblind',
    ax=ax,
)

ax.set_title(
    'Evolucion del Riesgo Crediticio Corporativo Global por Decada',
    fontsize=16, fontweight='bold', pad=15,
)
ax.set_xlabel('Average Credit Score Corporate', fontsize=13)
ax.set_ylabel('Densidad estimada (KDE)', fontsize=13)

# Annotation box con conclusion estadistica
text = (
    'Media | Std por decada\n'
    f"2000s: {stats.loc['2000s','mean']} | {stats.loc['2000s','std']}\n"
    f"2010s: {stats.loc['2010s','mean']} | {stats.loc['2010s','std']}\n"
    f"2020s: {stats.loc['2020s','mean']} | {stats.loc['2020s','std']}\n"
    'Tendencia: mejora del score con el tiempo\n(menor riesgo de impago corporativo)'
)
ax.text(
    0.02, 0.97, text,
    transform=ax.transAxes,
    fontsize=11, verticalalignment='top',
    bbox=dict(boxstyle='round,pad=0.6', facecolor='white', edgecolor='gray', alpha=0.9),
)

plt.tight_layout()
plt.savefig('kde_credito.png', dpi=300, bbox_inches='tight')
print('Guardado: kde_credito.png')
print('\nEstadisticos por decada:')
print(stats)
