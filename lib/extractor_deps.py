import os
import subprocess


def extract_deps(path):

    print(f"-> Extracting deps for {path}")

    extract_pom_deps(path)

    return


def extract_pom_deps(path):

    subdirectories = get_subdirectories(path)

    for subdir in subdirectories:
        print(f"-> Extracting pom.xml deps for {subdir}")
        project = os.path.basename(subdir)
        call_mvn_deps(subdir, project)

    return


def extract_package_json_deps(path):

    print(f"-> Extracting package.json deps for {path}")

    return


def get_subdirectories(root_folder):
    subdirs = []
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for dirname in dirnames:
            subdir_path = os.path.join(dirpath, dirname)
            subdirs.append(subdir_path)
    return subdirs


def call_mvn_deps(path, project):

    command = ["sh", "utils/mvn_deps.sh", path, project]

    try:
        result = subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
