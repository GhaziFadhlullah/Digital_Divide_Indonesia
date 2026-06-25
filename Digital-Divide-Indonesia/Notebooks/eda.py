from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    BASE_DIR / "Data" / "processed" / "digital_divide_clean.csv"
)

print(df.head())