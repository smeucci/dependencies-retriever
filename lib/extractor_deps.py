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

    subdirectories = get_subdirectories(path)

    for subdir in subdirectories:
        print(f"-> Extracting package.json deps for {subdir}")
        project = os.path.basename(subdir)
        call_package_json_deps(subdir, project)

    return


def get_subdirectories(root_folder):
    subdirs = []
    for dirpath, dirnames, filenames in os.walk(root_folder):
        if dirpath.find("node_modules") == -1 and dirpath.find("target") == -1:
            for dirname in dirnames:
                if dirname.find("node_modules") == -1 and dirname.find("target") == -1:
                    subdir_path = os.path.join(dirpath, dirname)
                    subdirs.append(subdir_path)
    return subdirs


def call_mvn_deps(path, project):

    command = ["sh", "utils/mvn_deps_and_licenses.sh", path, project]

    try:
        result = subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def call_package_json_deps(path, project):

    command = ["sh", "utils/npm_install.sh", path, project]

    try:
        result = subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
