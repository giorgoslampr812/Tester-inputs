import pandas as pd

input_file = "mdt_hits_with_co_time_2.csv"
output_file = "event_670755_co_time.csv"

# Read file
df = pd.read_csv(input_file)

# Filter event
filtered = df[df["event"] == 670755][["co_time", "mezz", "channel","layer"]]

# Save to new CSV
filtered.to_csv(output_file, index=False)

print(f"Saved {len(filtered)} rows to {output_file}")
