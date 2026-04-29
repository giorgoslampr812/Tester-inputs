import pandas as pd

input_file = "rpc_ps.csv"
output_file = "rpc_ps_full_BCID.csv"

# Read file
df = pd.read_csv(input_file)

# Ensure BCID is integer
df["BCID"] = df["BCID"].astype(int)

# Add BCID_te column
df["BCID_te"] = df["BCID"]

# All possible BCIDs
all_bcids = set(range(4096))
existing_bcids = set(df["BCID"])

missing_bcids = sorted(all_bcids - existing_bcids)

# Create zero rows for missing BCIDs
rows_to_add = []

for bcid in missing_bcids:
    new_row = {col: 0 for col in df.columns}
    new_row["BCID"] = bcid
    new_row["BCID_te"] = bcid
    rows_to_add.append(new_row)

# Append them
df_full = pd.concat([df, pd.DataFrame(rows_to_add)], ignore_index=True)

# Sort by BCID_te
df_full = df_full.sort_values("BCID_te").reset_index(drop=True)

# Save
df_full.to_csv(output_file, index=False)

print("Saved:", output_file)
print("Total rows:", len(df_full))

