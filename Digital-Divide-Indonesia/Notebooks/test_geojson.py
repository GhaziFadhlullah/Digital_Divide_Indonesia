import json

with open(
    "Data/geojson/indonesia.geojson",
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)

print("Jumlah feature:", len(data["features"]))

print("\nProperties pertama:")
print(data["features"][0]["properties"])