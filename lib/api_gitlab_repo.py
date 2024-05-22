import requests
import base64
from requests.exceptions import HTTPError


def fetch_groups(url, token):

    response = requests.get(url + "/groups", headers={"Private-Token": token}, verify=False)
    response.raise_for_status()
    groups = response.json()

    filtered_groups = [
        {
            "id": group["id"],
            "name": group["full_path"],
            "url": group["web_url"],
        }
        for group in groups
    ]

    return filtered_groups


def fetch_projects_by_group(url, token, group):

    response = requests.get(
        url + "/groups/" + str(group["id"]),
        headers={"Private-Token": token},
        verify=False,
    )
    response.raise_for_status()
    group = response.json()

    projects = group["projects"]

    filtered_projects = [
        {
            "id": project["id"],
            "name": project["name"],
            "url": project["web_url"],
            "pom_url": url + "/projects/" + str(project["id"]) + "/repository/files/pom.xml?ref=",
            "package_json_url": url + "/projects/" + str(project["id"]) + "/repository/files/package.json?ref=",
            "package_lock_json_url": url + "/projects/" + str(project["id"]) + "/repository/files/package-lock.json?ref=",
        }
        for project in projects
    ]

    return filtered_projects


def fetch_project_file(file_url, token):

    response = requests.get(
        file_url,
        headers={"Private-Token": token},
        verify=False,
    )
    file = response.json()

    if response.status_code == 404:
        return None

    return {
        "filename": file["file_name"],
        "content_encoded": file["content"],
        "content_decoded": base64.b64decode(file["content"]).decode("utf-8"),
    }
