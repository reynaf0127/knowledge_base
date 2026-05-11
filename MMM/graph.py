import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv('./MMM/data/merge_df.csv')
df['Date_'] = pd.to_datetime(df['Date_'])
# -------------
# overall trend
# -------------
fig, ax1 = plt.subplots(figsize=(10,6))
ax1.plot(df['Date_'], df['total_gmv_'], label='Total GMV', color='limegreen')
ax1.set_ylabel('Total GMV', color='limegreen')
ax2 = ax1.twinx()
ax2.plot(df['Date_'], df['total_units_'], label='Total Units', color='coral')
ax2.set_ylabel('Total Units', color='coral')
plt.show()
# -------------
# hist
# -------------
numeric_cols = df.select_dtypes(include=['number']).columns
n_col = 8
n_row = (len(numeric_cols) + n_col - 1) // n_col
fig, axes = plt.subplots(n_row, n_col, figsize=(5*n_col,4*n_row))
axes = axes.flatten()
for i, col in enumerate(numeric_cols):
    s = df[col].replace([np.inf,-np.inf],np.nan).dropna()
    if s.empty:
        axes[i].set_title(f'{col} (empty)')
        axes[i].axis('off')
        continue
    axes[i].boxplot(s, vert=True)
    axes[i].set_title(col)
for j in range(i+1, len(axes)):
    fig.delaxes(axes[j])
plt.tight_layout()
plt.show()
# -------------
# outlier
# -------------
upper = df['total_gmv_'].quantile(0.99)
df['total_gmv_'] = np.clip(df['total_gmv_'], None, upper)
df['log_gmv'] = np.log1p(df['total_gmv_'])
# -------------
# Seasonality
# -------------
df['date_month'] = df['Date_'].dt.to_period('M').astype(str)
monthly_bar = df.groupby('date_month')['total_gmv_'].sum().reset_index().sort_values('date_month')
monthly_bar['log_gmv'] = np.log1p(monthly_bar['total_gmv_'])
plt.figure(figsize=(10,6))
plt.bar(monthly_bar['date_month'],monthly_bar['log_gmv'],color='chocolate')
plt.show()
df['day_number'] = df['Date_'].dt.day
daynumber_bar = df.groupby('day_number')['total_gmv_'].sum().reset_index().sort_values('day_number')
daynumber_bar['log_gmv'] = np.log1p(daynumber_bar['total_gmv_'])
plt.figure(figsize=(10,6))
plt.bar(daynumber_bar['day_number'],daynumber_bar['log_gmv'],color='chocolate')
plt.show()