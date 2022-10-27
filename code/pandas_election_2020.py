import os
import pandas as pd

IN_PATH = os.path.join("data", "countypres_2000-2020.csv")
OUTPUT_DIR = "artifacts"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "election_report_pandas.csv")

if __name__ == "__main__":
    (
        pd.read_csv(IN_PATH)
        .rename(columns={"state_po": "state_code", "candidatevotes": "votes"})
        .dropna(subset=["candidatevotes"])
        .assign(votes= lambda df: df["votes"].astype("int"))
        .loc[lambda df: df["year" == 2020]]
        .groupby(["year", "state_code", "candidate"])["votes"]
        .sum()
        .reset_index()
        .sort_values(by=["state_code", "votes"], ascending= [True, False])
        .to_csv(OUTPUT_PATH, index=False)
    )
