"""
Mision 2 - Tarea 2.2: Matriz de Adyacencia Interactiva 15x15 (Plotly)
Top 15 paises por Trade_Connectivity_Index promedio.
Tooltip personalizado: 'Origen: X | Destino: Y | Volumen: Z'
"""
import numpy as np
import pandas as pd
import plotly.express as px

np.random.seed(7)

df = pd.read_csv('global_esg_risk.csv')

top15 = (
    df.groupby('Country')['Trade_Connectivity_Index']
      .mean()
      .nlargest(15)
      .index
      .tolist()
)
print('Top 15 paises por conectividad comercial:')
for i, c in enumerate(top15, 1):
    print(f'  {i:2d}. {c}')

# Simular matriz de adyacencia: volumen ~ promedio de conectividad de ambos
conn = df.groupby('Country')['Trade_Connectivity_Index'].mean()
gdp = df.groupby('Country')['GDP_Per_Capita'].mean()

n = 15
M = np.zeros((n, n))
for i, ci in enumerate(top15):
    for j, cj in enumerate(top15):
        if i == j:
            M[i, j] = 0  # autocomercio = 0
        else:
            base = (conn[ci] * conn[cj]) / 100  # 0..100
            scale = np.sqrt(gdp[ci] * gdp[cj]) / 1000  # 0..~60
            noise = np.random.uniform(0.7, 1.3)
            M[i, j] = round(base * scale * noise, 2)

# Construir tabla de origen-destino para custom_data
origen = np.array([[a for _ in top15] for a in top15])
destino = np.array([[b for b in top15] for _ in top15])

fig = px.imshow(
    M,
    x=top15,
    y=top15,
    color_continuous_scale='Viridis',
    aspect='equal',
    labels=dict(x='Pais destino', y='Pais origen', color='Volumen comercial'),
    title='Matriz de Adyacencia Comercial | Top 15 Paises por Conectividad',
)

# Tooltip personalizado con HTML
fig.update(data=[dict(
    customdata=np.dstack([origen, destino]),
    hovertemplate=(
        'Origen: <b>%{customdata[0]}</b><br>'
        'Destino: <b>%{customdata[1]}</b><br>'
        'Volumen: <b>%{z:.2f}</b>'
        '<extra></extra>'
    ),
)])

fig.update_layout(
    width=950, height=850,
    title_font=dict(size=18),
    coloraxis_colorbar=dict(title='Volumen<br>comercial<br>(simulado)'),
    xaxis=dict(tickangle=-45),
)

fig.write_html('matriz_adyacencia.html')
print('\nGuardado: matriz_adyacencia.html')
