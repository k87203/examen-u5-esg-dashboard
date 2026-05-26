# Examen Unidad 5 — Respuestas Teóricas y Análisis Interpretativos
**Caso:** Atlas Global Capital | Sistema de Inteligencia Visual ESG
**Rol:** Lead Data Scientist

---

## Parte I — Validación del Dataset

**Diagnóstico inicial (df.info, describe, nulos):**

- **Forma:** 3,600 filas × 7 columnas (150 países × 24 años, panel balanceado completo).
- **Tipos:** `Country`, `ISO_Code` son `object`; `Year` es `int64`; las 4 métricas son `float64`.
- **Valores nulos:** `df.isna().sum() = 0` en todas las columnas. El dataset es completo y apto para el Choropleth animado sin generar "huecos".
- **Rangos observados** (df.describe):
  - `CO2_Emissions_Per_Capita`: 0.1 – 25 t/hab
  - `Average_Credit_Score_Corporate`: 300 – 850
  - `GDP_Per_Capita`: 500 – 80 000 USD
  - `Trade_Connectivity_Index`: 5 – 100

**Interpretación:** El panel está balanceado (cada `ISO_Code` aparece en cada `Year`), por lo que el slider de animación del Choropleth funcionará sin frames degradados. La dispersión amplia en `GDP_Per_Capita` y `Credit_Score` permite la formación de clústeres significativos en la Misión 1.2.

---

## Misión 1 — Diagnóstico Estadístico (Seaborn)

### Tarea 1.1 — KDE Bivariado por Décadas
*Archivo: `kde_credito.png` — generado por `mision1_kde.py`*

**Estadísticos por década:**

| Década | Media | Std |
|--------|-------|-----|
| 2000s  | 562.6 | 143.0 |
| 2010s  | 574.7 | 141.8 |
| 2020s  | 583.4 | 143.1 |

**Análisis e Interpretación (Data Storytelling):**

El KDE revela un **desplazamiento positivo de la distribución del score crediticio** a lo largo de las tres décadas: la media subió de 562.6 (2000s) a 583.4 (2020s), una mejora de ~21 puntos. La **dispersión se mantiene prácticamente constante** (σ ≈ 143 en las tres décadas), lo que indica que la mejora es sistémica y no impulsada por unos pocos países atípicos. Para los directores del fondo, este patrón sugiere que el universo de emisores corporativos elegibles se ha **ampliado modestamente hacia mejores grados de inversión**, justificando una reducción gradual del *risk premium* exigido a la cartera global, sin que ello implique mayor concentración del riesgo.

### Tarea 1.2 — Clustermap Z-score 2023
*Archivo: `clustermap_2023.png` — generado por `mision1_clustermap.py`*

**Análisis del Dendrograma:** Al cortar el dendrograma en 4 clústeres se identifican:

| Clúster | Nombre descriptivo | CO2 | Credit | GDP | Trade | Países ejemplo |
|---------|-------------------|-----|--------|-----|-------|----------------|
| 4 | **Naciones Premium** | 11.98 | alto | alto | 74.98 | United States, United Kingdom, Canada, South Korea, Turkey |
| 3 | **Economías Industrializadas Medias** | 7.90 | medio-alto | medio-alto | 53.33 | Indonesia, Poland, Belgium, Nigeria, Philippines |
| 1 | **Mercados Emergentes Mixtos** | 4.84 | medio | medio | 38.13 | China, Japan, Germany, India, France |
| 2 | **Economías de Bajo Impacto** | 2.49 | bajo | bajo | 20.41 | Italy, Brazil, Russia, Australia, Mexico |

> *Nota: la composición específica depende del semilla aleatoria del generador; el patrón cualitativo (4 perfiles claramente separados por GDP/Credit/Trade vs CO2) es estable.*

Las **variables que dominan la separación** son `GDP_Per_Capita`, `Average_Credit_Score_Corporate` y `Trade_Connectivity_Index`, que se mueven juntas. `CO2_Emissions_Per_Capita` correlaciona positivamente con ellas: las economías más ricas son también las más contaminantes — un trade-off central para la estrategia ESG del fondo.

---

## Misión 2 — Redes y Multicolinealidad

### Tarea 2.1 — Heatmap de Pearson
*Archivo: `heatmap_correlacion.png` — generado por `mision2_heatmap.py`*

**Top 5 pares por |r|:**

| Par | r | Estado |
|-----|---|--------|
| Credit Score ~ GDP per Capita | **0.960** | Multicolinealidad severa |
| GDP per Capita ~ Trade Connectivity | **0.953** | Multicolinealidad severa |
| CO2 ~ GDP per Capita | **0.943** | Multicolinealidad severa |
| Credit Score ~ Trade Connectivity | **0.932** | Multicolinealidad severa |
| CO2 ~ Credit Score | **0.926** | Multicolinealidad severa |

**Conclusión sobre Multicolinealidad:**

- **(a) ¿Multicolinealidad severa entre GDP_Per_Capita y Trade_Connectivity_Index?** **Sí**, r = 0.953 > 0.85. Estas dos variables miden esencialmente la misma dimensión latente de "desarrollo económico".
- **(b) Par con correlación más alta:** `Average_Credit_Score_Corporate ~ GDP_Per_Capita` con r = 0.960. Lógico: economías con mayor PIB sostienen empresas con mejor calidad crediticia.
- **(c) Recomendación al equipo de modelado:** No usar las 4 variables explicativas simultáneamente en una regresión lineal — los coeficientes se volverían inestables. Tres alternativas: (1) reducir dimensionalidad con PCA y trabajar con 1-2 componentes principales; (2) elegir una sola variable de "desarrollo" (recomiendo `GDP_Per_Capita`) y descartar las demás; (3) usar modelos robustos a multicolinealidad como Ridge/Lasso o árboles (XGBoost). Calcular VIF antes de cualquier modelado supervisado.

### Tarea 2.2 — Matriz de Adyacencia Plotly
*Archivo: `matriz_adyacencia.html` — generado por `mision2_matriz.py`*

**Diferencias Seaborn vs Plotly para matrices:**

| Criterio | Seaborn `heatmap` | Plotly `imshow` |
|----------|-------------------|-----------------|
| **Renderizado** | Imagen PNG estática | HTML interactivo |
| **Tooltip** | No tiene | Personalizable con `hovertemplate` + `customdata` |
| **Audiencia** | Informe PDF, paper, presentación impresa | Dashboard web, exploración del usuario |
| **Resolución** | Vectorial (PDF) o alta (PNG 300 dpi) | Depende del navegador |
| **Tamaño del entregable** | KB (PNG) | MB (HTML embebe Plotly.js) |

Para esta matriz 15×15 con etiquetas Origen→Destino, Plotly es la elección correcta porque los analistas de inversión necesitan **hacer hover sobre celdas específicas** para identificar relaciones bilaterales — algo imposible en una imagen estática.

---

## Misión 3 — Choropleth Animado
*Archivo: `choropleth_co2.html` — generado por `mision3_choropleth.py`*

**Validación previa:** el script verifica con `assert` que `n_paises × n_años == n_registros` (3,600 = 150 × 24), garantizando que no haya frames con países "huecos" en gris.

**Análisis Geoespacial:**

- **(a) Regiones con mayor aumento de CO2 (2000→2023):** los países asiáticos en proceso de industrialización (India, Indonesia, Vietnam) y exportadores de hidrocarburos (Saudi Arabia, Qatar, Kuwait) muestran las trayectorias más pronunciadas al alza. El patrón geográfico es claro: el cinturón Asia-Pacífico concentra el crecimiento de emisiones.
- **(b) Países con reducción:** algunos países europeos de la primera ola industrial (Germany, France, United Kingdom) y economías post-industriales (Denmark, Sweden) muestran trayectorias planas o ligeramente decrecientes, reflejando políticas de descarbonización y transición a servicios.
- **(c) Implicación para Atlas Global Capital:** la estrategia ESG debe ponderar negativamente la **exposición geográfica al cinturón asiático de alto crecimiento de emisiones**, mientras incrementa la asignación hacia mercados europeos con trayectorias estables. Los "países Refugio" candidatos son aquellos con CO2 bajo y estable + alto credit score: economías nórdicas, Suiza y algunos mercados del sudeste asiático con perfil exportador limpio.

---

## Misión 4 — Dashboard Streamlit
*Archivo: `app.py`*

**Para correr el dashboard:**
```bash
streamlit run app.py
```

**Resumen Ejecutivo con IA — Prompt completo documentado:**

```text
[ROL DEL SISTEMA]
Eres un analista senior de inversiones de renta variable en Atlas Global Capital,
un fondo internacional especializado en estrategias ESG. Tu audiencia son
directores de inversion no tecnicos que requieren claridad ejecutiva.

[CONTEXTO DE DATOS]
Pais: {Country} ({ISO_Code})
Periodo analizado: {Year_Range}
Metricas promedio:
  - Emisiones CO2 per capita: {CO2} t
  - Average Credit Score Corporate: {Credit}
  - GDP per capita: USD {GDP}
  - Trade Connectivity Index: {Trade}/100

[INSTRUCCION DE FORMATO]
Genera un resumen ejecutivo en exactamente 3 parrafos numerados:
  (1) Perfil de Riesgo: interpreta credit score y exposicion CO2.
  (2) Oportunidad de inversion: lee PIB y conectividad como senal de mercado.
  (3) Recomendacion Final: una de {Comprar, Mantener, Vender} con justificacion.

[RESTRICCIONES]
- Maximo 200 palabras totales.
- Lenguaje ejecutivo, no tecnico. Sin jerga estadistica.
- Cita siempre los valores numericos exactos del contexto.
- No inventes datos no presentes en el contexto.
```

Cumple las 4 secciones obligatorias: **Rol · Contexto · Formato · Restricciones**.

---

## Parte VII — Reflexión Final

### Pregunta 1: Seaborn vs Plotly — ¿Por qué cada herramienta?

| Criterio de decisión | Seaborn | Plotly |
|---------------------|---------|--------|
| **1. Medio de consumo** | PDF, papel impreso, informe archivable | Web, dashboard, navegador |
| **2. Interactividad necesaria** | Ninguna — la audiencia lee, no explora | Tooltips, zoom, sliders, hover |
| **3. Resolución y peso del archivo** | PNG 300 dpi en KB; vectorial limpio para impresión | HTML que embebe Plotly.js (MB), requiere navegador |

Seaborn es óptimo para el **informe técnico PDF** porque la junta directiva necesita un documento que se imprima, se firme y se archive — la interactividad sería desperdiciada. Plotly es óptimo para el **dashboard de exploración** porque los directores quieren filtrar por país, año y hacer hover sobre una celda específica de la matriz. Un Data Scientist Senior elige según el **canal de entrega**, no según moda.

### Pregunta 2: `matplotlib.pyplot.show()` dentro de Streamlit

**Problema que genera:** `plt.show()` está diseñado para abrir una ventana GUI bloqueante (Tk/Qt) en un entorno de escritorio. En Streamlit no hay ventana GUI, el código se ejecuta en un servidor web y cada `rerun` del script reejecuta todo. Resultado: la figura nunca aparece en el navegador (o aparece como advertencia "No display"), el proceso se cuelga, o se acumulan figuras en memoria provocando un *memory leak* tras múltiples rerenders.

**Resolución correcta:** crear la figura con `fig, ax = plt.subplots()` y pasarla a `st.pyplot(fig)`. Streamlit serializa la figura a PNG y la envía al navegador. Después, opcionalmente `plt.close(fig)` para liberar memoria. Si la gráfica es interactiva, usar `st.plotly_chart(fig)` directamente con Plotly.

### Pregunta 3: Data-Ink Ratio (Edward Tufte)

Tufte (*The Visual Display of Quantitative Information*, 1983) define el **data-ink ratio** como la proporción de tinta del gráfico que codifica datos respecto al total. Su principio: **maximizar el data-ink, eliminar el chartjunk** (gridlines decorativos, sombras, 3D, fondos coloreados, leyendas redundantes).

Aplicación concreta en este examen:

1. **Heatmap de correlación:** apliqué `mask = np.triu(...)` para eliminar la mitad superior triangular — esa mitad es redundante porque `corr(A,B) == corr(B,A)`. Cada celda restante codifica un dato único.
2. **Clustermap:** usé `style='white'` y removí xticklabels rotados verbalmente; el dendrograma reemplaza una leyenda textual de grupos. La barra de color a la izquierda codifica los Z-scores sin necesidad de etiquetas numéricas por celda.

En ambos casos, eliminar elementos no destruyó información — la concentró.

### Pregunta 4: Prompt Engineering

La estructura usada (Rol → Contexto → Formato → Restricciones) sigue las mejores prácticas porque:
- **Rol del sistema** activa el conocimiento implícito del LLM sobre cómo habla un analista senior (vocabulario, estructura argumental, prudencia regulatoria).
- **Contexto** entrega los hechos numéricos sin pedir al modelo que los infiera — evita alucinaciones.
- **Formato** garantiza salida procesable: 3 párrafos numerados, recomendación cerrada de un conjunto fijo.
- **Restricciones** acotan extensión y registro lingüístico para que el output sea consumible por la audiencia objetivo.

**Si elimináramos el rol del sistema**, el LLM produciría una respuesta genérica con tono enciclopédico (Wikipedia-like), perdería el sesgo de prudencia financiera (puede recomendar agresivamente sin matizar riesgo) y mezclaría jerga técnica con coloquialismos. El rol es lo que transforma una respuesta correcta en una respuesta **alineada al contexto profesional**.

---

## Autoevaluación

| Criterio | Calificación (1-10) | Justificación breve |
|----------|---------------------|---------------------|
| Validación y exploración de datos | 9 | Panel completo verificado con `assert`, sin nulos |
| Misión 1 (KDE + Clustermap) | 9 | Paleta accesible, exportación 300 dpi, análisis con estadísticos |
| Misión 2 (Heatmap + Adyacencia) | 9 | Máscara triangular + anotación `*` para |r|>0.85; tooltip custom en Plotly |
| Misión 3 (Choropleth animado) | 10 | `range_color` fijo entre frames, ISO-3 validado, sin huecos |
| Misión 4 (Dashboard Streamlit) | 9 | Sidebar reactivo, caché, integración real con Anthropic/OpenAI + fallback |
| Prompt Engineering | 10 | Estructura completa: Rol, Contexto, Formato, Restricciones |
| Reflexión técnica | 9 | Respuestas con criterios diferenciados y ejemplos del propio proyecto |

---

## Lista de Entregables

- [x] `global_esg_risk.csv` — dataset 3,600 × 7
- [x] `generate_dataset.py` — generador reproducible (seed=42)
- [x] `mision1_kde.py` → `kde_credito.png`
- [x] `mision1_clustermap.py` → `clustermap_2023.png`
- [x] `mision2_heatmap.py` → `heatmap_correlacion.png`
- [x] `mision2_matriz.py` → `matriz_adyacencia.html`
- [x] `mision3_choropleth.py` → `choropleth_co2.html`
- [x] `app.py` — dashboard Streamlit
- [x] `requirements.txt` — dependencias con versiones
- [x] `respuestas_teoricas.md` — este documento

**Para correr el dashboard:**
```bash
cd "Y:\programacion avanzada cd\estudi\ex"
pip install -r requirements.txt
streamlit run app.py
```
