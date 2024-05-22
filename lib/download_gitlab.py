import os
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from lib import api_gitlab_repo

# Disabilita il warning per richieste HTTPS non verificate
urllib3.disable_warnings(InsecureRequestWarning)


def download_all_from_gitlab(data, group_name):

    groups = api_gitlab_repo.fetch_groups(data["gitlab_url"], data["token"])

    for group in groups:
        print("----------------------------------------------")
        print("Group: " + str(group["name"]))

        projects = api_gitlab_repo.fetch_projects_by_group(data["gitlab_url"], data["token"], group)

        for project in projects:
            download_from_gitlab(data, project, "pom.xml", group_name)
            download_from_gitlab(data, project, "package.json", group_name)


def download_from_gitlab(data, project, type, group_name):
    print("-- Project: " + str(project["name"]))

    if type == "pom.xml":
        download_pom_from_gitlab(data, project, data["token"], group_name)
    elif type == "package.json":
        download_package_json_from_gitlab(data, project, data["token"], group_name)


def download_pom_from_gitlab(data, project, token, group_name):

    branches = ["main", "master", "develop"]

    for branch in branches:
        print(f"---- Retrieving {project['pom_url']}{branch}")
        pom_file = api_gitlab_repo.fetch_project_file(f"{project['pom_url']}{branch}", token)

        if pom_file is not None:
            save_file(data, project, pom_file, "pom.xml", group_name)
            return


def download_package_json_from_gitlab(data, project, token, group_name):

    branches = ["main", "master", "develop"]

    for branch in branches:
        print(f"---- Retrieving {project['package_json_url']}{branch}")
        package_json_file = api_gitlab_repo.fetch_project_file(f"{project['package_json_url']}{branch}", token)

        if package_json_file is not None:
            save_file(data, project, package_json_file, "package.json", group_name)
            return


def save_file(data, project, content, type, group_name):

    filename = "pom.xml" if type == "pom.xml" else "package.json"

    path = data["output_path"] + "/" + group_name + "/projects/" + project["name"] + "/" + filename

    os.makedirs(os.path.dirname(path), exist_ok=True)

    print("---- Saving " + path)

    with open(path, "w") as text_file:
        text_file.write(content["content_decoded"])
