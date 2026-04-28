import pandas as pd
import os
for i in range(1,17):
# --- Input / Output ---
    input_csv = f"filtered_events_A/mdt_hits_within_offsets_per_layer_{i}.csv"
    output_csv = f"two_mezz_events_A/mdt_hits_filtered_top2mezz_per_layer_{i}.csv"

# --- Load file ---
    df = pd.read_csv(input_csv)

    print(f"Loaded {len(df)} MDT hits from {len(df['event'].unique())} events.")

# --- Helper function: keep top 2 mezz per layer per event ---
    filtered_events = []

    for evt, evt_df in df.groupby("event"):
        evt_filtered = []

        for layer, layer_df in evt_df.groupby("layer"):
            mezz_counts = layer_df["mezz"].value_counts()

            if len(mezz_counts) > 2:
                # Select top 2 mezzanines with most hits
                top2 = mezz_counts.nlargest(2).index.tolist()
                kept_df = layer_df[layer_df["mezz"].isin(top2)].copy()
            else:
                # Keep all mezzanines if ≤2
                kept_df = layer_df.copy()

            evt_filtered.append(kept_df)

        if evt_filtered:
            filtered_events.append(pd.concat(evt_filtered, ignore_index=True))

# --- Combine all filtered events ---
    if filtered_events:
        filtered_df = pd.concat(filtered_events, ignore_index=True)
        filtered_df.to_csv(output_csv, index=False)
        print(f"✅ Saved filtered data to {output_csv}")
        print(f"Remaining hits: {len(filtered_df)}, Events: {len(filtered_df['event'].unique())}")
    else:
        print("⚠️ No events found after mezzanine filtering.")

