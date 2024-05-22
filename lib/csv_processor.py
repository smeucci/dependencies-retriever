import csv
import os
from collections import defaultdict


def merge_csv_files(folder_path, output_file):

    print(f"-- Merging all csv file from folder {folder_path} in file {output_file}")

    libraries = defaultdict(lambda: defaultdict(set))  # defaultdict annidato per gestire 'type', 'library' e 'versions'

    # Scansione dei file nella directory
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):  # Verifica che sia un file CSV
            with open(os.path.join(folder_path, filename), "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Split delle versioni e aggiunta al set per evitare duplicati
                    current_versions = set(row["versions"].split(","))
                    libraries[row["type"]][row["library"]].update(current_versions)

    # Preparazione della lista delle righe da scrivere, ordinata per 'type'
    rows = []
    for type_key, libs in sorted(libraries.items()):
        for library, versions in sorted(libs.items()):
            rows.append({"type": type_key, "library": library, "versions": ",".join(sorted(versions))})

    # Scrittura del file CSV finale
    with open(output_file, "w", newline="") as file:
        fieldnames = ["type", "library", "versions"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)  # Scrittura delle righe ordinate
