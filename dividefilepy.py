import pandas as pd

# Load the dataset
file_path = "/Users/tachouyou/Desktop/tiktokorder/Laneige_order_June_July.csv"  # Replace with your actual path
df = pd.read_csv(file_path)

# Standardize column names (optional but helpful)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Define the relevant columns
quantity_col = 'quantity'
price_col = 'order_amount'  # Make sure this matches your actual column name

# Identify rows where quantity is present but price is missing or zero
missing_value_df = df[(df[quantity_col].notna()) & ((df[price_col].isna()) | (df[price_col] == 0))]

# The rest are non-missing
non_missing_value_df = df.drop(missing_value_df.index)

# Save the outputs to CSV files
missing_value_df.to_csv("Laninfluencer_orders.csv", index=False)
non_missing_value_df.to_csv("Lannormal_orders.csv", index=False)
