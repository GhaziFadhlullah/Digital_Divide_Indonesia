import pandas as pd
import glob
import os

internet_data = []

files = sorted(glob.glob("Data/raw/internet/*.csv"))

for file in files:

    tahun = int(os.path.basename(file).split("_")[1].split(".")[0])

    print(f"Memproses {tahun}...")

    df = pd.read_csv(
        file,
        header=2
    )

    # Buang baris tahun
    df = df.iloc[1:]

    df = df[["Unnamed: 0", "Perkotaan+Perdesaan"]]

    df.columns = ["Provinsi", "Internet"]

    df["Provinsi"] = df["Provinsi"].astype(str).str.strip()

    df["Internet"] = pd.to_numeric(
        df["Internet"],
        errors="coerce"
    )

    df["Tahun"] = tahun

    internet_data.append(df)

internet = pd.concat(
    internet_data,
    ignore_index=True
)

internet.to_csv(
    "Data/processed/internet_all.csv",
    index=False
)

print("\n=== HASIL ===")
print(internet.head())
print(internet.shape)

print("\nJumlah per tahun:")
print(internet.groupby("Tahun").size())