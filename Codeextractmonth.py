import pandas as pd

# Use the correct path provided by the upload
file_path = "/Users/tachouyou/Desktop/tiktokorder/Laninfluencer_orders.csv"
# Load the data
df = pd.read_csv(file_path,dtype=str)

df = df.astype(str).apply(lambda col: col.str.strip())

# Convert 'Created Time' to datetime
df['created_time'] = pd.to_datetime(df['created_time'],format="%m/%d/%Y %I:%M:%S %p"
,errors='coerce')

# Define the date range
start_date = "06/01/2025"
end_date = "07/01/2025"

# Filter the DataFrame
filtered_orders = df[(df['created_time'] >= start_date) & (df['created_time'] <= end_date)]

# Output result
output_path = "/Users/tachouyou/Desktop/tiktokorder/JuneLaninfluencer_orders.csv"
filtered_orders.to_csv(output_path, index=False)
