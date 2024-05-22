import os
import csv
import json
import pandas as pd
import subprocess
from bs4 import BeautifulSoup


def create_csvs(root_path, projects_folder):

    create_csvs_from_txt(root_path, projects_folder)
    create_csvs_from_json(root_path, projects_folder)


def create_csvs_from_txt(root_path, projects_folder):
    subdirs = get_subdirectories(f"{root_path}/{projects_folder}")

    for subdir in subdirs:
        print(f"Creating csv for: {subdir}")
        create_csv_from_html(root_path, subdir)


def create_csv_from_txt(root, path):

    project = os.path.basename(path)
    content = read_file(f"{path}/{project}.txt")
    parse_txt_content_to_csv(content, f"{root}/csvs/{project}.mvn.csv")


def create_csv_from_html(root, path):

    project = os.path.basename(path)
    content = read_file(f"{path}/{project}.html")
    parse_html_content_to_csv(content, f"{root}/csvs/{project}.mvn.csv")


def create_csvs_from_json(root_path, projects_folder):
    subdirs = get_subdirectories(f"{root_path}/{projects_folder}")

    for subdir in subdirs:
        print(f"Creating csv for: {subdir}")
        create_csv_from_json(root_path, subdir)


def create_csv_from_json(root, path):
    project = os.path.basename(path)
    content = read_json_file(f"{path}/package.json")
    parse_json_content_to_csv(content, f"{root}/csvs/{project}.npm.csv")


def read_file(filename):

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
        if dirpath.find("node_modules") == -1 and dirpath.find("target") == -1:
            for dirname in dirnames:
                if dirname.find("node_modules") == -1 and dirname.find("target") == -1:
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


def parse_html_content_to_csv(data, nome_file_csv):

    if data is None:
        return

    # Parse the HTML content
    soup = BeautifulSoup(data, "html.parser")

    # Extract dependencies from the Project Dependencies section
    dependencies = []

    # Compile dependencies
    compile_section_el = soup.find("a", {"name": "Project_Dependencies_compile"})

    if compile_section_el is not None:
        compile_section = compile_section_el.find_next("section")
        compile_table = compile_section.find("table")
        for row in compile_table.find_all("tr")[1:]:
            cols = row.find_all("td")
            group_id = cols[0].text.strip()
            artifact_id = cols[1].text.strip()
            versions = cols[2].text.strip()
            license_links = cols[4].find_all("a")
            licenses = ", ".join([link.text for link in license_links]) if license_links else "-"
            dependencies.append(["maven", f"{group_id}:{artifact_id}", versions, licenses])

    # Runtime dependencies
    runtime_section_el = soup.find("a", {"name": "Project_Dependencies_runtime"})

    if runtime_section_el is not None:
        runtime_section = runtime_section_el.find_next("section")
        runtime_table = runtime_section.find("table")
        for row in runtime_table.find_all("tr")[1:]:
            cols = row.find_all("td")
            group_id = cols[0].text.strip()
            artifact_id = cols[1].text.strip()
            versions = cols[2].text.strip()
            license_links = cols[4].find_all("a")
            licenses = ", ".join([link.text for link in license_links]) if license_links else "-"
            dependencies.append(["maven", f"{group_id}:{artifact_id}", versions, licenses])

    # Test dependencies
    test_section_el = soup.find("a", {"name": "Project_Dependencies_test"})

    if test_section_el is not None:
        test_section = test_section_el.find_next("section")
        test_table = test_section.find("table")
        for row in test_table.find_all("tr")[1:]:
            cols = row.find_all("td")
            group_id = cols[0].text.strip()
            artifact_id = cols[1].text.strip()
            versions = cols[2].text.strip()
            license_links = cols[4].find_all("a")
            licenses = ", ".join([link.text for link in license_links]) if license_links else "-"
            dependencies.append(["maven", f"{group_id}:{artifact_id}", versions, licenses])

    # Create a DataFrame
    df = pd.DataFrame(dependencies, columns=["type", "library", "versions", "licenses"])

    # Save to CSV
    os.makedirs(os.path.dirname(nome_file_csv), exist_ok=True)

    df.to_csv(nome_file_csv, index=False)


def parse_json_content_to_csv(data, nome_file_csv):

    if data is None:
        return

    righe_csv = []

    # Aggiungi i dati da "dependencies"
    if "dependencies" in data:
        for library, version in data["dependencies"].items():
            project = os.path.basename(nome_file_csv).replace(".npm.csv", "")
            path = os.path.dirname(nome_file_csv).replace("csvs", project)

            version = version.replace("^", "").replace("~", "")

            license = call_package_json_licenses(path, library, version)

            righe_csv.append(["npm", library, version, license])

    # Aggiungi i dati da "devDependencies"
    if "devDependencies" in data:
        for library, version in data["devDependencies"].items():
            project = os.path.basename(nome_file_csv).replace(".npm.csv", "")
            path = os.path.dirname(nome_file_csv).replace("csvs", project)

            version = version.replace("^", "").replace("~", "")

            license = call_package_json_licenses(path, library, version)

            righe_csv.append(["npm", library, version, license])

    save_csv(righe_csv, nome_file_csv)


def save_csv(righe_csv, nome_file_csv):

    os.makedirs(os.path.dirname(nome_file_csv), exist_ok=True)

    print("---- Saving csv: " + nome_file_csv)

    # Scrittura del file CSV
    with open(nome_file_csv, "w", newline="") as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(["type", "library", "versions", "licenses"])  # Scrittura dell'intestazione
        for riga in righe_csv:
            writer.writerow(riga)  # Scrittura delle righe di dati


def call_package_json_licenses(path, library, version):

    script_dir = os.path.dirname(os.path.realpath(__file__))

    command = ["sh", "utils/package_json_licenses.sh", f"{script_dir}/../{path}", f"{library}@{version}"]

    try:
        result = subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.replace("\n", "")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return "-"
