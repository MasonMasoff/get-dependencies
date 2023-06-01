# Gathers all public and private repos from specified org
# Gathers all dependencies for repos

import os
import requests
import csv
import variables
from tqdm import tqdm


def list_dependencies(owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/topics"
    headers = {
        "Accept": "application/vnd.github.mercy-preview+json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "names" in data:
            dependencies = data["names"]
            return dependencies
        else:
            return []
    else:
        return []

def get_all_organization_repositories(org, token):
    url = f"https://api.github.com/orgs/{org}/repos"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}"
    }

    repositories = []
    page = 1
    per_page = 100

    response = requests.get(url, headers=headers, params={"page": page, "per_page": per_page})
    total_repos = int(response.headers.get("X-Total-Count", 0))

    with tqdm(total=total_repos, desc="Fetching repositories") as pbar:
        while True:
            params = {"page": page, "per_page": per_page, "type": "all"}
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                if len(data) == 0:
                    break
                repositories.extend(data)
                page += 1
                pbar.update(len(data))
            else:
                break

    return repositories

# Example usage
repositories = get_all_organization_repositories(variables.organization, variables.access_token)

if repositories:

    if not os.path.exists(variables.csv_file_path):
        with open(variables.csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Repository", "Public Dependencies", "Private Dependencies"])

    with open(variables.csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        for repo in repositories:
            dependencies = list_dependencies(variables.organization, repo["name"], variables.access_token)
            public_dependencies = []
            private_dependencies = []
            for dependency in dependencies:
                if dependency.startswith("private-"):
                    private_dependencies.append(dependency)
                else:
                    public_dependencies.append(dependency)

            writer.writerow([f"{variables.organization}/{repo['name']}",
                             ', '.join(public_dependencies),
                             ', '.join(private_dependencies)])

    print(f"Repository list exported to '{variables.csv_file_path}'.")
else:
    print("No repositories found.")
