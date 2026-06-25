import os
import pandas as pd
import json
import glob
import plotly.express as px

# =========================
# BASE PATH
# =========================
BASE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

# =========================
# LOAD DATA
# =========================
csv_path = os.path.join(
    BASE,
    "Data",
    "processed",
    "digital_divide_clean.csv"
)

df = pd.read_csv(csv_path)

# =========================
# CLEAN DATA
# =========================
df = df[df["Provinsi"].astype(str).str.upper() != "INDONESIA"]

df["Provinsi"] = (
    df["Provinsi"]
    .astype(str)
    .str.upper()
    .str.strip()
)

# =========================
# MATCH DENGAN GEOJSON
# =========================
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

# =========================
# LOAD GEOJSON
# =========================
geo_folder = os.path.join(BASE, "Data", "geojson")
geo_file = glob.glob(
    os.path.join(geo_folder, "*.geojson")
)[0]

with open(geo_file, "r", encoding="utf-8") as f:
    geo = json.load(f)

# =========================
# DEBUG
# =========================
geo_names = sorted([
    x["properties"]["state"]
    for x in geo["features"]
])

print("\n=== GEOJSON STATES ===")
print(geo_names)

# =========================
# AGGREGATE
# =========================
df_map = (
    df.groupby("Provinsi", as_index=False)
      .mean(numeric_only=True)
)

print("\n=== CSV STATES ===")
print(sorted(df_map["Provinsi"].unique()))

print("\n=== MISSING IN GEOJSON ===")
print(
    set(df_map["Provinsi"].unique()) -
    set(geo_names)
)

print("\n=== MISSING IN CSV ===")
print(
    set(geo_names) -
    set(df_map["Provinsi"].unique())
)

# =========================
# CHOROPLETH
# =========================
fig = px.choropleth(
    df_map,
    geojson=geo,
    locations="Provinsi",
    featureidkey="properties.state",
    color="Internet",
    hover_name="Provinsi",
    color_continuous_scale="Blues",
    title="Digital Divide Indonesia (Internet Access)"
)

fig.update_geos(
    fitbounds="locations",
    visible=False
)

fig.update_layout(
    margin=dict(l=0, r=0, t=60, b=0)
)

# =========================
# SAVE HTML
# =========================
output_html = os.path.join(
    BASE,
    "Data",
    "digital_divide_map.html"
)

fig.write_html(output_html)

print("\n✔ MAP CREATED")
print(output_html)

# =========================
# SHOW
# =========================
fig.show()