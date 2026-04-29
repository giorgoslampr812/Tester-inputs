import pandas as pd

input_file = "mdt_hits_event_585278.csv"
output_file = "event_585278_sorted.csv"

# Read file
df = pd.read_csv(input_file)

# Filter event
filtered = df[df["event"] == 585278][["co_time", "rank", "channel"]].rename(
    columns={"rank": "tester_tdc"}
)

# Save to new CSV
filtered.to_csv(output_file, index=False)

print(f"Saved {len(filtered)} rows to {output_file}")
