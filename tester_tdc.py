import pandas as pd
import numpy as np

# --------------------------
# Load data
# --------------------------
df = pd.read_csv("mdt_hits_with_co_time_1.csv")

# --------------------------
# Ask user for event ID
# --------------------------
event_id = 585278 
df = df[df["event"] == event_id].copy()
print(f"Processing only event {event_id}, {len(df)} hits")

# --------------------------
# 1. Compute distance
# --------------------------
df["dis"] = np.sqrt(df["tube_rho"]**2 + df["tube_z"]**2)

# --------------------------
# 2. Group by (mezz, layer)
# --------------------------
group_cols = ["mezz", "layer"]

avg_dis = (
    df.groupby(group_cols)["dis"]
    .mean()
    .reset_index()
    .rename(columns={"dis": "avg_dis"})
)

# --------------------------
# 3. Sort and rank
# --------------------------
avg_dis = avg_dis.sort_values("avg_dis").reset_index(drop=True)
avg_dis["rank"] = avg_dis.index

# --------------------------
# 4. Merge back (keeps ALL original columns)
# --------------------------
df = df.merge(avg_dis, on=group_cols, how="left")

# --------------------------
# Save output
# --------------------------
out_file = f"mdt_hits_event_{event_id}.csv"

df.to_csv(out_file, index=False)

print(f"Saved → {out_file}")
