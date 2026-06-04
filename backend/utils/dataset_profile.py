import pandas as pd

df = pd.read_csv("datasets/raw/IndianWeatherRepository.csv")

print("=" * 50)
print("DATASET PROFILE")
print("=" * 50)

print("\nShape")
print(df.shape)

print("\nData Types")
print(df.dtypes)

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

print("\nNumerical Statistics")
print(df.describe())

print("\nCategorical Statistics")
print(df.describe(include="string"))
