import pandas as pd

df = pd.read_csv("event_585278_co_time.csv")
df.loc[df["tdcid"] == 2, "tdcid"] = 1
df.loc[df["tdcid"] == 4, "tdcid"] = 2
df.loc[df["tdcid"] == 7, "tdcid"] = 3
df.loc[df["tdcid"] == 10, "tdcid"] = 4
df.loc[df["tdcid"] == 13, "tdcid"] = 5
df.loc[df["tdcid"] == 15, "tdcid"] = 6
df.to_csv("event_modified.csv", index=False)
