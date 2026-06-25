import pandas as pd
import glob
import os

komputer_data = []

files = sorted(glob.glob("Data/raw/komputer/*.csv"))

for file in files:

    tahun = int(os.path.basename(file).split("_")[1].split(".")[0])

    print(f"Memproses {tahun}...")

    df = pd.read_csv(
        file,
        header=2
    )

    df = df.iloc[1:]

    df = df[["Unnamed: 0", "Perkotaan+Perdesaan"]]

    df.columns = ["Provinsi", "Komputer"]

    df["Provinsi"] = df["Provinsi"].astype(str).str.strip()

    df["Komputer"] = pd.to_numeric(
        df["Komputer"],
        errors="coerce"
    )

    df["Tahun"] = tahun

    komputer_data.append(df)

komputer = pd.concat(
    komputer_data,
    ignore_index=True
)

komputer.to_csv(
    "Data/processed/komputer_all.csv",
    index=False
)

print("\n=== HASIL ===")
print(komputer.head())
print(komputer.shape)

print("\nJumlah per tahun:")
print(komputer.groupby("Tahun").size())