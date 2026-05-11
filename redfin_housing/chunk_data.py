import pandas as pd
from pathlib import Path

file_path = "./redfin_housing/city_market_tracker.tsv000"
output_dir = Path("./redfin_housing/data")
output_dir.mkdir(parents=True, exist_ok=True)
chunksize = 200_000
for i, chunk in enumerate(pd.read_csv(file_path, sep="\t", chunksize=chunksize)):
    chunk.to_parquet(
        output_dir / f"part_{i:04d}.parquet",
        index=False
    )
    print(f"Saved chunk {i}, shape={chunk.shape}")