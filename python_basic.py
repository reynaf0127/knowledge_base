"""
Python practice sheet

How to use this file:
- Treat it as a learning notebook in `.py` form.
- Run one section at a time instead of running the whole file.
- Most examples assume the DataFrames already exist.

Main ideas in this file:
- Core pandas operations for data analysis
- Common "SQL-like" operations in Python
- Window-style calculations
- Practical matplotlib chart examples and customization
"""

import itertools

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ============================================================
# 1. LOAD AND INSPECT DATA
# Knowledge:
# - `pd.read_csv()` loads a CSV into a DataFrame.
# - `head()`, `info()`, `shape`, and `columns` help you inspect structure.
# ============================================================

df = pd.read_csv("file.csv")

df.head()
df.info()
df.shape
df.columns

result = pd.DataFrame(
    {
        "total_customers": [df["customer_id"].count()],
        "average_amount": [df["amount"].mean()],
    }
)


# ============================================================
# 2. SELECT AND FILTER ROWS
# Knowledge:
# - `df["col"]` selects one column.
# - `df[["col1", "col2"]]` selects multiple columns.
# - Boolean masks filter rows.
# - `isin()` checks membership.
# - `str.contains()` is useful for text filtering.
# - `query()` can feel similar to SQL WHERE.
# ============================================================

df["col"]
df[["col1", "col2"]]
df[df["revenue"] > 100]
df[df["country"].isin(["US", "CA"])]
df[df["name"].str.contains("unity", case=False, na=False)]
df.query("revenue > 100 and country == 'US'")

# "Not in" filter: `~` reverses a boolean condition.
result = free_users[~rc_users["user_id"].isin(user_calls["user_id"].unique())]["user_id"]

# Filter by date range.
user_call = rc_calls[
    (rc_calls["call_date"] >= "2020-04-01")
    & (rc_calls["call_date"] <= "2020-04-30")
]

# Filter rows in one specific month.
sf_events[sf_events["record_date"].dt.to_period("M") == "2021-01"]

# Filter rows where columns are null.
cvs_claims[
    (cvs_claims["date_submitted"].dt.to_period("M") == "2021-12")
    & (cvs_claims["date_accepted"].isnull())
    & (cvs_claims["date_rejected"].isnull())
]["claim_id"].nunique()

# Ends with a string.
sat_scores[~sat_scores["school"].str.endswith("HS")]

# Case-insensitive text search.
partners = postmates_partners[
    postmates_partners["name"].str.contains("pizza", case=False)
][["id", "name"]]


# ============================================================
# 3. CREATE OR MODIFY COLUMNS
# Knowledge:
# - `pd.to_datetime()` converts text to real dates.
# - `.dt` gives access to date parts like month/day/year.
# - `np.where()` is like a simple IF statement.
# - Good metric columns often come from division between aggregates.
# ============================================================

df["date"] = pd.to_datetime(df["date"])
df["day"] = df["date"].dt.date
df["month_num"] = df["date"].dt.month
df["month"] = df["date"].dt.to_period("M")

df["session_duration"] = (
    df["session_end"] - df["session_start"]
).dt.total_seconds()

df["ctr"] = df["clicks"] / df["impressions"]
df["cvr"] = df["conversions"] / df["clicks"]
df["roas"] = df["revenue"] / df["spend"]
df["cpi"] = df["spend"] / df["installs"]
df["flag"] = np.where(df["revenue"] > 100, 1, 0)

# Important: wrap long math expressions in parentheses for readability.
result = (
    facebook_products[
        (facebook_products["is_low_fat"] == "Y")
        & (facebook_products["is_recyclable"] == "Y")
    ]["product_id"].nunique()
    / facebook_products["product_id"].nunique()
)


# ============================================================
# 4. MISSING VALUES
# Knowledge:
# - `isna()` / `isnull()` detect missing values.
# - `notna()` is the opposite.
# - `fillna()` replaces missing data.
# ============================================================

df.isna().sum()
df = df.fillna(0)
df["score"] = df["score"].fillna(df["score"].median())

airbnb_search_details["review_scores_rating"].notna()


# ============================================================
# 5. SORT, UNIQUE, DUPLICATES
# Knowledge:
# - `sort_values()` sorts rows.
# - `nunique()` counts distinct values.
# - `drop_duplicates()` removes repeated rows.
# ============================================================

df.sort_values(["campaign", "revenue"], ascending=[True, False])
df["user_id"].nunique()
df.drop_duplicates()
df.drop_duplicates(subset=["user_id"])
df.drop_duplicates(subset=["col1", "col2"])

# Sort using a custom key: here by the 2nd character.
random_id.sort_values(by="id", key=lambda x: x.str[1]).reset_index(drop=True)

# Convert text to int before sorting.
movie_catalogue["duration_int"] = (
    movie_catalogue["duration"].str.replace(" min", "").astype(int)
)
result = movie_catalogue.sort_values(
    by="duration_int", ascending=False
).drop(columns=["duration_int"])


# ============================================================
# 6. GROUPBY AND AGGREGATION
# Knowledge:
# - `groupby()` splits data into groups.
# - `agg()` lets you compute several summary stats at once.
# - `size()` counts all rows, including duplicates.
# ============================================================

agg_df = (
    df.groupby(["campaign", "country"])
    .agg(
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        conversions=("conversions", "sum"),
        revenue=("revenue", "sum"),
        spend=("spend", "sum"),
        users=("user_id", "nunique"),
    )
    .reset_index()
)

agg_df["ctr"] = agg_df["clicks"] / agg_df["impressions"]
agg_df["cvr"] = agg_df["conversions"] / agg_df["clicks"]
agg_df["roas"] = agg_df["revenue"] / agg_df["spend"]

result = dim_customer.groupby("cust_id").size().reset_index(name="count").query("count > 1")

df = transactions_filter.merge(wfm_products, on="product_id", how="inner")
result = (
    df.groupby("product_category")
    .agg(
        num_transaction=("transaction_id", "nunique"),
        total_sale=("sales", "sum"),
    )
    .sort_values("total_sale", ascending=False)
    .reset_index()
)

# Aggregate and return one named result.
result = amazon_sales.loc[
    amazon_sales["order_date"].dt.year == 2021,
    "order_total",
].agg(revenue="sum")

# Sort then take only the first row.
result = (
    forbes_global_2010_2014.groupby("industry")["sales"]
    .mean()
    .reset_index()
    .sort_values(by="sales")
    .head(1)[["industry"]]
)

# Group then filter like SQL HAVING.
result = (
    airbnb_search_details.groupby("neighbourhood")["beds"]
    .sum()
    .reset_index()
    .query("beds >= 3")
)


# ============================================================
# 7. MERGE / JOIN
# Knowledge:
# - `merge()` is the pandas version of SQL JOIN.
# - `on=` means same join key on both sides.
# - `left_on=` and `right_on=` are for different column names.
# ============================================================

df = df.merge(other_df, on="user_id", how="left")
df = df.merge(other_df, left_on="campaign_id", right_on="id", how="inner")

result = pd.merge(transactions, signups, how="left", on="signup_id")

merged = pd.merge(rc_calls, rc_users, how="left", on="user_id")


# ============================================================
# 8. DATE HANDLING
# Knowledge:
# - `.dt.to_period("M")` creates month buckets.
# - `.dt.strftime()` formats dates as strings.
# - `between()` is useful for date intervals.
# ============================================================

amazon_shipment["month"] = amazon_shipment["shipment_date"].dt.to_period("M")
amazon_shipment["unique_id"] = (
    amazon_shipment["shipment_id"].astype(str)
    + "_"
    + amazon_shipment["sub_id"].astype(str)
)
result = amazon_shipment.groupby("month")["unique_id"].nunique().reset_index()

sf_exchange_rate["month"] = sf_exchange_rate["date"].dt.to_period("M")
sf_exchange_rate["month"] = sf_exchange_rate["month"].dt.strftime("%Y-%m")

result = sf_exchange_rate[
    sf_exchange_rate["month"].isin(["2020-01", "2020-07"])
].sort_values(["source_currency", "date"])

postmates_orders["date"] = postmates_orders["order_timestamp_utc"].dt.date
postmates_orders[
    postmates_orders["date"].isin(pd.to_datetime(["2019-03-11", "2019-04-11"]).date)
]

result = doordash_delivery[
    doordash_delivery["customer_placed_order_datetime"].between("2020-05-01", "2020-05-31")
].groupby("restaurant_id")["order_total"].sum().to_frame("total_order").reset_index()


# ============================================================
# 9. WINDOW-STYLE OPERATIONS
# Knowledge:
# - `transform()` keeps the original row count and adds a group-level value.
# - `shift()` gets previous or next rows inside a group.
# - `rank()` creates ranking similar to SQL RANK / DENSE_RANK.
# - `cumsum()` creates a running total.
# ============================================================

amazon_shipment["total_weight"] = (
    amazon_shipment.groupby("shipment_id")["weight"].transform("sum")
)

df["campaign_total_rev"] = df.groupby("campaign")["revenue"].transform("sum")
df["rev_share"] = df["revenue"] / df["campaign_total_rev"]

df = df.sort_values(["user_id", "date"])
df["prev_revenue"] = df.groupby("user_id")["revenue"].shift(1)
df["rev_diff"] = df["revenue"] - df["prev_revenue"]

df["rank"] = df.groupby("campaign")["revenue"].rank(method="dense", ascending=False)
df["cum_rev"] = df.sort_values("date").groupby("campaign")["revenue"].cumsum()

# Dense rank example.
shipment_rank = (
    amazon_shipment.groupby("shipment_id")["weight"]
    .sum()
    .reset_index(name="total_weight")
)
shipment_rank["rank"] = shipment_rank["total_weight"].rank(method="dense", ascending=False)
result = shipment_rank[shipment_rank["rank"] == 3][["shipment_id", "total_weight"]]

# Max value per group with transform.
worker_logins["most_recent_login"] = (
    worker_logins.groupby("worker_id")["login_timestamp"].transform("max")
)
result = worker_logins[
    worker_logins["login_timestamp"] == worker_logins["most_recent_login"]
].drop(columns=["most_recent_login"])

# Previous rate by currency.
result["prev_rate"] = result.groupby("source_currency")["exchange_rate"].shift(1)
result["change"] = result["exchange_rate"] - result["prev_rate"]
final = result[result["month"] == "2020-07"][["source_currency", "change"]]


# ============================================================
# 10. PERCENT CHANGE, FIRST/LAST, IDXMAX
# Knowledge:
# - `pct_change()` gives growth rate.
# - `idxmin()` and `idxmax()` return row positions of min/max values.
# ============================================================

growth = (
    sf_events.assign(month=sf_events["record_date"].dt.to_period("M"))
    .query("month >= '2020-12' and month <= '2021-01'")
    .groupby(["account_id", "month"])["user_id"]
    .nunique()
    .reset_index()
    .sort_values(["account_id", "month"])
)
growth["growth_rate"] = growth.groupby("account_id")["user_id"].pct_change()
final = growth[growth["month"] == "2021-01"][["account_id", "growth_rate"]].reset_index(drop=True)

grouped = postmates_orders.groupby(["city_id", "date"])["amount"].sum().reset_index()
grouped = grouped.sort_values(["city_id", "date"])
grouped["prev_amount"] = grouped.groupby("city_id")["amount"].shift(1)
grouped["change"] = grouped["amount"] - grouped["prev_amount"]
max_growth = grouped.loc[grouped["change"].idxmax()]
max_drop = grouped.loc[grouped["change"].idxmin()]
final = pd.DataFrame([max_growth, max_drop])[["city_id", "change"]]


# ============================================================
# 11. TOP N PER GROUP
# Knowledge:
# - Sort first, then use `groupby(...).head(n)` to keep top rows in each group.
# ============================================================

top3 = (
    df.sort_values(["country", "revenue"], ascending=[True, False])
    .groupby("country")
    .head(3)
)


# ============================================================
# 12. PIVOT, UNSTACK, WIDE FORMAT
# Knowledge:
# - `pivot_table()` reshapes data into wide format.
# - `unstack()` moves one group level from rows to columns.
# ============================================================

pivot = pd.pivot_table(
    df,
    index="campaign",
    columns="device",
    values="revenue",
    aggfunc="sum",
    fill_value=0,
)

submissions.pivot_table(
    index="loan_id",
    columns="rate_type",
    values="id",
    aggfunc="size",
    fill_value=0,
).reset_index()

counts = (
    twitch_sessions.groupby(["user_id", "session_type"])["session_id"]
    .count()
    .unstack(fill_value=0)
)
counts = counts.rename(
    columns={
        "streamer": "streaming_sessions",
        "viewer": "viewing_sessions",
    }
)


# ============================================================
# 13. TEXT CLEANING AND EXPLODE
# Knowledge:
# - `str.replace()` cleans strings.
# - `str.split()` turns a string into a list.
# - `explode()` turns one list item into one row.
# ============================================================

df["amenities_clean"] = df["amenities"].str.replace(r"[{}\"]", "", regex=True)
df["amenities_clean"] = df["amenities_clean"].str.split(",")
df_explode = df.explode("amenities_clean")

df_explode[
    (df_explode["amenities_clean"].str.contains("parking", case=False, na=False))
    & (df_explode["cleaning_fee"] == False)
]["neighbourhood"].unique()


# ============================================================
# 14. BINNING AND CASE-WHEN LOGIC
# Knowledge:
# - `pd.cut()` bins numeric values into categories.
# - `np.select()` works like SQL CASE WHEN.
# ============================================================

airbnb_search_details["review_category"] = pd.cut(
    airbnb_search_details["number_of_reviews"],
    bins=[-1, 0, 5, 15, 40, float("inf")],
    labels=["NO", "FEW", "SOME", "MANY", "A LOT"],
)

conditions = [
    result["number_of_reviews"] == 0,
    result["number_of_reviews"].between(1, 5),
    result["number_of_reviews"].between(6, 15),
    result["number_of_reviews"].between(16, 40),
    result["number_of_reviews"] > 40,
]

choices = ["NO", "FEW", "SOME", "MANY", "A LOT"]

result["review_category"] = np.select(conditions, choices)
result = result[["price", "review_category"]]


# ============================================================
# 15. FUNNEL, RETENTION, OUTLIERS
# Knowledge:
# - These are common business analytics patterns.
# - Funnel tracks user drop-off between steps.
# - Retention tracks returning users over time.
# - IQR is a quick statistical rule for outlier detection.
# ============================================================

funnel = df.groupby("step")["user_id"].nunique().reset_index(name="users")
funnel["conversion_rate"] = funnel["users"] / funnel["users"].iloc[0]
funnel['conversion_rate'].fillna(0) # safe divide

first_seen = df.groupby("user_id")["date"].min().rename("first_date")
df = df.merge(first_seen, on="user_id")
df["days_since_first"] = (df["date"] - df["first_date"]).dt.days
retention = df.groupby("days_since_first")["user_id"].nunique().reset_index(name="active_users")

q1 = df["revenue"].quantile(0.25)
q3 = df["revenue"].quantile(0.75)
iqr = q3 - q1
outliers = df[
    (df["revenue"] < q1 - 1.5 * iqr)
    | (df["revenue"] > q3 + 1.5 * iqr)
]


# ============================================================
# 16. CORRELATION
# Knowledge:
# - `corr()` measures linear relationship between two numeric columns.
# - Positive means they rise together, negative means one rises when the other falls.
# ============================================================

delivery_details["final_order_value"] = (
    delivery_details["order_total"]
    + delivery_details["tip_amount"]
    - (delivery_details["discount_amount"] + delivery_details["refunded_amount"])
)

delivery_details["delivery_time"] = (
    delivery_details["delivered_to_consumer_datetime"]
    - delivery_details["customer_placed_order_datetime"]
)
delivery_details["delivery_time_minutes"] = delivery_details["delivery_time"].apply(
    lambda x: x.total_seconds() / 60
)

result = delivery_details.groupby("restaurant_id").agg(
    {
        "delivery_time_minutes": "mean",
        "final_order_value": "mean",
    }
)
result = result["delivery_time_minutes"].corr(result["final_order_value"])


# ============================================================
# 17. QUANTILES / NTILE-LIKE LOGIC
# Knowledge:
# - `pd.qcut()` splits data into quantile buckets.
# - It is similar to SQL NTILE.
# ============================================================

result = (
    doordash_delivery[
        doordash_delivery["customer_placed_order_datetime"].between("2020-05-01", "2020-05-31")
    ]
    .groupby("restaurant_id")["order_total"]
    .sum()
    .to_frame("total_order")
    .reset_index()
)
result["ntile"] = pd.qcut(
    result["total_order"],
    q=50,
    labels=range(1, 50),
    duplicates="drop",
).values.tolist()
result = result[result["ntile"] == 1][["restaurant_id", "total_order"]].sort_values(
    "total_order", ascending=False
)


# ============================================================
# 18. MORE PRACTICE PATTERNS
# Knowledge:
# - This section keeps useful interview-style patterns grouped together.
# - Many of them combine filter + groupby + merge + transform.
# ============================================================

df1 = result.groupby("location")["amt"].mean().to_frame("mean_revenue")
signups["signup_duration"] = (
    signups["signup_stop_date"] - signups["signup_start_date"]
).astype("timedelta64[D]")
df2 = signups.groupby("location")["signup_duration"].mean().to_frame("mean_duration")
result = pd.merge(df2, df1, how="left", left_index=True, right_index=True).reset_index()
result["ratio"] = result["mean_revenue"] / result["mean_duration"]
result = result.sort_values(by="ratio", ascending=False)

events_list = [
    "video call received",
    "video call sent",
    "voice call received",
    "voice call sent",
]

fact_events["event_check"] = fact_events["event_type"].isin(events_list).astype(int)
fact_events["event_check_mean"] = fact_events.groupby("user_id")["event_check"].transform("mean")

filtered = fact_events[fact_events["event_check_mean"] >= 0.5][["user_id", "client_id"]].drop_duplicates()
result = (
    filtered.groupby("client_id")["user_id"]
    .count()
    .reset_index(name="user_count")
    .sort_values("user_count", ascending=False)
    .head(1)
    .rename(columns={"client_id": "CLIENT_ID"})
    [["CLIENT_ID"]]
)

result = fact_events.groupby(pd.to_datetime(fact_events["time_id"]).dt.month)["user_id"].nunique().to_frame(
    "n_users"
)
df1 = fact_events.groupby("user_id")["time_id"].min().to_frame("month_min").reset_index()
df1["month_min"] = pd.to_datetime(df1["month_min"]).dt.month
df1 = df1.groupby("month_min")["user_id"].nunique().to_frame("n_new_users")
result = result.join(df1)
result["share_of_new_users"] = result["n_new_users"] / result["n_users"]
result["share_of_old_users"] = 1 - result["share_of_new_users"]
result = result[["share_of_new_users", "share_of_old_users"]].reset_index()

twitch_sessions["session_start"] = pd.to_datetime(twitch_sessions["session_start"])
first_sessions = twitch_sessions.loc[twitch_sessions.groupby("user_id")["session_start"].idxmin()]
first_viewers = first_sessions[first_sessions["session_type"] == "viewer"][["user_id"]]

streamer_counts = (
    twitch_sessions[twitch_sessions["session_type"] == "streamer"]
    .groupby("user_id")["session_id"]
    .count()
    .reset_index(name="n_sessions")
)

result = pd.merge(first_viewers, streamer_counts, on="user_id", how="left").fillna(0)
result["n_sessions"] = result["n_sessions"].astype(int)
result = result.sort_values(["n_sessions", "user_id"], ascending=[False, True])


# ============================================================
# 19. MULTI-STEP MERGE EXAMPLE
# Knowledge:
# - This is a more advanced path-building example using repeated merges.
# - `itertools.product()` creates all possible origin/destination pairs.
# ============================================================

df = pd.DataFrame(
    list(itertools.product(da_flights["origin"].unique(), da_flights["destination"].unique())),
    columns=["origin", "destination"],
)
df = df[df["origin"] != df["destination"]]

connections_1 = pd.merge(
    da_flights,
    da_flights,
    how="left",
    left_on="destination",
    right_on="origin",
    suffixes=["_0", "_1"],
)

connections_2 = pd.merge(
    connections_1,
    da_flights[["origin", "destination", "cost"]],
    how="left",
    left_on="destination_1",
    right_on="origin",
    suffixes=["", "_2"],
).fillna(0)

connections_2.columns = [
    "id_0",
    "origin_0",
    "destination_0",
    "cost_0",
    "id_1",
    "origin_1",
    "destination_1",
    "cost_1",
    "origin_2",
    "destination_2",
    "cost_2",
]

connections_2["cost_v1"] = connections_2["cost_0"] + connections_2["cost_1"]
connections_2["cost_v2"] = (
    connections_2["cost_0"] + connections_2["cost_1"] + connections_2["cost_2"]
)

result = pd.merge(
    df,
    da_flights[["origin", "destination", "cost"]],
    how="left",
    on=["origin", "destination"],
)

result = pd.merge(
    result,
    connections_2[["origin_0", "destination_1", "cost_v1"]],
    how="left",
    left_on=["origin", "destination"],
    right_on=["origin_0", "destination_1"],
)

result = pd.merge(
    result,
    connections_2[["origin_0", "destination_2", "cost_v2"]],
    how="left",
    left_on=["origin", "destination"],
    right_on=["origin_0", "destination_2"],
)

result["min_price"] = result[["cost", "cost_v1", "cost_v2"]].min(axis=1)
result[~result["min_price"].isna()][["origin", "destination", "min_price"]]


# ============================================================
# 20. MATPLOTLIB BASICS
# Knowledge:
# - `plt.figure()` sets chart size.
# - `plt.plot()` makes line charts.
# - `plt.bar()` makes bar charts.
# - `plt.pie()` makes pie charts.
# - `label`, `title`, `legend`, `color`, `grid`, and `xticks` are common customizations.
# ============================================================

# Example data for chart practice.
months = ["Jan", "Feb", "Mar", "Apr"]
sales = [120, 150, 135, 170]
cost = [80, 95, 90, 110]
profit = [40, 55, 45, 60]
market_share = [40, 25, 20, 15]
channels = ["Ads", "Email", "Organic", "Referral"]


# ------------------------------------------------------------
# 20A. Line chart
# Knowledge:
# - Best for trends over time.
# - `marker` highlights each point.
# - `linestyle` changes the line pattern.
# ------------------------------------------------------------
plt.figure(figsize=(8, 4))
plt.plot(months, sales, marker="o", linestyle="-", color="steelblue", label="Sales")
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(True, linestyle="--", alpha=0.4)
plt.legend()
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 20B. Bar chart
# Knowledge:
# - Best for comparing categories.
# - `color` can be one color or a list of colors.
# - `alpha` controls transparency.
# ------------------------------------------------------------
plt.figure(figsize=(8, 4))
plt.bar(months, sales, color="cornflowerblue", alpha=0.85)
plt.title("Sales by Month")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 20C. Pie chart
# Knowledge:
# - Best for showing share of a total.
# - `autopct` shows percentages.
# - `startangle` rotates the chart.
# - `explode` pulls a slice outward to emphasize it.
# ------------------------------------------------------------
plt.figure(figsize=(6, 6))
plt.pie(
    market_share,
    labels=channels,
    autopct="%1.1f%%",
    startangle=90,
    explode=[0.05, 0, 0, 0],
)
plt.title("Traffic Source Share")
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 20D. Combo chart: bar + line
# Knowledge:
# - Useful when you want to compare volume and trend together.
# - A common combo is bars for sales and a line for profit.
# ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(months, sales, color="skyblue", label="Sales")
ax.plot(months, profit, color="darkorange", marker="o", linewidth=2, label="Profit")
ax.set_title("Sales and Profit")
ax.set_xlabel("Month")
ax.set_ylabel("Amount")
ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 20E. Multiple line chart
# Knowledge:
# - Plot more than one series to compare trends.
# - `linewidth` changes thickness.
# ------------------------------------------------------------
plt.figure(figsize=(8, 4))
plt.plot(months, sales, marker="o", linewidth=2, label="Sales")
plt.plot(months, cost, marker="s", linewidth=2, label="Cost")
plt.plot(months, profit, marker="^", linewidth=2, label="Profit")
plt.title("Sales, Cost, and Profit")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 20F. How to customize charts
# Knowledge:
# - These are the most common chart controls you will use.
# ------------------------------------------------------------
plt.figure(figsize=(9, 5))
plt.bar(months, sales, color=["#4C78A8", "#59A14F", "#F28E2B", "#E15759"])
plt.title("Customized Bar Chart", fontsize=14, fontweight="bold")
plt.xlabel("Month", fontsize=11)
plt.ylabel("Sales", fontsize=11)
plt.xticks(rotation=30)
plt.ylim(0, 200)
plt.grid(axis="y", linestyle=":", alpha=0.4)

for i, value in enumerate(sales):
    plt.text(i, value + 3, str(value), ha="center")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 20G. Pandas plotting shortcut
# Knowledge:
# - `DataFrame.plot()` is a quick wrapper around matplotlib.
# - Good for fast exploratory analysis.
# ------------------------------------------------------------
daily = df.groupby("date", as_index=False)["revenue"].sum()
daily.plot(x="date", y="revenue", figsize=(8, 4), title="Daily Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

agg_df.groupby("campaign")["roas"].mean().plot(kind="bar", figsize=(8, 4), title="Average ROAS by Campaign")
plt.ylabel("ROAS")
plt.tight_layout()
plt.show()

