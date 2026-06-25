import os
import pandas as pd

print("🔥 SCRIPT MULAI JALAN")

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
print("BASE:", BASE)

csv_path = os.path.join(BASE, "Data", "processed", "digital_divide_clean.csv")
print("CSV PATH:", csv_path)

df = pd.read_csv(csv_path)

print("\n✔ DATA LOADED")
print(df.head())

print("\n✔ KOLOM:")
print(df.columns)