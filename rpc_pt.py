import numpy as np
import pandas as pd
import os

# --------------------------
# Constants
# --------------------------
B = 0.5  # Tesla


# --------------------------
# pT threshold function
# --------------------------
def get_pt_threshold(pt):
    if pt < 4:
        return 0
    elif pt > 80:
        return 15
    elif pt > 40:
        return 12
    elif pt > 30:
        return 12
    elif pt > 25:
        return 12
    elif pt > 20:
        return 10
    elif pt > 18:
        return 9
    elif pt > 15:
        return 8
    elif pt > 12:
        return 7
    elif pt > 10:
        return 6
    elif pt > 9:
        return 5
    elif pt > 8:
        return 4
    elif pt > 7:
        return 4
    else:
        return 0


# --------------------------
# Circle fit
# --------------------------
def fit_circle(x, y):
    A = np.c_[2*x, 2*y, np.ones(len(x))]
    b = x**2 + y**2

    c, *_ = np.linalg.lstsq(A, b, rcond=None)
    xc, yc, d = c

    R = np.sqrt(xc**2 + yc**2 + d)
    return R, xc, yc


# --------------------------
# Event processing (rpc_radii passed dynamically)
# --------------------------
def compute_event(row, rpc_radii):
    z_hits = np.array([
        row["z_RPC0"],
        row["z_RPC1"],
        row["z_RPC2"],
        row["z_RPC3"]
    ])

    mask = z_hits != 0
    if np.sum(mask) < 3:
        return pd.Series([np.nan, 0, np.nan, "insufficient_hits"])

    r = np.array(rpc_radii)[mask]
    z = z_hits[mask]

    try:
        R_mm, xc, yc = fit_circle(r, z)

        if R_mm <= 0 or not np.isfinite(R_mm):
            return pd.Series([np.nan, 0, np.nan, "bad_fit"])

        R_m = R_mm / 1000.0
        pt = 0.3 * B * R_m

        charge = np.sign(xc)
        if charge == 0:
            charge = 1

        pt_thr = get_pt_threshold(pt)

        return pd.Series([pt, pt_thr, charge, "ok"])

    except:
        return pd.Series([np.nan, 0, np.nan, "fit_failure"])


# --------------------------
# Batch loop
# --------------------------
for side in ["A", "C"]:
 for i in range(1, 17):

    in_file = f"B_{side}_{i}/B_{side}_{i}_rpc.csv"
    out_file = f"B_{side}_{i}/B_{side}_{i}_rpc_with_pt_charge.csv"

    if not os.path.exists(in_file):
        print(f"[SKIP] Missing file: {in_file}")
        continue

    # --------------------------
    # Geometry selection
    # --------------------------
    if i % 2 == 0:
        rpc_radii = [4700, 7700, 8400, 9900]
    else:
        rpc_radii = [5200, 6800, 7580, 9900]

    print(f"[PROCESSING] {in_file} | rpc_radii = {rpc_radii}")

    df = pd.read_csv(in_file, comment="#")

    df[["pT_GeV", "pt_threshold", "charge", "fit_status"]] = df.apply(
        compute_event,
        axis=1,
        args=(rpc_radii,)
    )

    df.to_csv(out_file, index=False)

    print(f"[DONE] Saved -> {out_file}")
