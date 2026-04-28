import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend for server use
import matplotlib.pyplot as plt
import numpy as np
import os

for i in range(1,17):
# --- Input CSV files ---
 mdt_csv = f"two_mezz_events_A/mdt_hits_filtered_top2mezz_per_layer_{i}.csv"
 rpc_csv = f"B_A_{i}/B_A_{i}_rpc.csv"
 output_dir = f"event_plots_mezz_colored"

 os.makedirs(output_dir, exist_ok=True)

# --- Load data ---

 df_mdt = pd.read_csv(mdt_csv,skiprows = 0)
 df_rpc = pd.read_csv(rpc_csv,skiprows = 6)

# Ensure common events
 common_events = sorted(set(df_mdt["event"]).intersection(df_rpc["event"]))
 print(f"Found {len(common_events)} common events.")

# --- Define unique colors for mezzanines ---
 unique_mezz = sorted(df_mdt["mezz"].unique())
 cmap = plt.get_cmap("tab20", len(unique_mezz))
 mezz_colors = {mezz: cmap(i) for i, mezz in enumerate(unique_mezz)}

# --- Fixed RPC radii ---
 if i%2 == 0:
  rpc_radii = [4700, 7700,8400, 9900]
 else:
  rpc_radii = [5200, 6800,7580, 9900]

# --- Plot loop ---
 for k, evt in enumerate(common_events):
    evt_mdt = df_mdt[df_mdt["event"] == evt]
    evt_rpc = df_rpc[df_rpc["event"] == evt]

    plt.figure(figsize=(8, 8))
    
    # --- Plot MDT hits ---
    for mezz in sorted(evt_mdt["mezz"].unique()):
        mezz_hits = evt_mdt[evt_mdt["mezz"] == mezz]
        plt.scatter(
            mezz_hits["tube_z"], mezz_hits["tube_rho"],
            color=mezz_colors[mezz], marker='x', s=40,
            label=f"Mezz {mezz}"
        )
    
    # --- Plot RPC hits ---
    if not evt_rpc.empty:
        rpc_z = evt_rpc[["z_RPC0", "z_RPC1", "z_RPC2", "z_RPC3"]].iloc[0].values
        for j, z in enumerate(rpc_z):
            if not np.isnan(z):
                plt.scatter(z, rpc_radii[j], color="black", marker="o", s=60, label="RPC hit" if j == 0 else "")

        # --- Draw line from IP to RPC0 ---
        plt.plot([0, rpc_z[0]], [0, rpc_radii[0]], color="gray", linestyle="--", label="IP–RPC0")

    plt.xlabel("z [mm]")
    plt.ylabel("r [mm]")
    plt.title(f"Event {evt} — MDT hits colored by Mezzanine")
    plt.legend(loc="best", fontsize=8)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()

    output_path = os.path.join(output_dir, f"sector_{i}_event_{evt}.png")
    plt.savefig(output_path, dpi=150)
    plt.close()
    if k == 10: break
    if k < 5:
        print(f"Saved plot for event {evt}")

print(f"✅ Saved {len(common_events)} plots to directory: {output_dir}")

