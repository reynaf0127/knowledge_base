import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_parquet("./redfin_housing/data/sample_data.parquet")

# -----------
# trend
# -----------
df['PERIOD_BEGIN'] = pd.to_datetime(df['PERIOD_BEGIN'])
groupdf = df.groupby('PERIOD_BEGIN').agg(
    median_sale=('MEDIAN_SALE_PRICE', 'mean'),
    home_sold=('HOMES_SOLD', 'sum')
    )
fig, ax1 = plt.subplots(figsize=(12,6))
ax1.plot(groupdf.index,groupdf['median_sale'],color='blue',label='Median Sale Price')
ax1.set_ylabel('Median Sale Price', color='blue')
ax2 = ax1.twinx()
ax2.plot(groupdf.index,groupdf['home_sold'],color='limegreen',label='Home Sold')
ax2.set_ylabel('Home Sold', color='limegreen')
plt.title('Median Sale Price and Home Sold Over Time')
plt.show()
# -----------
# top cities
# -----------
df[df['PERIOD_BEGIN']>=pd.to_datetime('2022-01-01')].groupby('CITY')['MEDIAN_SALE_PRICE'].mean().sort_values(ascending=False).head(20).plot(kind='barh', figsize=(8,10), color='coral')
plt.show()