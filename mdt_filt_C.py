import matplotlib
matplotlib.use("Agg")  # non-interactive backend for servers

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
for i in range(1,17):
# --- Input files ---
    mdt_file = f"B_C_{i}/B_C_{i}_csm.csv"
    rpc_file = f"B_C_{i}/B_C_{i}_rpc.csv"
    output_csv = f"filtered_events_C/mdt_hits_within_offsets_per_layer_{i}.csv"
    out_dir = "event_hitmaps_selected"
    os.makedirs(out_dir, exist_ok=True)
    
# --- Load data ---
    mdt_df = pd.read_csv(mdt_file,skiprows = 6)
    rpc_df = pd.read_csv(rpc_file,skiprows = 6)

# --- Common events ---
    common_events = sorted(set(mdt_df["event"]).intersection(set(rpc_df["event"])))
    print(f"Found {len(common_events)} common events.")

# --- RPC radii ---
    if i%2 == 0:
     rpc_radii = [4700, 7700,8400, 9900]
    else: 
     rpc_radii = [5200, 6800,7580, 9900]
# --- Helper ---
    def get_rpc_zs(row):
        try:
            return [float(row[f"z_RPC{i}"]) for i in range(4)]
        except Exception:
            return None

    def get_layer(r):
        if r < 5550:
            return 1
        elif r < 9500:
            return 2
        else:
            return 3

    selected_hits = []

# --- Event loop ---
    for evt in common_events:
        mdt_evt = mdt_df[mdt_df["event"] == evt]
        rpc_evt = rpc_df[rpc_df["event"] == evt]

        if mdt_evt.empty or rpc_evt.empty:
            continue

        rpc_row = rpc_evt.iloc[0]
        rpc_zs = get_rpc_zs(rpc_row)
        if rpc_zs is None or any(np.isnan(rpc_zs)):
            continue

        eta_rpc = rpc_row.get("Eta", np.nan)

        #Eta check to select different eta regions 
        #Phi is selected by sector 
        eta_low = 0.59
        eta_high= 0.60
        #if eta_rpc < eta_low or eta_rpc > eta_high: 
        # continue

        z_rpc0, r_rpc0 = rpc_zs[0], rpc_radii[0]
        if z_rpc0 == 0:
            continue

    # --- geometry: slope and offsets ---
        m = r_rpc0 / z_rpc0
        b_left, b_right = m * 120, -m * 120  # ±12 cm offsets

        z_hit = mdt_evt["tube_z"].values
        r_hit = mdt_evt["tube_rho"].values

    # Compute offset boundaries
        r_center = m * z_hit
        r_left = m * z_hit + b_left
        r_right = m * z_hit + b_right

    # ensure left < right
        r_min = np.minimum(r_left, r_right)
        r_max = np.maximum(r_left, r_right)

    # Select hits inside region
        mask = (r_hit >= r_min) & (r_hit <= r_max)
        mdt_sel = mdt_evt[mask].copy()

        if mdt_sel.empty:
            continue

    # Check at least one hit per layer inside region
        mdt_sel["layer"] = mdt_sel["tube_rho"].apply(get_layer)
        layer_counts = mdt_sel.groupby("layer").size()

        if all(l in layer_counts.index for l in [1, 2, 3]):
            selected_hits.append(mdt_sel)
        else:
            continue

    # --- Plot for reference ---
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(mdt_evt["tube_z"], mdt_evt["tube_rho"],
               c="gray", marker="x", s=25, label="All MDT hits")

    # RPC points
        ax.scatter(rpc_zs, rpc_radii, color="orange", s=80,
               edgecolor="black", marker="s", label="RPC hits")

    # Offset lines
        z_vals = np.linspace(min(z_hit.min(), min(rpc_zs)) - 200,
                         max(z_hit.max(), max(rpc_zs)) + 200, 400)
        ax.plot(z_vals, m * z_vals, "r--", label="Center line")
        ax.plot(z_vals, m * z_vals + b_left, "b:", label="-120 mm offset")
        ax.plot(z_vals, m * z_vals + b_right, "g:", label="+120 mm offset")

    # Selected hits (hollow circles)
        ax.scatter(
            mdt_sel["tube_z"], mdt_sel["tube_rho"],
            facecolors="none", edgecolors="red", s=(15/10)**2*100,
            linewidths=1.2, label="MDT hits within ±12 cm"
    )

        ax.set_xlabel("z [mm]")
        ax.set_ylabel("r [mm]")
        ax.set_title(f"Event {evt} (≥1 hit per layer in region)")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(loc="best", fontsize=8)
        fig.tight_layout()
        fig.savefig(os.path.join(out_dir, f"event_{evt}.png"), dpi=150)
        plt.close(fig)

    print(f"Saved event_{evt}.png with {len(mdt_sel)} hits in region.")

# --- Save filtered hits ---
    if selected_hits:
        final_df = pd.concat(selected_hits, ignore_index=True)
        final_df.to_csv(output_csv, index=False)
        print(f"✅ Saved {len(final_df)} MDT hits from {len(final_df['event'].unique())} events to {output_csv}")
    else:
        print("⚠️ No events found with ≥1 MDT hit per layer inside ±12 cm region.")

