import pandas as pd

df = pd.read_csv("Data/processed/digital_divide.csv")

missing = df[
    df["Internet"].isna() |
    df["Komputer"].isna()
]

print(missing)

missing.to_csv(
    "Data/processed/missing_data.csv",
    index=False
)