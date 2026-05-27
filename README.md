# Examen Unidad 5 — Sistema de Inteligencia Visual ESG

**Caso:** Atlas Global Capital | Análisis ESG y Riesgo de Cadena de Suministro
**Materia:** Programación Avanzada para Ciencia de Datos
**Carrera:** Ingeniería en Ciencia de Datos — Instituto Tecnológico de Tláhuac III

Dashboard interactivo que identifica países "Refugio" (bajo riesgo financiero, alta conectividad comercial, métricas ambientales estables) a partir de un dataset multinivel de 150 países × 24 años (2000-2023).

## Estructura del proyecto

| Archivo | Descripción |
|---|---|
| `app.py` | Dashboard Streamlit integrado con módulo IA |
| `examen_u5_esg.ipynb` | Notebook con las 4 misiones (KDE, Clustermap, Heatmap, Matriz adyacencia, Choropleth animado) |
| `global_esg_risk.csv` | Dataset multinivel 150 países × 24 años |
| `requirements.txt` | Dependencias |
| `runtime.txt` | Python 3.11 para Streamlit Cloud |

## Cómo correr el dashboard

```bash
pip install -r requirements.txt
streamlit run app.py
```

Abrir `http://localhost:8501` en el navegador.

## Dashboard desplegado

https://examen-u5-esg-dashboard-a9hhrlhxytb9lwsumjmhbp.streamlit.app/

## Stack técnico

- **Seaborn + Matplotlib** — gráficos estáticos de alta resolución (300 dpi)
- **Plotly Express** — visualizaciones interactivas (matriz adyacencia + choropleth animado)
- **Streamlit** — dashboard web con filtros reactivos y caché
- **Anthropic / OpenAI SDK** — módulo de IA para resúmenes ejecutivos (con fallback simulado)

## Misiones implementadas

1. **Diagnóstico estadístico** — KDE multivariable por décadas + Clustermap Z-score con linkage Ward
2. **Análisis de redes y multicolinealidad** — Heatmap Pearson con anotación de pares |r|>0.85 + Matriz adyacencia con tooltips personalizados
3. **Visualización geoespacial animada** — Choropleth mundial con slider temporal y rango de color fijo
4. **Dashboard + IA** — Streamlit con sidebar interactivo + Prompt Engineering estructurado (Rol/Contexto/Formato/Restricciones)
