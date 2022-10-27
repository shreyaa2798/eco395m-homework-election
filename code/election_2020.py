import csv
import os

IN_PATH = os.path.join("data", "countypres_2000-2020.csv")
OUTPUT_DIR = "artifacts"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "election_report.csv")


def count_votes(path):

    with open(IN_PATH, "r") as in_file:
        counts = {}

        dict_reader = csv.DictReader(in_file)

        for row in dict_reader:
            year = row["year"]
            state = row["state_po"]
            candidate = row["candidate"]
            votes = row["candidatevotes"]
            mode = row["mode"]

            key = (year, state, candidate)
            

            if not votes == "NA" and year == "2020":
                votes_int = int(votes)

                if key in counts:
                    counts[key] += votes_int
                else:
                    counts[key] = votes_int

    return counts


def get_rows(counts):

    rows = []
    for key, votes in counts.items():
        row = [*key, votes]
        rows.append(row)

    return rows


def sort_rows(rows):

    state_code_index = 1
    votes_index = 3

    rows_votes_ordered = sorted(rows, key=lambda row: row[votes_index], reverse=True)
    rows_lex_ordered = sorted(rows_votes_ordered, key=lambda row: row[state_code_index])

    return rows_lex_ordered


def write_rows(rows):

    with open(OUTPUT_PATH, "w+") as out_file:
        csv_writer = csv.writer(out_file)
        csv_writer.writerow(["year", "state_code", "candidate", "votes"])
        csv_writer.writerows(rows)

if __name__ == "__main__":

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    counts = count_votes(IN_PATH)
    rows = get_rows(counts)
    sorted_rows = sort_rows(rows)
    write_rows(sorted_rows)
