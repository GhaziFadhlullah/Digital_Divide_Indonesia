import pandas as pd

df = pd.read_csv(
    "Data/processed/digital_divide.csv"
)

papua_baru = [
    "PAPUA BARAT DAYA",
    "PAPUA SELATAN",
    "PAPUA TENGAH",
    "PAPUA PEGUNUNGAN"
]

df = df[
    ~df["Provinsi"].isin(papua_baru)
]

df.to_csv(
    "Data/processed/digital_divide_clean.csv",
    index=False
)

print(df.shape)
print(df.isnull().sum())