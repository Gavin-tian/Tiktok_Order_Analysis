import pandas as pd
import os

# Define path to Downloads folder
downloads_path = os.path.expanduser("~/Downloads")

# Full paths to your files
file1 = os.path.join(downloads_path, "All order-2025-03-18-03_33.csv")
file2 = os.path.join(downloads_path, "All order-2025-03-25-01_54.csv")

# Read the CSVs
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Normalize column names
df1.columns = df1.columns.str.strip().str.lower()
df2.columns = df2.columns.str.strip().str.lower()

# Merge and remove duplicates based on 'order id' and 'sku id'
merged = pd.concat([df1, df2], ignore_index=True)
merged_dedup = merged.drop_duplicates(subset=['order id', 'sku id'])

# Save result back to Downloads
output_path = os.path.join(downloads_path, "final_merged_no_duplicates.csv")
merged_dedup.to_csv(output_path, index=False)

print(f"Merged file saved as: {output_path}")
