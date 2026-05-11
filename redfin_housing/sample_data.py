import pandas as pd
import glob
files = glob.glob("./redfin_housing/data/*.parquet")
df = pd.concat([
    pd.read_parquet(file).sample(5000) for file in files
])

df.to_parquet("./redfin_housing/data/sample_data.parquet", index=False)
print('shape: ', df.shape)
df.info()
print('columns: ', df.columns)
df.describe()