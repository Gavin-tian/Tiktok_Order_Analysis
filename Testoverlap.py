import os
from datetime import datetime
import pandas as pd

# === File path setup ===
user_home = os.path.expanduser("~")

# New raw file path
new_file_path = os.path.join(user_home, "Downloads", "All order-2025-06-03-10_09.csv")

# Previous combined file path
combined_file_path = os.path.join(user_home, "Downloads", "All order-2025-06-09-11_19.csv")

# === Load new file ===
df_new = pd.read_csv(new_file_path)
df_new.columns = df_new.columns.str.strip()  # remove leading/trailing spaces
if "Order ID" in df_new.columns:
    df_new.rename(columns={"Order ID": "order_id"}, inplace=True)
df_new["order_id"] = df_new["order_id"].astype(str)

# === Load previous combined file if exists ===
if os.path.exists(combined_file_path):
    df_old = pd.read_csv(combined_file_path)
    df_old.columns = df_old.columns.str.strip()
    if "Order ID" in df_old.columns:
        df_old.rename(columns={"Order ID": "order_id"}, inplace=True)
    df_old["order_id"] = df_old["order_id"].astype(str)

    # === Overlap check ===
    overlap = set(df_new["order_id"]) & set(df_old["order_id"])
    if overlap:
        print(f"❌ Overlap detected! {len(overlap)} duplicate order_id(s). Merge aborted.")
        exit()
    else:
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
        print(f"✅ No overlap. Merged {len(df_new)} new rows.")
else:
    df_combined = df_new.copy()
    print(f"ℹ️ No previous combined file found. Starting fresh with {len(df_new)} rows.")

# === Create timestamped output folder ===
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = os.path.join(user_home, "Desktop", f"order_check_session_{timestamp}")
os.makedirs(output_dir, exist_ok=True)

# === Save files ===
date_str = datetime.now().strftime("%Y%m%d")
combined_dated_path = os.path.join(output_dir, f"combined_orders_{date_str}.csv")
df_combined.to_csv(combined_dated_path, index=False)

raw_copy_path = os.path.join(output_dir, os.path.basename(new_file_path))
df_new.to_csv(raw_copy_path, index=False)

df_combined.to_csv(combined_file_path, index=False)

# === Summary Output ===
print(f"📁 Dated combined file saved to: {combined_dated_path}")
print(f"📦 Raw new file copied to: {raw_copy_path}")
print(f"🆕 Master combined file updated at: {combined_file_path}")
