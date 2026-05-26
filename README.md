# Examen Unidad 5 — Sistema de Inteligencia Visual ESG

**Caso:** Atlas Global Capital | Análisis ESG y Riesgo de Cadena de Suministro
**Materia:** Programación Avanzada para Ciencia de Datos
**Carrera:** Ingeniería en Ciencia de Datos — Instituto Tecnológico de Tláhuac III

Dashboard interactivo que identifica países "Refugio" (bajo riesgo financiero, alta conectividad comercial, métricas ambientales estables) a partir de un dataset multinivel de 150 países × 24 años (2000-2023).

## Estructura del proyecto

| Archivo | Descripción |
|---|---|
| `generate_dataset.py` | Genera `global_esg_risk.csv` con 150 países ISO-3 reales |
| `mision1_kde.py` | KDE bivariado por décadas → `kde_credito.png` |
| `mision1_clustermap.py` | Clustermap Z-score 2023 → `clustermap_2023.png` |
| `mision2_heatmap.py` | Heatmap Pearson + máscara triangular → `heatmap_correlacion.png` |
| `mision2_matriz.py` | Matriz adyacencia 15×15 interactiva → `matriz_adyacencia.html` |
| `mision3_choropleth.py` | Choropleth animado CO2 (2000-2023) → `choropleth_co2.html` |
| `app.py` | Dashboard Streamlit integrado con módulo IA |
| `requirements.txt` | Dependencias |
| `respuestas_teoricas.md` | Análisis interpretativos y reflexión técnica |

## Cómo correr el dashboard

```bash
pip install -r requirements.txt
streamlit run app.py
```

Abrir `http://localhost:8501` en el navegador.

## Stack técnico

- **Seaborn + Matplotlib** — gráficos estáticos de alta resolución (300 dpi) para informe PDF
- **Plotly Express** — visualizaciones interactivas (matriz adyacencia + choropleth animado)
- **Streamlit** — dashboard web con filtros reactivos y caché
- **Anthropic / OpenAI SDK** — módulo de IA para resúmenes ejecutivos (con fallback simulado)

## Misiones implementadas

1. **Diagnóstico estadístico** — KDE multivariable por décadas + Clustermap Z-score con linkage Ward
2. **Análisis de redes y multicolinealidad** — Heatmap Pearson con anotación de pares \|r\|>0.85 + Matriz adyacencia con tooltips personalizados
3. **Visualización geoespacial animada** — Choropleth mundial con slider temporal y rango de color fijo
4. **Dashboard + IA** — Streamlit con sidebar interactivo + Prompt Engineering estructurado (Rol/Contexto/Formato/Restricciones)
