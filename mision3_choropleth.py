"""
Mision 3 - Tarea 3.1: Choropleth Map Animado (Plotly)
Evolucion de CO2_Emissions_Per_Capita por pais (2000-2023) con slider temporal.
"""
import pandas as pd
import plotly.express as px

df = pd.read_csv('global_esg_risk.csv')

# 1. Limpieza: cada ISO debe tener un registro por cada Year (sin huecos)
df_clean = df.dropna(subset=['ISO_Code', 'CO2_Emissions_Per_Capita']).copy()
expected = df_clean['ISO_Code'].nunique() * df_clean['Year'].nunique()
print(f'Registros esperados (ISO x Year): {expected}')
print(f'Registros reales: {len(df_clean)}')
assert expected == len(df_clean), 'Hay huecos en el panel ISO x Year'

# 2. Rango de color FIJO para que la escala sea consistente en todos los frames
co2_min = float(df_clean['CO2_Emissions_Per_Capita'].min())
co2_max = float(df_clean['CO2_Emissions_Per_Capita'].max())

fig = px.choropleth(
    df_clean.sort_values('Year'),
    locations='ISO_Code',
    locationmode='ISO-3',
    color='CO2_Emissions_Per_Capita',
    hover_name='Country',
    hover_data={'ISO_Code': True, 'Year': True,
                'CO2_Emissions_Per_Capita': ':.2f'},
    animation_frame='Year',
    color_continuous_scale='YlOrRd',
    range_color=(co2_min, co2_max),
    projection='natural earth',
    title='Evolucion Global de Emisiones de CO2 per Capita (2000-2023)',
    labels={'CO2_Emissions_Per_Capita': 'CO2 t/hab'},
)

fig.update_layout(
    width=1200, height=720,
    title_font=dict(size=20),
    coloraxis_colorbar=dict(
        title='CO2<br>(t per capita)',
        thickness=18,
    ),
    geo=dict(
        showframe=False, showcoastlines=True,
        coastlinecolor='gray', showland=True, landcolor='whitesmoke',
    ),
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        y=0, x=1.10, xanchor='right', yanchor='top',
        buttons=[dict(label='Play', method='animate',
                      args=[None, dict(frame=dict(duration=600, redraw=True),
                                       fromcurrent=True)])],
    )],
)

fig.write_html('choropleth_co2.html')
print('Guardado: choropleth_co2.html')
