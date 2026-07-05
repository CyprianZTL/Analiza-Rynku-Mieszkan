import pandas as pd

df = pd.read_json("data/mieszkania.json")

print(df.head(1).T)