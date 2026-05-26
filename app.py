"""
Atlas Global Capital | Sistema de Inteligencia ESG
Dashboard Streamlit - Examen Unidad 5

Estructura:
  - Sidebar: slider rango anos + selectbox riesgo + boton reset
  - Main:
      1. KPIs ejecutivos
      2. Choropleth animado de CO2 (Mision 3)
      3. Matriz de adyacencia 15x15 (Mision 2)
      4. Boton "Generar Resumen Ejecutivo con IA" (Mision 4.3)
"""
import os
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# =========================================================================
# Configuracion de pagina
# =========================================================================
st.set_page_config(
    layout='wide',
    page_title='Atlas Global Capital | ESG Dashboard',
    page_icon='ATL',
)

# =========================================================================
# Carga de datos (cacheada)
# =========================================================================
@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv('global_esg_risk.csv')


df = load_data()

# =========================================================================
# Sidebar: filtros dinamicos
# =========================================================================
st.sidebar.title('Filtros de Inversion')
st.sidebar.caption('Atlas Global Capital | Lead Data Scientist')

YEAR_MIN, YEAR_MAX = int(df['Year'].min()), int(df['Year'].max())

# Boton reset (debe ir ANTES de los widgets para limpiar session_state)
if st.sidebar.button('Restablecer filtros'):
    for k in ('year_range', 'risk_level', 'country_sel'):
        st.session_state.pop(k, None)
    st.rerun()

year_range = st.sidebar.slider(
    'Rango de Anos',
    min_value=YEAR_MIN, max_value=YEAR_MAX,
    value=(YEAR_MIN, YEAR_MAX),
    step=1,
    key='year_range',
)

risk_level = st.sidebar.selectbox(
    'Nivel de Riesgo Crediticio',
    options=['Todos', 'Alto (>700)', 'Medio (500-700)', 'Bajo (<500)'],
    key='risk_level',
)

# Logica de filtrado
mask = (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
if risk_level == 'Alto (>700)':
    mask &= df['Average_Credit_Score_Corporate'] > 700
elif risk_level == 'Medio (500-700)':
    mask &= df['Average_Credit_Score_Corporate'].between(500, 700)
elif risk_level == 'Bajo (<500)':
    mask &= df['Average_Credit_Score_Corporate'] < 500

df_f = df.loc[mask].copy()

st.sidebar.divider()
st.sidebar.metric('Registros filtrados', f'{len(df_f):,}')
st.sidebar.metric('Paises en seleccion', df_f['Country'].nunique())

# =========================================================================
# MAIN: Dashboard
# =========================================================================
st.title('Atlas Global Capital | Sistema de Inteligencia ESG')
st.markdown(
    'Dashboard para identificar **paises Refugio**: bajo riesgo financiero, '
    'alta conectividad comercial y metricas ambientales estables.'
)

# --- KPIs ejecutivos ---
c1, c2, c3, c4 = st.columns(4)
c1.metric('CO2 promedio (t/hab)',
          f"{df_f['CO2_Emissions_Per_Capita'].mean():.2f}")
c2.metric('Credit Score promedio',
          f"{df_f['Average_Credit_Score_Corporate'].mean():.0f}")
c3.metric('PIB per capita promedio',
          f"${df_f['GDP_Per_Capita'].mean():,.0f}")
c4.metric('Conectividad promedio',
          f"{df_f['Trade_Connectivity_Index'].mean():.1f}")

st.divider()

# --- Choropleth animado (Mision 3) ---
st.subheader('Mapa Coropleta Animado | Emisiones de CO2 per Capita')
co2_min = float(df['CO2_Emissions_Per_Capita'].min())
co2_max = float(df['CO2_Emissions_Per_Capita'].max())

fig_map = px.choropleth(
    df_f.sort_values('Year'),
    locations='ISO_Code', locationmode='ISO-3',
    color='CO2_Emissions_Per_Capita',
    hover_name='Country',
    animation_frame='Year',
    color_continuous_scale='YlOrRd',
    range_color=(co2_min, co2_max),
    projection='natural earth',
    labels={'CO2_Emissions_Per_Capita': 'CO2 t/hab'},
)
fig_map.update_layout(height=600, margin=dict(l=0, r=0, t=20, b=0))
st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# --- Matriz de adyacencia (Mision 2) ---
st.subheader('Matriz de Adyacencia Comercial | Top 15 por Conectividad')

@st.cache_data
def build_adjacency(_df: pd.DataFrame) -> tuple[np.ndarray, list[str]]:
    np.random.seed(7)
    top15 = (_df.groupby('Country')['Trade_Connectivity_Index']
                .mean().nlargest(15).index.tolist())
    conn = _df.groupby('Country')['Trade_Connectivity_Index'].mean()
    gdp = _df.groupby('Country')['GDP_Per_Capita'].mean()
    n = len(top15)
    M = np.zeros((n, n))
    for i, ci in enumerate(top15):
        for j, cj in enumerate(top15):
            if i == j:
                continue
            base = (conn[ci] * conn[cj]) / 100
            scale = np.sqrt(gdp[ci] * gdp[cj]) / 1000
            M[i, j] = round(base * scale * np.random.uniform(0.7, 1.3), 2)
    return M, top15


if len(df_f) < 100:
    st.warning('Pocos registros tras filtrar; la matriz puede no ser representativa.')

M, top15 = build_adjacency(df_f if len(df_f) > 0 else df)
origen = np.array([[a for _ in top15] for a in top15])
destino = np.array([[b for b in top15] for _ in top15])

fig_adj = px.imshow(
    M, x=top15, y=top15,
    color_continuous_scale='Viridis', aspect='equal',
    labels=dict(x='Pais destino', y='Pais origen', color='Volumen'),
)
fig_adj.update(data=[dict(
    customdata=np.dstack([origen, destino]),
    hovertemplate=(
        'Origen: <b>%{customdata[0]}</b><br>'
        'Destino: <b>%{customdata[1]}</b><br>'
        'Volumen: <b>%{z:.2f}</b><extra></extra>'
    ),
)])
fig_adj.update_layout(height=700, xaxis=dict(tickangle=-45))
st.plotly_chart(fig_adj, use_container_width=True)

st.divider()

# =========================================================================
# Modulo de IA: Resumen Ejecutivo
# =========================================================================
st.subheader('Resumen Ejecutivo con IA')

country_options = sorted(df_f['Country'].unique()) if len(df_f) else sorted(df['Country'].unique())
selected_country = st.selectbox(
    'Pais a analizar',
    options=country_options,
    key='country_sel',
)

# Datos del pais seleccionado (promedio en el rango filtrado)
country_df = df_f[df_f['Country'] == selected_country]
if len(country_df) == 0:
    country_df = df[df['Country'] == selected_country]

country_data = {
    'Country': selected_country,
    'ISO_Code': country_df['ISO_Code'].iloc[0],
    'Year_Range': f'{year_range[0]}-{year_range[1]}',
    'CO2_Emissions_Per_Capita': round(country_df['CO2_Emissions_Per_Capita'].mean(), 2),
    'Average_Credit_Score_Corporate': round(country_df['Average_Credit_Score_Corporate'].mean(), 0),
    'GDP_Per_Capita': round(country_df['GDP_Per_Capita'].mean(), 0),
    'Trade_Connectivity_Index': round(country_df['Trade_Connectivity_Index'].mean(), 1),
}


def build_prompt(data: dict) -> str:
    """
    Prompt estructurado segun mejores practicas de Prompt Engineering:
    (1) Rol del sistema  (2) Contexto de datos
    (3) Formato de salida (4) Restricciones
    """
    return f"""
[ROL DEL SISTEMA]
Eres un analista senior de inversiones de renta variable en Atlas Global Capital,
un fondo internacional especializado en estrategias ESG. Tu audiencia son
directores de inversion no tecnicos que requieren claridad ejecutiva.

[CONTEXTO DE DATOS]
Pais: {data['Country']} ({data['ISO_Code']})
Periodo analizado: {data['Year_Range']}
Metricas promedio:
  - Emisiones CO2 per capita: {data['CO2_Emissions_Per_Capita']} t
  - Average Credit Score Corporate: {data['Average_Credit_Score_Corporate']}
  - GDP per capita: USD {data['GDP_Per_Capita']:,}
  - Trade Connectivity Index: {data['Trade_Connectivity_Index']}/100

[INSTRUCCION DE FORMATO]
Genera un resumen ejecutivo en exactamente 3 parrafos numerados:
  (1) Perfil de Riesgo: interpreta credit score y exposicion CO2.
  (2) Oportunidad de inversion: lee PIB y conectividad como senal de mercado.
  (3) Recomendacion Final: una de {{Comprar, Mantener, Vender}} con justificacion.

[RESTRICCIONES]
- Maximo 200 palabras totales.
- Lenguaje ejecutivo, no tecnico. Sin jerga estadistica.
- Cita siempre los valores numericos exactos del contexto.
- No inventes datos no presentes en el contexto.
""".strip()


def simulate_summary(data: dict) -> str:
    """Fallback determinista cuando no hay API key disponible."""
    credit = data['Average_Credit_Score_Corporate']
    co2 = data['CO2_Emissions_Per_Capita']
    gdp = data['GDP_Per_Capita']
    trade = data['Trade_Connectivity_Index']

    risk = ('bajo' if credit > 700 else
            'moderado' if credit > 500 else 'elevado')
    rec = ('Comprar' if credit > 650 and trade > 60 else
           'Mantener' if credit > 500 else 'Vender')

    return f"""
**(1) Perfil de Riesgo.** {data['Country']} presenta un score crediticio promedio
de {credit:.0f}, equivalente a un nivel de riesgo {risk} para emisores corporativos.
Sus emisiones de {co2:.2f} t CO2/hab senalan la exposicion ambiental relativa
del mercado local; este factor pesa en la calificacion ESG del fondo.

**(2) Oportunidad de Inversion.** Con un PIB per capita de USD {gdp:,.0f} y un
indice de conectividad comercial de {trade:.1f}/100, el pais ofrece un perfil
de mercado consistente con el universo de inversion de Atlas. La conectividad
comercial es la palanca clave para identificar paises 'Refugio'.

**(3) Recomendacion Final: {rec}.** Combinando solidez crediticia, integracion
comercial y huella ambiental, la posicion sugerida es '{rec}' para el horizonte
{data['Year_Range']}, con revision trimestral del score crediticio.
""".strip()


def call_llm(prompt: str) -> str | None:
    """
    Intenta llamar a un LLM real si hay credenciales disponibles.
    Soporta tanto OpenAI como Anthropic. Retorna None si no hay API key.
    """
    # Opcion A: Anthropic (Claude)
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if api_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            msg = client.messages.create(
                model='claude-sonnet-4-5',
                max_tokens=600,
                messages=[{'role': 'user', 'content': prompt}],
            )
            return msg.content[0].text
        except Exception as e:
            st.warning(f'Anthropic fallo: {e}. Usando simulacion.')

    # Opcion B: OpenAI
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{'role': 'user', 'content': prompt}],
                max_tokens=600,
            )
            return resp.choices[0].message.content
        except Exception as e:
            st.warning(f'OpenAI fallo: {e}. Usando simulacion.')

    return None


def generate_executive_summary(country_data: dict) -> str:
    """Genera resumen ejecutivo via LLM, o fallback simulado."""
    prompt = build_prompt(country_data)
    real = call_llm(prompt)
    return real if real is not None else simulate_summary(country_data)


col_left, col_right = st.columns([2, 1])

with col_right:
    st.markdown('**Datos del pais seleccionado**')
    st.json(country_data)

with col_left:
    if st.button('Generar Resumen Ejecutivo con IA', type='primary'):
        with st.spinner('Analizando datos con el modelo...'):
            summary = generate_executive_summary(country_data)
        st.markdown(summary)

    with st.expander('Ver prompt enviado al modelo (Prompt Engineering)'):
        st.code(build_prompt(country_data), language='text')

st.divider()
st.caption(
    'Atlas Global Capital | Sistema de Inteligencia ESG  -  '
    'Examen Unidad 5: Visualizacion de Datos Avanzada'
)
