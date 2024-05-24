import os
import subprocess


def download_all_from_svn(data, repo_name):

    svn_url = data["svn_url"] + "/" + repo_name
    username = data["username"]
    password = data["password"]
    local_base_dir = data["output_path"] + "/" + repo_name + "/projects"

    # Esplora il repository SVN
    files = explore_svn_repository(svn_url, username, password)

    # Filtra i file 'pom.xml' e 'package.json'
    target_files = ["pom.xml", "package.json", "package-lock.json"]
    filtered_files = [f for f in files if any(tf in f for tf in target_files)]

    # Esporta i file specificati
    for file in filtered_files:
        file_url = f"{svn_url}/{file}"
        local_path = os.path.join(local_base_dir, file)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        export_svn_file(file_url, local_path, username, password)
        print(f"Exported {file_url} to {local_path}")


# Funzione per eseguire il comando SVN
def run_svn_command(command):
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout


# Funzione per esplorare il repository SVN
def explore_svn_repository(url, user, pwd):
    command = ["svn", "list", url, "--recursive", "--username", user, "--password", pwd, "--non-interactive"]
    return run_svn_command(command).splitlines()


# Funzione per esportare i file specificati
def export_svn_file(url, local_path, user, pwd):
    command = ["svn", "export", url, local_path, "--username", user, "--password", pwd, "--non-interactive"]
    subprocess.run(command, check=True)
