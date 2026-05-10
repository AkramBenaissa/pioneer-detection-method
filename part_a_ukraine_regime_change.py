import pandas as pd

df = pd.read_csv("Official hrivnya exchange rates.csv")
print(df.head())
print(df.columns)
print(df.dtypes)
print(df.tail())