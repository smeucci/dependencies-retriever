import os
import json
import argparse
import time
from datetime import datetime
from lib import download_gitlab, extractor_deps, csv_creator, csv_processor, download_svn

script_dir = os.path.dirname(os.path.realpath(__file__))


def load_config(repo_name):
    with open(os.path.join(script_dir, "config/config.json"), "r") as file:
        config = json.load(file)
    return config.get(repo_name)


def process_gitlab(repo_name, download=False, extract=False, create=False, process=False):
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


def process_svns(repo_name, download=False, extract=False, create=False, process=False):

    data = load_config(repo_name)
    if not data:
        print(f"No configuration found for {repo_name}")
        return

    for repo in data["repos"]:
        process_svn(repo, data, download, extract, create, process)


def process_svn(repo_name, data, download=False, extract=False, create=False, process=False):

    # Full paths
    data["repo_name"] = repo_name
    data["output_path"] = "data/output"
    data["projects_output_path"] = os.path.join(data["output_path"], data["repo_name"], "projects")
    data["repo_path"] = os.path.join(data["output_path"], data["repo_name"])
    data["csv_output_path"] = os.path.join(data["output_path"], data["repo_name"], "csvs")
    data["final_csv_output"] = os.path.join(data["output_path"], data["repo_name"], f"{data['repo_name']}-libs.csv")

    if download:
        download_svn.download_all_from_svn(data, repo_name)

    if extract:
        extractor_deps.extract_deps(data["projects_output_path"])

    if create:
        csv_creator.create_csvs(data["repo_path"], "projects")

    if process:
        csv_processor.merge_csv_files(data["csv_output_path"], data["final_csv_output"])


def merge_only(folder_path, output_file):
    csv_processor.merge_csv_files(folder_path, output_file)


def main():
    parser = argparse.ArgumentParser(description="Processa i repositories specificati.")
    parser.add_argument("--repo-name", type=str, help="Nome del repository da processare")
    parser.add_argument("--repo-type", type=str, help="Tipo di repository: gitlab, svn")
    parser.add_argument("--download", action="store_true", help="Scarica i dati")
    parser.add_argument("--extract", action="store_true", help="Estrai le dipendenze")
    parser.add_argument("--create", action="store_true", help="Crea i file CSV")
    parser.add_argument("--process", action="store_true", help="Elabora i file CSV")
    parser.add_argument("--all", action="store_true", help="Esegue tutti gli step: download, extract, create, process")
    parser.add_argument("--merge-only", type=str, help="Specifica la cartella contenente i CSV da unire")

    args = parser.parse_args()

    if args.merge_only:
        output_file = os.path.join(args.merge_only, "merged_output.csv")
        merge_only(args.merge_only, output_file)
        return

    if args.all:
        args.download = args.extract = args.create = args.process = True

    if not args.repo_name:
        parser.error("the following arguments are required: --repo_name")

    if not args.repo_type:
        parser.error("the following arguments are required: --repo_type")

    start_time = time.time()
    start_timestamp = datetime.now()

    if args.repo_type == "gitlab":
        process_gitlab(args.repo_name, args.download, args.extract, args.create, args.process)
    elif args.repo_type == "svn":
        process_svns(args.repo_name, args.download, args.extract, args.create, args.process)
    else:
        print(f"Nessun tipo repository corrispondente a: {args.repo_type}")

    end_time = time.time()
    end_timestamp = datetime.now()
    duration = end_time - start_time

    print(f"\nScript started at {start_timestamp.strftime('%Y-%m-%d %H:%M:%S')} and ended at {end_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total execution time: {duration/60:.2f} minutes")


if __name__ == "__main__":
    main()
