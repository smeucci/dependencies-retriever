import csv
import os
from collections import defaultdict


keywords_to_exclude = ["movyon", "autostrade"]


def merge_csv_files(folder_path, output_file):

    print(f"-- Merging all csv file from folder {folder_path} in file {output_file}")

    # defaultdict annidato per gestire 'type', 'library' e 'versions'
    libraries = defaultdict(lambda: defaultdict(set))

    # Scansione dei file nella directory
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):  # Verifica che sia un file CSV
            with open(os.path.join(folder_path, filename), "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:

                    if should_exclude(row["library"]):
                        continue

                    # Split delle versioni e aggiunta al set per evitare duplicati
                    current_versions = set(row["versions"].split(","))
                    current_licenses = set(row["licenses"].split(",")) if row["licenses"] != "-" else set()
                    libraries[row["type"], row["library"]]["versions"].update(current_versions)
                    libraries[row["type"], row["library"]]["licenses"].update(current_licenses)

    # Preparazione della lista delle righe da scrivere, ordinata per 'type'
    rows = []
    for (type_key, library), info in sorted(libraries.items()):
        versions = ",".join(sorted(info["versions"]))
        licenses = ",".join(sorted(info["licenses"])) if info["licenses"] else "-"
        rows.append({"type": type_key, "library": library, "versions": versions, "licenses": licenses})

    # Scrittura del file CSV finale
    with open(output_file, "w", newline="") as file:
        fieldnames = ["type", "library", "versions", "licenses"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)  # Scrittura delle righe ordinate


def should_exclude(library):
    return any(keyword in library for keyword in keywords_to_exclude)
