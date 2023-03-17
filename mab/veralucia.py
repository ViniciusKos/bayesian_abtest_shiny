import pandas as pd
df = pd.concat( [ pd.read_csv(f"../bayesian_abtest/data_collected_{i}.csv") for i in ["red","blue"] ] )
print(df.head())