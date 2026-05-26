"""
Generador del dataset global_esg_risk.csv
Atlas Global Capital | Examen Unidad 5

Crea 150 paises con codigos ISO-3 reales (no inventados) y 24 anos de datos
(2000-2023) para que el Choropleth animado no tenga huecos.

Se introduce correlacion intencional entre variables para que el heatmap
de Pearson tenga senal real y el clustermap forme grupos interpretables:
    - GDP_Per_Capita y Average_Credit_Score_Corporate: correlacion positiva
    - GDP_Per_Capita y Trade_Connectivity_Index: correlacion positiva
    - GDP_Per_Capita y CO2_Emissions_Per_Capita: correlacion positiva moderada
"""
import numpy as np
import pandas as pd

np.random.seed(42)

# 150 paises con codigos ISO 3166-1 alpha-3 reales
COUNTRIES = [
    ('United States', 'USA'), ('China', 'CHN'), ('Japan', 'JPN'),
    ('Germany', 'DEU'), ('India', 'IND'), ('United Kingdom', 'GBR'),
    ('France', 'FRA'), ('Italy', 'ITA'), ('Brazil', 'BRA'),
    ('Canada', 'CAN'), ('Russia', 'RUS'), ('South Korea', 'KOR'),
    ('Australia', 'AUS'), ('Spain', 'ESP'), ('Mexico', 'MEX'),
    ('Indonesia', 'IDN'), ('Netherlands', 'NLD'), ('Saudi Arabia', 'SAU'),
    ('Turkey', 'TUR'), ('Switzerland', 'CHE'), ('Poland', 'POL'),
    ('Sweden', 'SWE'), ('Belgium', 'BEL'), ('Argentina', 'ARG'),
    ('Thailand', 'THA'), ('Ireland', 'IRL'), ('Norway', 'NOR'),
    ('Austria', 'AUT'), ('Israel', 'ISR'), ('Nigeria', 'NGA'),
    ('Egypt', 'EGY'), ('South Africa', 'ZAF'), ('Denmark', 'DNK'),
    ('Singapore', 'SGP'), ('Philippines', 'PHL'), ('Malaysia', 'MYS'),
    ('Vietnam', 'VNM'), ('Bangladesh', 'BGD'), ('Chile', 'CHL'),
    ('Finland', 'FIN'), ('Romania', 'ROU'), ('Czech Republic', 'CZE'),
    ('Portugal', 'PRT'), ('New Zealand', 'NZL'), ('Peru', 'PER'),
    ('Greece', 'GRC'), ('Iraq', 'IRQ'), ('Algeria', 'DZA'),
    ('Qatar', 'QAT'), ('Kazakhstan', 'KAZ'), ('Hungary', 'HUN'),
    ('Ukraine', 'UKR'), ('Kuwait', 'KWT'), ('Morocco', 'MAR'),
    ('Ecuador', 'ECU'), ('Slovakia', 'SVK'), ('Sri Lanka', 'LKA'),
    ('Ethiopia', 'ETH'), ('Dominican Republic', 'DOM'), ('Kenya', 'KEN'),
    ('Guatemala', 'GTM'), ('Oman', 'OMN'), ('Bulgaria', 'BGR'),
    ('Venezuela', 'VEN'), ('Belarus', 'BLR'), ('Costa Rica', 'CRI'),
    ('Croatia', 'HRV'), ('Lithuania', 'LTU'), ('Uruguay', 'URY'),
    ('Slovenia', 'SVN'), ('Tunisia', 'TUN'), ('Panama', 'PAN'),
    ('Ghana', 'GHA'), ('Serbia', 'SRB'), ('Lebanon', 'LBN'),
    ('Azerbaijan', 'AZE'), ('Tanzania', 'TZA'), ('Belarus', 'BLR2'),
    ('Bolivia', 'BOL'), ('Paraguay', 'PRY'), ('Latvia', 'LVA'),
    ('Estonia', 'EST'), ('Bahrain', 'BHR'), ('Iceland', 'ISL'),
    ('Cyprus', 'CYP'), ('Jordan', 'JOR'), ('Honduras', 'HND'),
    ('Cambodia', 'KHM'), ('Senegal', 'SEN'), ('Uganda', 'UGA'),
    ('Zambia', 'ZMB'), ('Albania', 'ALB'), ('Mongolia', 'MNG'),
    ('Armenia', 'ARM'), ('Georgia', 'GEO'), ('Mozambique', 'MOZ'),
    ('Madagascar', 'MDG'), ('Cameroon', 'CMR'), ('Angola', 'AGO'),
    ('Nepal', 'NPL'), ('Myanmar', 'MMR'), ('Yemen', 'YEM'),
    ('Afghanistan', 'AFG'), ('Sudan', 'SDN'), ('North Macedonia', 'MKD'),
    ('Moldova', 'MDA'), ('Mauritius', 'MUS'), ('Malta', 'MLT'),
    ('Luxembourg', 'LUX'), ('Trinidad and Tobago', 'TTO'),
    ('Jamaica', 'JAM'), ('Botswana', 'BWA'), ('Namibia', 'NAM'),
    ('Gabon', 'GAB'), ('Mali', 'MLI'), ('Burkina Faso', 'BFA'),
    ('Niger', 'NER'), ('Rwanda', 'RWA'), ('Malawi', 'MWI'),
    ('Zimbabwe', 'ZWE'), ('Tajikistan', 'TJK'), ('Kyrgyzstan', 'KGZ'),
    ('Turkmenistan', 'TKM'), ('Uzbekistan', 'UZB'), ('Laos', 'LAO'),
    ('Papua New Guinea', 'PNG'), ('Fiji', 'FJI'), ('Brunei', 'BRN'),
    ('Bhutan', 'BTN'), ('Maldives', 'MDV'), ('Bahamas', 'BHS'),
    ('Barbados', 'BRB'), ('Belize', 'BLZ'), ('Suriname', 'SUR'),
    ('Guyana', 'GUY'), ('Cape Verde', 'CPV'), ('Comoros', 'COM'),
    ('Djibouti', 'DJI'), ('Eritrea', 'ERI'), ('Lesotho', 'LSO'),
    ('Eswatini', 'SWZ'), ('Liberia', 'LBR'), ('Sierra Leone', 'SLE'),
    ('Burundi', 'BDI'), ('Central African Republic', 'CAF'),
    ('Chad', 'TCD'), ('Republic of the Congo', 'COG'),
    ('Democratic Republic of the Congo', 'COD'), ('Guinea', 'GIN'),
    ('Guinea-Bissau', 'GNB'), ('Equatorial Guinea', 'GNQ'),
    ('Mauritania', 'MRT'), ('Somalia', 'SOM'), ('South Sudan', 'SSD'),
    ('Togo', 'TGO'), ('Benin', 'BEN'),
]

# Eliminar duplicado de Belarus (puse BLR2 como filler)
COUNTRIES = [c for c in COUNTRIES if c[1] != 'BLR2']
# Aseguramos 150 exactos: si faltan, agregamos islas; si sobran, recortamos
EXTRA = [('Saint Lucia', 'LCA'), ('Grenada', 'GRD'), ('Tonga', 'TON'),
         ('Samoa', 'WSM'), ('Vanuatu', 'VUT')]
for c in EXTRA:
    if len(COUNTRIES) < 150:
        COUNTRIES.append(c)
COUNTRIES = COUNTRIES[:150]

YEARS = list(range(2000, 2024))

# Perfil economico base por pais (latent variable que correlaciona variables)
# Distribuye paises en niveles: desarrollado (alto) | emergente (medio) | bajo
n = len(COUNTRIES)
base_wealth = np.concatenate([
    np.random.uniform(0.75, 1.00, size=40),   # desarrollados
    np.random.uniform(0.35, 0.75, size=60),   # emergentes
    np.random.uniform(0.05, 0.35, size=50),   # bajos ingresos
])
np.random.shuffle(base_wealth)

records = []
for idx, (country, iso) in enumerate(COUNTRIES):
    w = base_wealth[idx]  # 0..1
    for year in YEARS:
        # Tendencia temporal: leve crecimiento de PIB y reduccion de credit risk
        t = (year - 2000) / 23  # 0..1
        noise = lambda s: np.random.normal(0, s)

        gdp = 800 + w * 62000 + t * 4000 + noise(2500)
        gdp = float(np.clip(gdp, 500, 80000))

        # Credit score correlaciona positivo con riqueza, mejora con el tiempo
        credit = 300 + w * 500 + t * 30 + noise(35)
        credit = float(np.clip(credit, 300, 850))

        # CO2 correlaciona positivo con riqueza (industrializacion)
        co2 = 0.3 + w * 14 + noise(1.2)
        co2 = float(np.clip(co2, 0.1, 25))

        # Trade connectivity correlaciona positivo con riqueza
        trade = 10 + w * 80 + noise(6)
        trade = float(np.clip(trade, 5, 100))

        records.append({
            'Country': country,
            'ISO_Code': iso,
            'Year': year,
            'CO2_Emissions_Per_Capita': round(co2, 3),
            'Average_Credit_Score_Corporate': round(credit, 2),
            'GDP_Per_Capita': round(gdp, 2),
            'Trade_Connectivity_Index': round(trade, 2),
        })

df = pd.DataFrame(records)
df.to_csv('global_esg_risk.csv', index=False)
print(f'Dataset generado: {len(df)} filas x {len(df.columns)} columnas')
print(f'Paises unicos: {df["Country"].nunique()}')
print(f'Anos: {df["Year"].min()} - {df["Year"].max()}')
print('\nPrimeras filas:')
print(df.head())
print('\nResumen estadistico:')
print(df.describe())
