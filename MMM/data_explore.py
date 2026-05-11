import pandas as pd

# -------------
# Media investment
# -------------
mediainvestment = pd.read_csv('./MMM/data/MediaInvestment.csv')
mediainvestment['Date'] = pd.to_datetime(mediainvestment[['Year', 'Month']].assign(day=1))
values = [
    'Total Investment', 'TV', 'Digital', 'Sponsorship', 'Content Marketing', 'Online marketing', ' Affiliates', 'SEM', 'Radio', 'Other'
]
mediainvestment['days_in_month'] = mediainvestment['Date'].dt.days_in_month
mediainvestment_daily = mediainvestment.loc[mediainvestment.index.repeat(mediainvestment['days_in_month'])].copy()
mediainvestment_daily['day_number'] = mediainvestment_daily.groupby('Date').cumcount()
mediainvestment_daily['date_daily'] = mediainvestment_daily['Date'] + pd.to_timedelta(mediainvestment_daily['day_number'],unit='D')
for col in values:
    mediainvestment_daily[col] = mediainvestment_daily[col] / mediainvestment_daily['days_in_month']
mediainvestment_daily.columns = (
    mediainvestment_daily.columns.str.strip()
    .str.lower()
    .str.replace(' ','_')
) 
# -------------
# Sales
# -------------
sales = pd.read_csv('./MMM/data/Sales.csv', sep='\t')
sales['Date'] = pd.to_datetime(sales['Date']).dt.date
sales['GMV'] = sales['GMV'].str.replace(' ','')
sales['GMV'] = pd.to_numeric(sales['GMV'], errors='coerce')
sales_group = sales.groupby(['Date','Analytic_Category']).agg(
    gmv=('GMV','sum'),
    units=('Units_sold','sum'),
    mrp=('MRP','sum')
).reset_index()
sales_group_pivot = pd.pivot_table(
    sales_group, 
    index='Date', 
    columns='Analytic_Category',
    values=['gmv','units','mrp'], 
    aggfunc='sum', 
    fill_value=0).reset_index()
sales_group_pivot['total_gmv'] = sales_group_pivot['gmv'].sum(axis=1)
sales_group_pivot['total_units'] = sales_group_pivot['units'].sum(axis=1)
sales_group_pivot['total_mrp'] = sales_group_pivot['mrp'].sum(axis=1)
sales_group_pivot['total_discount'] = sales_group_pivot['total_gmv'] / sales_group_pivot['total_mrp']
for col in sales_group_pivot['gmv'].columns:
    sales_group_pivot[('discount',col)] = (
        sales_group_pivot[('gmv',col)] / sales_group_pivot[('mrp',col)]
    )
sales_group_pivot.columns = [
    '_'.join(col).strip() if isinstance(col, tuple) else col for col in sales_group_pivot.columns
]
sales_group_pivot['Date_'] = pd.to_datetime(sales_group_pivot['Date_'])
# -------------
# Special Sales
# -------------
special_sale = pd.read_csv('./MMM/data/SpecialSale.csv')
special_sale['Date'] = pd.to_datetime(special_sale['Date'])
special_sale_pivot = pd.pivot_table(
    special_sale,
    index='Date',
    columns='Sales Name',
    fill_value=0,
    aggfunc='size'
).reset_index()
special_sale_pivot.columns = (
    special_sale_pivot.columns.str.strip()
    .str.lower()
    .str.replace(r"[ &-']","_",regex=True)
)
# -------------
# aggregate data
# -------------
merge_df = sales_group_pivot.merge(mediainvestment_daily, left_on='Date_', right_on='date_daily', how='left').merge(special_sale_pivot, left_on='Date_',right_on='date', how='left')
merge_df.to_csv('./MMM/data/merge_df.csv', index=False)