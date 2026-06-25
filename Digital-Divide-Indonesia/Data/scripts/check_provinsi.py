import os
import pandas as pd
import json
import glob

# =========================
# BASE PROJECT (AMAN)
# =========================
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# =========================
# LOAD CSV
# =========================
csv_path = os.path.join(BASE, "Data", "processed", "digital_divide_clean.csv")
df = pd.read_csv(csv_path)

print("\n✔ DATA LOADED")
print(df.head())

# =========================
# CLEAN COLUMN NAME
# =========================
prov_col = [c for c in df.columns if "prov" in c.lower()][0]

# remove noise
df = df[df[prov_col].astype(str).str.upper() != "INDONESIA"]

# =========================
# LOAD GEOJSON (AUTO DETECT FILE)
# =========================
geo_folder = os.path.join(BASE, "Data", "geojson")
geo_file = glob.glob(os.path.join(geo_folder, "*.geojson"))[0]

print("\nGEO FILE:", geo_file)

with open(geo_file, encoding="utf-8") as f:
    geo = json.load(f)

# =========================
# EXTRACT GEO PROVINCE
# =========================
geo_prov = []

for feature in geo["features"]:
    props = feature["properties"]

    name = (
        props.get("name") or
        props.get("state") or
        props.get("NAME_1") or
        props.get("provinsi")
    )

    if name:
        geo_prov.append(name.upper().strip())

geo_prov = sorted(set(geo_prov))

# =========================
# NORMALIZE CSV
# =========================
df["prov_clean"] = df[prov_col].astype(str).str.upper().str.strip()

# =========================
# FINAL MAPPING INDONESIA FIX
# =========================
mapping = {
    # Jakarta
    "DKI JAKARTA": "JAKARTA RAYA",
    "JAKARTA RAYA": "JAKARTA RAYA",

    # Yogyakarta
    "DI YOGYAKARTA": "YOGYAKARTA",
    "YOGYAKARTA": "YOGYAKARTA",

    # Kepulauan Riau
    "KEP. RIAU": "KEPULAUAN RIAU",
    "KEPULAUAN RIAU": "KEPULAUAN RIAU",

    # Bangka Belitung
    "KEP. BANGKA BELITUNG": "BANGKA-BELITUNG",
    "BANGKA-BELITUNG": "BANGKA-BELITUNG",
}

df["prov_clean"] = df["prov_clean"].replace(mapping)

# =========================
# FINAL UNIQUE LIST
# =========================
csv_prov = sorted(df["prov_clean"].unique())

# =========================
# COMPARE
# =========================
print("\n=== PROVINSI CSV (CLEAN) ===")
print(csv_prov)

print("\n=== PROVINSI GEOJSON ===")
print(geo_prov)

missing_geo = set(csv_prov) - set(geo_prov)
missing_csv = set(geo_prov) - set(csv_prov)

print("\n=== MISSING DI GEOJSON ===")
print(missing_geo)

print("\n=== MISSING DI CSV ===")
print(missing_csv)

print("\n=== SUMMARY ===")
print("CSV:", len(csv_prov))
print("GEO:", len(geo_prov))
print("Missing Geo:", len(missing_geo))
print("Missing CSV:", len(missing_csv))