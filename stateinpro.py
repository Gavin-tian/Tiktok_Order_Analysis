import pandas as pd
import plotly.express as px

# Load and clean your dataset
file_path = "/Users/tachouyou/Desktop/non_missing_value_orders.csv"  # Update this path if needed
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

# Keep only top 10 states
top_states = merged[['State', 'Purchase Count_Total']].drop_duplicates().nlargest(10, 'Purchase Count_Total')
merged_top = merged[merged['State'].isin(top_states['State'])].copy()  # <- make a copy

# Create rich hover text safely
merged_top.loc[:, 'hover_text'] = (
    "Buyer: " + merged_top['Recipient'] +
    "<br>Purchases: " + merged_top['Purchase Count'].astype(str) +
    "<br>Products: " + merged_top['product_name']
)

# Plot interactive bar chart
fig = px.bar(
    merged_top,
    x='State',
    y='Purchase Count',
    color='Recipient',
    hover_name='Recipient',
    hover_data={'State': False, 'Purchase Count': False, 'hover_text': True},
    custom_data=['hover_text']
)

fig.update_traces(
    hovertemplate='%{customdata[0]}<extra></extra>'
)
fig.update_layout(
    title="Top 10 buyer States with Buyer and Product Details",
    xaxis_title="State",
    yaxis_title="Purchase Count"
)

# Save to HTML
fig.write_html("Buyer_states_with_products.html")
