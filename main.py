import os
import json
import argparse
from lib import download_gitlab, extractor_deps, csv_creator, csv_processor

script_dir = os.path.dirname(os.path.realpath(__file__))


def load_config(repo_name):
    with open(os.path.join(script_dir, "config/config.json"), "r") as file:
        config = json.load(file)
    return config.get(repo_name)


def process(repo_name, download=False, extract=False, create=False, process=False):
    data = load_config(repo_name)
    if not data:
        print(f"No configuration found for {repo_name}")
        return

    # Full paths
    data["cert_path"] = "data/cert/cert.pem"
    data["output_path"] = "data/output"
    data["projects_output_path"] = os.path.join(data["output_path"], data["repo_name"], "projects")
    data["repo_path"] = os.path.join(data["output_path"], data["repo_name"])
    data["csv_output_path"] = os.path.join(data["output_path"], data["repo_name"], "csvs")
    data["final_csv_output"] = os.path.join(data["output_path"], data["repo_name"], f"{data['repo_name']}-libs.csv")

    if download:
        download_gitlab.download_all_from_gitlab(data, data["repo_name"])

    if extract:
        extractor_deps.extract_deps(data["projects_output_path"])

    if create:
        csv_creator.create_csvs(data["repo_path"], "projects")

    if process:
        csv_processor.merge_csv_files(data["csv_output_path"], data["final_csv_output"])


def main():
    parser = argparse.ArgumentParser(description="Processa i repositories specificati.")
    parser.add_argument("repo_name", type=str, help="Nome del repository da processare")
    parser.add_argument("repo_type", type=str, help="Tipo di repository: gitlab, svn")
    parser.add_argument("--download", action="store_true", help="Scarica i dati")
    parser.add_argument("--extract", action="store_true", help="Estrai le dipendenze")
    parser.add_argument("--create", action="store_true", help="Crea i file CSV")
    parser.add_argument("--process", action="store_true", help="Elabora i file CSV")
    parser.add_argument("--all", action="store_true", help="Esegue tutti gli step: download, extract, create, process")

    args = parser.parse_args()

    if args.all:
        args.download = args.extract = args.create = args.process = True

    if args.repo_type == "gitlab":
        process(args.repo_name, args.download, args.extract, args.create, args.process)
    else:
        print(f"Nessun tipo repository corrispondente a: {args.repo_type}")


if __name__ == "__main__":
    main()
