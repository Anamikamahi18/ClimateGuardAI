import pandas as pd

df = pd.read_csv("datasets/processed/climate_anomalies.csv")

cols = ["air_quality_us-epa-index", "air_quality_gb-defra-index"]

print(df[cols].describe())

print("\nUnique EPA")
print(sorted(df["air_quality_us-epa-index"].unique()))

print("\nUnique DEFRA")
print(sorted(df["air_quality_gb-defra-index"].unique()))

importance_features = ["air_quality_us-epa-index", "air_quality_gb-defra-index"]

for feature in importance_features:
    print(feature)
