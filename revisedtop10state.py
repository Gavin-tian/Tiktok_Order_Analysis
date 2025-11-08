import pandas as pd
import plotly.express as px

# Load and clean your dataset
file_path = "/Users/tachouyou/Desktop/tiktokorder/JulyLannormal_orders.csv"  # Update this path if needed
df = pd.read_csv(file_path, dtype=str)
df = df.astype(str).apply(lambda col: col.str.strip())

# Extract Recipient and State from shipping_information
df['Recipient'] = df['shipping_information'].str.extract(r'^([^\n\r]+)')
df['State'] = df['shipping_information'].str.extract(r'\n(?:.*\n)?[A-Za-z\s]+,\s*([A-Za-z\s]+)')
df['product_name'] = df['product_name'].fillna("Unknown Product")

# Drop rows with missing Recipient or State
df = df.dropna(subset=['Recipient', 'State'])

# Count how many times each buyer bought in each state & collect product names
grouped = (
    df.groupby(['State', 'Recipient'])
    .agg({
        'order_id': 'count',
        'product_name': lambda x: ', '.join(sorted(set(x)))
    })
    .reset_index()
    .rename(columns={'order_id': 'Purchase Count'})
)

# Aggregate total purchase count per state
state_counts = grouped.groupby('State')['Purchase Count'].sum().reset_index()
state_counts = state_counts.rename(columns={'Purchase Count': 'Purchase Count_Total'})

# Merge for enriched data
merged = pd.merge(grouped, state_counts, on='State')

# Keep only top 10 states by total purchases (DESC) and freeze that order for plotting
top_states = (
    merged[['State', 'Purchase Count_Total']].drop_duplicates()
    .sort_values('Purchase Count_Total', ascending=False)
    .head(10)
)
ordered_states = top_states['State'].tolist()

merged_top = merged[merged['State'].isin(ordered_states)].copy()
merged_top['State'] = pd.Categorical(merged_top['State'], categories=ordered_states, ordered=True)

# Create rich hover text safely
merged_top.loc[:, 'hover_text'] = (
    "Buyer: " + merged_top['Recipient'] +
    "<br>Purchases: " + merged_top['Purchase Count'].astype(str) +
    "<br>Products: " + merged_top['product_name']
)

# Plot interactive bar chart (legend hidden)
fig = px.bar(
    merged_top.sort_values('State'),
    x='State',
    y='Purchase Count',
    color='Recipient',
    hover_name='Recipient',
    hover_data={'State': False, 'Purchase Count': False, 'hover_text': True},
    custom_data=['hover_text']
)

fig.update_traces(hovertemplate='%{customdata[0]}<extra></extra>')

# Ensure x is ordered by total descending and hide legend
fig.update_layout(
    title="Top 10 Buyer States (Most → Least) with Buyer & Product Details",
    xaxis_title="State",
    yaxis_title="Purchase Count",
    showlegend=False,  # <- hides the legend
    xaxis=dict(categoryorder='array', categoryarray=ordered_states)  # enforce ordering
)

# Save to HTML
fig.write_html("Buyer_states_with_products_sorted_no_legend(Julynor).html")

# ---------- Top 10 States × Global Top 5 Products (+ Others) with REVENUE in hover ----------

import re
import numpy as np
import plotly.express as px
import pandas as pd

def _norm(s): return re.sub(r'[\s_]+','', s or '').lower()

def _pick_first(df_cols, candidates):
    norm = {_norm(c): c for c in df_cols}
    for cand in candidates:
        k = _norm(cand)
        if k in norm: return norm[k]
    return None

def _coerce_money(s: pd.Series) -> pd.Series:
    cleaned = (
        s.astype(str)
         .str.replace(r'[^\d\.\-\(\)]', '', regex=True)
         .str.replace(r'\((.*?)\)', r'-\1', regex=True)
    )
    cleaned = cleaned.apply(lambda x: re.sub(r'(?<=\d)\.(?=.*\.)', '', x) if isinstance(x, str) else x)
    return pd.to_numeric(cleaned, errors='coerce')

# Ensure we have a Revenue column to sum
if 'Revenue' not in df.columns:
    money_col = _pick_first(df.columns, [
        "Order Amount","Paid Amount","Amount","Total Amount","Total Price","Order Total",
        "Gross Amount","Net Amount","Payment Amount","order_amount","paid_amount"
    ])
    if money_col:
        df['Revenue'] = _coerce_money(df[money_col])
    else:
        price_col = _pick_first(df.columns, ["Price","Unit Price","Sale Price","Item Price","UnitPrice","price"])
        qty_col   = _pick_first(df.columns, ["Quantity","Qty","Item Qty","Order Quantity","quantity"])
        if price_col and qty_col:
            df['Revenue'] = _coerce_money(df[price_col]) * pd.to_numeric(df[qty_col], errors='coerce')
        else:
            df['Revenue'] = np.nan

# 1) Global Top-5 products (by COUNT over the period; change to 'Revenue' if you prefer)
global_top5_products = (
    df.groupby('product_name')
      .size()
      .reset_index(name='Total Purchases')
      .sort_values('Total Purchases', ascending=False)
      .head(5)['product_name']
      .tolist()
)

# 2) Top-10 states (by COUNT; set by_revenue=True to rank by revenue instead)
by_revenue = False  # <-- toggle if you want state ranking by revenue
if by_revenue:
    top10_states_global = (
        df.groupby('State')['Revenue'].sum().reset_index(name='Total')
          .sort_values('Total', ascending=False).head(10)['State'].tolist()
    )
else:
    top10_states_global = (
        df.groupby('State').size().reset_index(name='Total')
          .sort_values('Total', ascending=False).head(10)['State'].tolist()
    )

# 3) Filter to those states; aggregate COUNT + REVENUE (+ unique orders if available)
order_id_col = _pick_first(df.columns, ["Order ID","OrderID","order_id","Order Number","order_number"])

subset = df[df['State'].isin(top10_states_global)].copy()
subset['Revenue'] = pd.to_numeric(subset['Revenue'], errors='coerce').fillna(0)

agg_dict = {
    'product_name': 'size',      # will rename to Purchase Count
    'Revenue': 'sum',
}
group_cols = ['State','product_name']

if order_id_col:
    # use nunique order id at (State, product) level
    grouped = (subset
               .groupby(group_cols, dropna=False)
               .agg(Purchase_Count=('product_name','size'),
                    Revenue=('Revenue','sum'),
                    Unique_Orders=(order_id_col,'nunique'))
               .reset_index())
else:
    grouped = (subset
               .groupby(group_cols, dropna=False)
               .agg(Purchase_Count=('product_name','size'),
                    Revenue=('Revenue','sum'))
               .reset_index())
    grouped['Unique_Orders'] = np.nan

# 4) Split Top-5 vs Others (aggregate Others’ count/revenue/orders per state)
is_top5 = grouped['product_name'].isin(global_top5_products)
top5_rows = grouped[is_top5].copy()

others_rows = (grouped[~is_top5]
               .groupby('State', as_index=False)
               .agg(Purchase_Count=('Purchase_Count','sum'),
                    Revenue=('Revenue','sum'),
                    Unique_Orders=('Unique_Orders','sum')))
others_rows['product_name'] = 'Other products'

# 5) Combine; freeze state and product order
sp_counts = pd.concat([top5_rows, others_rows], ignore_index=True)
sp_counts['State'] = pd.Categorical(sp_counts['State'], categories=top10_states_global, ordered=True)
product_order = global_top5_products + ['Other products']

# 6) Build chart (bar height = Purchase Count; hover shows Revenue and Orders)
fig3 = px.bar(
    sp_counts.sort_values(['State','Purchase_Count'], ascending=[True, False]),
    x='State',
    y='Purchase_Count',
    color='product_name',
    category_orders={'product_name': product_order},
    custom_data=['product_name', 'Revenue', 'Unique_Orders']
)

# Hover with REVENUE and (if present) unique orders
fig3.update_traces(
    hovertemplate=(
        "State: %{x}<br>"
        "Product: %{customdata[0]}<br>"
        "Revenue: $%{customdata[1]:,.2f}<br>"
        "Unique Orders: %{customdata[2]}<extra></extra>"
    )
)

fig3.update_layout(
    title="Top 10 States — Global Top 5 Products + Other Products (Count bars, Revenue in hover)",
    xaxis_title="State",
    yaxis_title="Purchase Count",
    showlegend=False,                 # keep legend hidden per your preference
    barmode='stack',
    xaxis=dict(categoryorder='array', categoryarray=top10_states_global)
)

fig3.write_html("LanJuly10St5Pro.html")
