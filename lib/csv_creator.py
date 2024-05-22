import os
import csv
import json


def create_csvs(root_path, projects_folder):

    create_csvs_from_txt(root_path, projects_folder)
    create_csvs_from_json(root_path, projects_folder)


def create_csvs_from_txt(root_path, projects_folder):
    subdirs = get_subdirectories(f"{root_path}/{projects_folder}")

    for subdir in subdirs:
        create_csv_from_txt(root_path, subdir)


def create_csv_from_txt(root, path):

    project = os.path.basename(path)
    content = read_txt_file(f"{path}/{project}.txt")
    parse_txt_content_to_csv(content, f"{root}/csvs/{project}.mvn.csv")


def create_csvs_from_json(root_path, projects_folder):
    subdirs = get_subdirectories(f"{root_path}/{projects_folder}")

    for subdir in subdirs:
        create_csv_from_json(root_path, subdir)


def create_csv_from_json(root, path):
    project = os.path.basename(path)
    content = read_json_file(f"{path}/package.json")
    parse_json_content_to_csv(content, f"{root}/csvs/{project}.npm.csv")


def read_txt_file(filename):

    try:

        with open(filename, "r") as file:
            content = file.read()
        return content

    except:
        return None


def read_json_file(filename):

    try:

        with open(filename, "r") as file:
            # Caricamento dei dati JSON
            data = json.load(file)
            return data

    except:
        return None


def get_subdirectories(root_folder):
    subdirs = []
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for dirname in dirnames:
            subdir_path = os.path.join(dirpath, dirname)
            subdirs.append(subdir_path)
    return subdirs


def parse_txt_content_to_csv(data, nome_file_csv):

    if data is None:
        return

    # Creazione di una lista per memorizzare le righe del CSV
    righe_csv = []

    # Split del contenuto in righe
    righe = data.split("\n")

    # Parsing delle righe
    for riga in righe:
        if riga.strip():  # Verifica che la riga non sia vuota
            parts = riga.split(":")
            if len(parts) >= 5:  # Assicurarsi che la riga sia nel formato atteso
                # Estrazione delle componenti necessarie
                library = f"{parts[0].strip()}:{parts[1].strip()}"
                version = parts[3].strip()

                # Aggiunta alla lista CSV
                righe_csv.append(["maven", library, version])

    save_csv(righe_csv, nome_file_csv)


def parse_json_content_to_csv(data, nome_file_csv):

    if data is None:
        return

    righe_csv = []

    # Aggiungi i dati da "dependencies"
    if "dependencies" in data:
        for library, version in data["dependencies"].items():
            righe_csv.append(["npm", library, version])

    # Aggiungi i dati da "devDependencies"
    if "devDependencies" in data:
        for library, version in data["devDependencies"].items():
            righe_csv.append(["npm", library, version])

    save_csv(righe_csv, nome_file_csv)


def save_csv(righe_csv, nome_file_csv):

    os.makedirs(os.path.dirname(nome_file_csv), exist_ok=True)

    print("---- Saving csv: " + nome_file_csv)

    # Scrittura del file CSV
    with open(nome_file_csv, "w", newline="") as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(["type", "library", "versions"])  # Scrittura dell'intestazione
        for riga in righe_csv:
            writer.writerow(riga)  # Scrittura delle righe di dati
