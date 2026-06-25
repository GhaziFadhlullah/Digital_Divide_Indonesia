import pandas as pd

# Load dataset hasil merge
internet = pd.read_csv(
    "Data/processed/internet_all.csv"
)

komputer = pd.read_csv(
    "Data/processed/komputer_all.csv"
)

# Bersihkan nama provinsi
internet["Provinsi"] = (
    internet["Provinsi"]
    .astype(str)
    .str.strip()
    .str.upper()
)

komputer["Provinsi"] = (
    komputer["Provinsi"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Pastikan tipe tahun sama
internet["Tahun"] = internet["Tahun"].astype(int)
komputer["Tahun"] = komputer["Tahun"].astype(int)

# Merge
digital_divide = pd.merge(
    internet,
    komputer,
    on=["Provinsi", "Tahun"],
    how="inner"
)

# Simpan
digital_divide.to_csv(
    "Data/processed/digital_divide.csv",
    index=False
)

print("\n=== HASIL MERGE ===")
print(digital_divide.head())

print("\nShape:")
print(digital_divide.shape)

print("\nJumlah Provinsi:")
print(digital_divide["Provinsi"].nunique())

print("\nRentang Tahun:")
print(
    digital_divide["Tahun"].min(),
    "-",
    digital_divide["Tahun"].max()
)

print("\nMissing Value:")
print(digital_divide.isnull().sum())