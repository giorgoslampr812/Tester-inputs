import numpy as np
import csv

# Parameters
t_max = 131072
mean_spacing = 6400
n_events = 144

rng = np.random.default_rng()

rows = []

for event_id in range(n_events):

    # Compute IDs from event number
    tdcid = event_id // 24 + 1   # 1–6
    chnlid = event_id % 24       # 0–23

    t = 0

    while True:
        dt = rng.exponential(mean_spacing)
        t += dt

        if t >= t_max:
            break

        rows.append([
            event_id,
            int(t),
            tdcid,
            chnlid
        ])

# Save CSV
with open("pseudodata.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["event", "time", "tdcid", "chnlid"])
    writer.writerows(rows)

print("Saved pseudodata.csv")

