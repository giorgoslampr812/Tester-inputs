import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


DELTA_ETA = 0.1


def get_eta_from_rz(r, z):
    theta = np.arctan2(r, z)
    return -np.log(np.tan(theta / 2.0))


def get_layer(r):
    if r < 5550:
        return 1
    elif r < 9500:
        return 2
    else:
        return 3


for i in range(1, 17):

    mdt_file = f"B_A_{i}/B_A_{i}_csm.csv"
    rpc_file = f"B_A_{i}/B_A_{i}_rpc.csv"
    output_csv = f"filtered_events_eta_A/mdt_hits_within_offsets_per_layer_{i}.csv"

    out_dir = "event_hitmaps_selected_eta_A"
    os.makedirs(out_dir, exist_ok=True)

    mdt_df = pd.read_csv(mdt_file, skiprows=6)
    rpc_df = pd.read_csv(rpc_file, skiprows=6)

    common_events = sorted(
        set(mdt_df["event"]).intersection(set(rpc_df["event"]))
    )

    print(f"[B_A_{i}] common events: {len(common_events)}")

    selected_hits = []
    plot_counter = 0   

    for evt in common_events:

        mdt_evt = mdt_df[mdt_df["event"] == evt]
        rpc_evt = rpc_df[rpc_df["event"] == evt]

        if mdt_evt.empty or rpc_evt.empty:
            continue

        rpc_row = rpc_evt.iloc[0]
        
        eta_rpc = rpc_row.get("Eta", np.nan)

        #Eta check to select different eta regions 
        #Phi is selected by sector 
        eta_low = 0.59 
        eta_high= 0.60 
        #if eta_rpc < eta_low or eta_rpc > eta_high: 
        #  continue
        if np.isnan(eta_rpc):
            continue

        # --------------------------
        # MDT η reconstruction
        # --------------------------
        r = mdt_evt["tube_rho"].values
        z = mdt_evt["tube_z"].values

        valid = (r > 0) & (z != 0)

        eta_mdt = np.full(len(mdt_evt), np.nan)
        eta_mdt[valid] = get_eta_from_rz(r[valid], z[valid])

        mdt_evt = mdt_evt.copy()
        mdt_evt["eta_mdt"] = eta_mdt

        mask = np.abs(mdt_evt["eta_mdt"] - eta_rpc) < DELTA_ETA
        mdt_sel = mdt_evt[mask].copy()

        if mdt_sel.empty:
            continue

        mdt_sel["layer"] = mdt_sel["tube_rho"].apply(get_layer)
        layer_counts = mdt_sel.groupby("layer").size()

        if not all(l in layer_counts.index for l in [1, 2, 3]):
            continue

        selected_hits.append(mdt_sel)

        # --------------------------
        # SAVE ONLY FIRST 20 PLOTS
        # --------------------------
        if plot_counter < 20:

            fig, ax = plt.subplots(figsize=(8, 6))

            ax.scatter(
                mdt_evt["tube_z"], mdt_evt["tube_rho"],
                c="gray", marker="x", s=25,
                label="All MDT hits"
            )

            ax.scatter(
                mdt_sel["tube_z"], mdt_sel["tube_rho"],
                facecolors="none", edgecolors="red",
                s=80, linewidths=1.2,
                label="MDT η-matched"
            )

            ax.set_title(f"Event {evt} (η matching)")
            ax.set_xlabel("z [mm]")
            ax.set_ylabel("r [mm]")
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.legend()

            fig.tight_layout()
            fig.savefig(os.path.join(out_dir, f"B_A_{i}_event_{evt}.png"), dpi=150)
            plt.close(fig)

            plot_counter += 1   # 👈 INCREMENT

    # --------------------------
    # Save CSV
    # --------------------------
    if selected_hits:
        final_df = pd.concat(selected_hits, ignore_index=True)
        final_df.to_csv(output_csv, index=False)

        print(
            f"✅ Saved {len(final_df)} MDT hits "
            f"from {len(final_df['event'].unique())} events → {output_csv}"
        )
    else:
        print("⚠️ No η-matched events found.")
