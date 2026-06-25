import streamlit as st
import pandas as pd
import json
import os
import glob
import plotly.express as px
import folium
from streamlit_folium import st_folium

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Digital Divide Indonesia",
    layout="wide"
)

st.markdown("""
<style>

[data-testid="stSidebar"]{
    background-color:#0f172a;
}

[data-testid="stSidebar"] label{
    color:white !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p{
    color:white;
}

[data-testid="metric-container"]{
    background:#1e293b;
    border:1px solid #334155;
    padding:10px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# PATH
# ==================================================

BASE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

csv_path = os.path.join(
    BASE,
    "Data",
    "processed",
    "digital_divide_clean.csv"
)

geo_folder = os.path.join(
    BASE,
    "Data",
    "geojson"
)

geo_file = glob.glob(
    os.path.join(geo_folder, "*.geojson")
)[0]

# ==================================================
# LOAD DATA
# ==================================================

df = pd.read_csv(csv_path)

with open(geo_file, encoding="utf-8") as f:
    geo = json.load(f)

# ==================================================
# CLEAN DATA
# ==================================================

df = df[df["Provinsi"] != "INDONESIA"]

mapping = {
    "DKI JAKARTA": "Jakarta Raya",
    "DI YOGYAKARTA": "Yogyakarta",
    "KEP. RIAU": "Kepulauan Riau",
    "KEP. BANGKA BELITUNG": "Bangka-Belitung",

    "ACEH": "Aceh",
    "SUMATERA UTARA": "Sumatera Utara",
    "SUMATERA BARAT": "Sumatera Barat",
    "RIAU": "Riau",
    "JAMBI": "Jambi",
    "SUMATERA SELATAN": "Sumatera Selatan",
    "BENGKULU": "Bengkulu",
    "LAMPUNG": "Lampung",

    "JAWA BARAT": "Jawa Barat",
    "JAWA TENGAH": "Jawa Tengah",
    "JAWA TIMUR": "Jawa Timur",
    "BANTEN": "Banten",

    "BALI": "Bali",
    "NUSA TENGGARA BARAT": "Nusa Tenggara Barat",
    "NUSA TENGGARA TIMUR": "Nusa Tenggara Timur",

    "KALIMANTAN BARAT": "Kalimantan Barat",
    "KALIMANTAN TENGAH": "Kalimantan Tengah",
    "KALIMANTAN SELATAN": "Kalimantan Selatan",
    "KALIMANTAN TIMUR": "Kalimantan Timur",
    "KALIMANTAN UTARA": "Kalimantan Utara",

    "SULAWESI UTARA": "Sulawesi Utara",
    "GORONTALO": "Gorontalo",
    "SULAWESI TENGAH": "Sulawesi Tengah",
    "SULAWESI BARAT": "Sulawesi Barat",
    "SULAWESI SELATAN": "Sulawesi Selatan",
    "SULAWESI TENGGARA": "Sulawesi Tenggara",

    "MALUKU": "Maluku",
    "MALUKU UTARA": "Maluku Utara",

    "PAPUA": "Papua",
    "PAPUA BARAT": "Papua Barat"
}

df["Provinsi"] = df["Provinsi"].replace(mapping)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("Digital Divide Indonesia")

    st.markdown("---")

    st.subheader("Filter Data")

    tahun = st.selectbox(
        "Tahun",
        sorted(df["Tahun"].unique())
    )

    indikator = st.selectbox(
        "Indikator",
        ["Internet", "Komputer"]
    )

    st.markdown("---")

    st.subheader("Informasi")

    st.info(
        """
        Dashboard ini menampilkan
        tingkat kesenjangan digital
        antar provinsi di Indonesia.
        """
    )
# ==================================================
# FILTER DATA
# ==================================================

df_year = df[df["Tahun"] == tahun]

# ==================================================
# KPI
# ==================================================

rata2 = df_year[indikator].mean()

max_idx = df_year[indikator].idxmax()
min_idx = df_year[indikator].idxmin()

prov_max = df_year.loc[max_idx, "Provinsi"]
prov_min = df_year.loc[min_idx, "Provinsi"]

nilai_max = df_year.loc[max_idx, indikator]
nilai_min = df_year.loc[min_idx, indikator]

gap = nilai_max - nilai_min

# ==================================================
# SIDEBAR STATISTIK
# ==================================================

with st.sidebar:

    st.subheader("Statistik Nasional")

    st.metric(
        "Rata-rata",
        f"{rata2:.2f}%"
    )

    st.metric(
        "Tertinggi",
        prov_max
    )

    st.metric(
        "Terendah",
        prov_min
    )

    st.metric(
        "Gap Digital",
        f"{gap:.2f}%"
    )

    st.metric(
        "Jumlah Provinsi",
        len(df_year)
    )
# ==================================================
# HEADER
# ==================================================

st.title("Dashboard Digital Divide Indonesia")

st.markdown(
    f"Analisis kesenjangan digital Indonesia berdasarkan **{indikator}** pada tahun **{tahun}**"
)

# ==================================================
# KPI CARDS
# ==================================================

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Rata-rata Nasional",
    f"{rata2:.2f}%"
)

k2.metric(
    "Provinsi Tertinggi",
    prov_max,
    f"{nilai_max:.2f}%"
)

k3.metric(
    "Provinsi Terendah",
    prov_min,
    f"{nilai_min:.2f}%"
)

k4.metric(
    "Gap Digital",
    f"{gap:.2f}%"
)

# ==================================================
# PETA INTERAKTIF
# ==================================================

st.subheader("Peta Sebaran Indonesia")

nilai_dict = dict(
    zip(
        df_year["Provinsi"],
        df_year[indikator]
    )
)

for feature in geo["features"]:

    provinsi = feature["properties"]["state"]

    feature["properties"]["nilai"] = round(
        nilai_dict.get(provinsi, 0),
        2
    )

m = folium.Map(
    location=[-2.5, 118],
    zoom_start=5,
    tiles="CartoDB Dark_Matter",
    control_scale=True
)

folium.Choropleth(
    geo_data=geo,
    data=df_year,
    columns=["Provinsi", indikator],
    key_on="feature.properties.state",
    fill_color="RdYlGn",
    fill_opacity=0.9,
    line_opacity=1,
    line_color="white",
    legend_name=f"{indikator} (%)"
).add_to(m)

folium.GeoJson(
    geo,
    style_function=lambda x: {
        "fillOpacity": 0,
        "color": "white",
        "weight": 1
    },
    tooltip=folium.GeoJsonTooltip(
        fields=[
            "state",
            "nilai"
        ],
        aliases=[
            "Provinsi",
            f"{indikator} (%)"
        ],
        sticky=True,
        labels=True,
        style="""
            background-color: #1e293b;
            color: white;
            border: 2px solid #38bdf8;
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
        """
    )
).add_to(m)

folium.LayerControl().add_to(m)

st_folium(
    m,
    width=None,
    height=750
)
# ==================================================
# TOP 5 & BOTTOM 5
# ==================================================

top5 = (
    df_year
    .sort_values(indikator, ascending=False)
    .head(5)
)

bottom5 = (
    df_year
    .sort_values(indikator)
    .head(5)
)

c1, c2 = st.columns(2)

with c1:

    st.subheader("Top 5 Provinsi Tertinggi")

    fig_top = px.bar(
        top5.sort_values(indikator),
    x=indikator,
    y="Provinsi",
    orientation="h",
    text=indikator,
    color_discrete_sequence=["#22c55e"]
    )

    fig_top.update_layout(height=450)

    st.plotly_chart(
        fig_top,
        width="stretch"
    )

with c2:

    st.subheader("Top 5 Provinsi Terendah")

    fig_bottom = px.bar(
         bottom5.sort_values(indikator),
    x=indikator,
    y="Provinsi",
    orientation="h",
    text=indikator,
    color_discrete_sequence=["#ef4444"]
    )

    fig_bottom.update_layout(height=450)

    st.plotly_chart(
        fig_bottom,
        width="stretch"
    )

# ==================================================
# RANKING NASIONAL
# ==================================================

st.subheader("Ranking Seluruh Provinsi")

ranking = (
    df_year
    .sort_values(indikator, ascending=False)
    .reset_index(drop=True)
)

ranking.index += 1

st.dataframe(
    ranking[
        ["Provinsi", indikator]
    ],
    width="stretch",
    height=500
)

# ==================================================
# TREN NASIONAL
# ==================================================

st.subheader("Tren Nasional 2015–2024")

trend = (
    df.groupby("Tahun")[["Internet", "Komputer"]]
    .mean()
    .reset_index()
)

fig_trend = px.line(
    trend,
    x="Tahun",
    y=["Internet", "Komputer"],
    markers=True
)

fig_trend.update_layout(
    height=500
)

st.plotly_chart(
    fig_trend,
    width="stretch"
)

