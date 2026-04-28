import pandas as pd

input_file = "pseudodata_modified.csv"
output_file = "pseudodata_bitstream.csv"

# Load data
df = pd.read_csv(input_file)

# ---- Sort by time ----
df = df.sort_values("time").reset_index(drop=True)

# ---- Create bit streams ----
df["tdcid_bits"] = df["tdcid"].apply(lambda x: format(int(x), "04b"))
df["channel_bits"] = df["chnlid"].apply(lambda x: format(int(x), "05b"))
df["time_bits"] = df["time"].apply(lambda x: format(int(x), "017b"))

# Save result
df.to_csv(output_file, index=False)

print("Saved:", output_file)

