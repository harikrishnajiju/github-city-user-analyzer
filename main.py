import requests
import csv
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

# Define API endpoint and headers for authorization
GITHUB_API = "https://api.github.com"
headers = {"Authorization": f"token {token}"}

def get_github_users(city, followers_min):
    users = []
    page = 1
    print(f"Fetching GitHub users in {city} with over {followers_min} followers...")
    while True:
        response = requests.get(
            f"{GITHUB_API}/search/users?q=location:{city}+followers:>={followers_min}&page={page}&per_page=100",
            headers=headers
        )
        if response.status_code != 200:
            print(f"Error fetching users: {response.status_code} - {response.json().get('message', '')}")
            break
        data = response.json().get("items", [])
        if not data:
            break
        users.extend(data)
        print(f"Fetched {len(data)} users from page {page}")
        page += 1
    print(f"Total users fetched: {len(users)}")
    return users

def get_user_details(user_login):
    response = requests.get(f"{GITHUB_API}/users/{user_login}", headers=headers)
    if response.status_code != 200:
        print(f"Error fetching user details for {user_login}: {response.status_code}")
        return {}
    user_details = response.json()
    
    # Clean `company` field
    company = (user_details.get("company") or "").strip().lstrip("@").upper()
    user_details["company"] = company
    return user_details

def get_user_repositories(user_login):
    repos = []
    page = 1
    print(f"Fetching repositories for user: {user_login}")
    while len(repos) < 500:
        response = requests.get(f"{GITHUB_API}/users/{user_login}/repos?page={page}&per_page=100", headers=headers)
        if response.status_code != 200:
            print(f"Error fetching repositories for {user_login}: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        repos.extend(data)
        print(f"Fetched {len(data)} repos from page {page} for user {user_login}")
        page += 1
    print(f"Total repositories fetched for {user_login}: {len(repos)}")
    return repos[:500]  # Limit to 500 most recent repos

def save_users_to_csv(users):
    print("Saving user data to users.csv...")
    with open("users.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["login", "name", "company", "location", "email", "hireable", "bio", 
                         "public_repos", "followers", "following", "created_at"])
        for i, user in enumerate(users, start=1):
            details = get_user_details(user['login'])
            if details:
                writer.writerow([
                    details.get("login", ""), details.get("name", ""), details.get("company", ""),
                    details.get("location", ""), details.get("email", ""), details.get("hireable", ""),
                    details.get("bio", ""), details.get("public_repos", ""), details.get("followers", ""),
                    details.get("following", ""), details.get("created_at", "")
                ])
            print(f"Processed {i}/{len(users)} users")
    print("User data saved to users.csv")

def save_repositories_to_csv(users):
    print("Saving repository data to repositories.csv...")
    with open("repositories.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["login", "full_name", "created_at", "stargazers_count", "watchers_count", 
                         "language", "has_projects", "has_wiki", "license_name"])
        for i, user in enumerate(users, start=1):
            repos = get_user_repositories(user['login'])
            for repo in repos:
                # Handle None for the license field
                license_name = repo.get("license")["name"] if repo.get("license") else ""
                
                writer.writerow([
                    repo["owner"]["login"],
                    repo.get("full_name", ""),
                    repo.get("created_at", ""),
                    repo.get("stargazers_count", ""),
                    repo.get("watchers_count", ""),
                    repo.get("language", ""),
                    repo.get("has_projects", ""),
                    repo.get("has_wiki", ""),
                    license_name
                ])
            print(f"Processed repositories for {i}/{len(users)} users")
    print("Repository data saved to repositories.csv")


if __name__ == "__main__":
    # Specify the city and follower threshold
    city = "Basel"
    followers_min = 10
    
    # Fetch users and save data to CSVs
    users = get_github_users(city, followers_min)
    save_users_to_csv(users)
    save_repositories_to_csv(users)
