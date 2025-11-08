import pandas as pd
import plotly.express as px

# Load and clean your dataset
file_path = "/Users/tachouyou/Desktop/missing_value_orders.csv"
df = pd.read_csv(file_path, dtype=str)
df = df.astype(str).apply(lambda col: col.str.strip())

# Extract Recipient and State from Shipping Information if they don't exist
if 'Recipient' not in df.columns or 'State' not in df.columns:
    df['Recipient'] = df['shipping_information'].str.extract(r'^([^\n\r]+)')
    df['State'] = df['shipping_information'].str.extract(r'\n(?:.*\n)?[A-Za-z\s]+,\s*([A-Za-z\s]+)')

# Remove rows with missing Recipient or State
df = df.dropna(subset=['Recipient', 'State'])

# Count how many times each buyer bought in each state
buyer_state_counts = df.groupby(['State', 'Recipient']).size().reset_index(name='Purchase Count')

# Aggregate total order count per state
state_order_counts = buyer_state_counts.groupby('State')['Purchase Count'].sum().reset_index()

# Join recipient info for hover tooltip
def make_hover_text(state):
    buyers = buyer_state_counts[buyer_state_counts['State'] == state]
    return "<br>".join([f"{row['Recipient']}: {row['Purchase Count']}x" for _, row in buyers.iterrows()])

state_order_counts['Recipient'] = state_order_counts['State'].apply(make_hover_text)

# Sort by order count and select top 10
top_states = state_order_counts.sort_values(by='Purchase Count', ascending=False).head(10)

# Plot interactive bar chart
fig = px.bar(
    top_states,
    x='State',
    y='Purchase Count',
    hover_data={'Recipient': True},
    title='Top 10 Buyer States (Click Bar to View Buyer Names + Counts)',
    labels={'Recipient': 'Buyers'}
)

# Save to HTML
fig.write_html("/Users/tachouyou/Desktop/LGtop_10_influencer_states(Jan).html")
