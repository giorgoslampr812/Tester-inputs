import pandas as pd
for i in range(1,17):
 input_file = f"mdt_hits_filtered_top2mezz_per_layer_{i}.csv"
 output_file = f"mdt_hits_with_co_time_{i}.csv"

 # Read CSV
 df = pd.read_csv(input_file)

 # Compute co_time
 df["co_time"] = (df["BCID"] * 32 + df["drift_time"] * 32 / 25).astype(int)

 # Ensure range 0–131071
 df["co_time"] = df["co_time"].clip(0, 131071)

 # Save new file
 df.to_csv(output_file, index=False)

 print("Saved:", output_file)

