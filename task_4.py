#task 2.4

import requests
import json
import os


# Константы
GITHUB_API_URL = "https://api.github.com"
SAVE_FILE = "resource/result/github_data.json"
MAX_PASS_LINE = [0, 100]


#Функция быстрый вывод частых сообщений
def say(mode0=None, mode1="\n"):
    if mode0 in range(MAX_PASS_LINE[0], MAX_PASS_LINE[1]):
        print(mode1 * mode0)
    elif mode0 == "s":
        print("<--- Beginning work Program --->\n")
    elif mode0 == "e":
        print("\n<--- End work Program --->")
    elif mode0 == "er":
        if mode1 == "req":
            print("Error. GitHub API request failed!\n")
        elif mode1 == "user":
            print("Error. User NOT FOUND!\n")
        elif mode1 == "empty":
            print("Error. Input CANNOT be empty!\n")
        elif mode1 == "mode":
            print("Error. Mode NOT FOUND !\n")
        elif mode1 == "save":
            print("Error. Failed to SAVE file!\n")
        elif mode1 == "load":
            print("Error. Failed to LOAD file!\n")


#Функция ввод строки с проверкой
def input_string(text):
    while True:
        input_str = input(f"> {text}")
        if input_str.strip() == "":
            say("er", "empty")
            continue
        return input_str.strip()


#Функция выполнение запроса к GitHub API
def make_github_request(url):
    try:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Python-GitHub-App"
        }
        response = requests.get(url, headers = headers, timeout = 10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            say("er", "user")
            return {}
        else:
            say("er", "req")
            return {}
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        say("er", "req")
        return {}


#Функция получение профиля пользователя
def get_user_profile(username):
    url = f"{GITHUB_API_URL}/users/{username}"
    data = make_github_request(url)
    if data is None:
        return None

    profile = {
        "username": data.get("login", "N/A"),
        "name": data.get("name", "Not specified"),
        "profile_url": data.get("html_url", "N/A"),
        "repos_count": data.get("public_repos", 0),
        "gists_count": data.get("public_gists", 0),
        "following_count": data.get("following", 0),
        "followers_count": data.get("followers", 0),
        "created_at": data.get("created_at", "N/A"),
        "company": data.get("company", "Not specified"),
        "location": data.get("location", "Not specified"),
        "bio": data.get("bio", "Not specified")
    }
    return profile


#Функция получение репозиториев пользователя
def get_user_repositories(username):
    url = f"{GITHUB_API_URL}/users/{username}/repos?per_page=100&sort=updated"
    data = make_github_request(url)
    if data is None:
        return None

    repositories = []
    for i in data:
        repo_info = {
            "name": i.get("name", "N/A"),
            "url": i .get("html_url", "N/A"),
            "language": i .get("language", "Not specified"),
            "visibility": "Public" if not i .get("private", False) else "Private",
            "default_branch": i .get("default_branch", "N/A"),
            "stars": i .get("stargazers_count", 0),
            "forks": i .get("forks_count", 0),
            "description": i.get("description", "No description")
        }
        repositories.append(repo_info)
    return repositories


#Функция Поиск репозиториев по названию
def search_repositories(query):
    url = f"{GITHUB_API_URL}/search/repositories?q={query}&per_page=20"
    data = make_github_request(url)
    if data is None:
        return None

    repositories = []
    for repo in data.get("items", []):
        repo_info = {
            "full_name": repo.get("full_name", "N/A"),
            "url": repo.get("html_url", "N/A"),
            "language": repo.get("language", "Not specified"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "description": repo.get("description", "No description"),
            "owner": repo.get("owner", {}).get("login", "N/A")
        }
        repositories.append(repo_info)
    return repositories


#Функция сохранение профиля в JSON
def save_profile_to_file(profile):
    try:
        os.makedirs(os.path.dirname(SAVE_FILE), exist_ok = True)
        with open(SAVE_FILE, 'w') as f:
            json.dump(profile, f, ensure_ascii = False, indent = 4)
        print(f"\nProfile saved to {SAVE_FILE}\n")
    except FileNotFoundError:
        say("er", "save")


#Фукнция просмотр профиля пользователя
def show_user_profile():
    print("\n-- View User Profile --\n")
    username = input_string("Enter GitHub username: ")
    profile = get_user_profile(username)
    if profile is None:
        return

    print(f"Profile: {profile['username']}\n")
    print(f"Name:           {profile['name']}")
    print(f"Profile URL:    {profile['profile_url']}")
    print(f"Bio:            {profile['bio']}")
    print(f"Location:       {profile['location']}")
    print(f"Company:        {profile['company']}")
    print(f"Created:        {profile['created_at'][:10]}")
    print(f"Public Repos:   {profile['repos_count']}")
    print(f"Public Gists:   {profile['gists_count']}")
    print(f"Following:      {profile['following_count']}")
    print(f"Followers:      {profile['followers_count']}\n")
    select_mode = input("Save this profile to file? (y/n): ").strip().lower()
    if select_mode == 'y':
        save_profile_to_file(profile)


#Функция просмотр репозиториев пользователя
def show_user_repositories():
    print("\n-- View User Repositories --\n")
    username = input_string("Enter GitHub username: ")
    repos = get_user_repositories(username)
    if repos is None:
        return

    if not repos:
        print(f"\nUser '{username}' has no public repositories\n")
        return

    print(f"\nFound {len(repos)} repositories for '{username}':")
    say(1)
    for i, repo in enumerate(repos, 1):
        print(f"{i}. {repo['name']}")
        print(f"   URL:           {repo['url']}")
        print(f"   Language:      {repo['language']}")
        print(f"   Visibility:    {repo['visibility']}")
        print(f"   Default branch:{repo['default_branch']}")
        print(f"   Stars:         {repo['stars']}")
        print(f"   Forks:         {repo['forks']}")
        if repo['description'] != "No description":
            print(f"   Description:   {repo['description']}")
        say(1)


#Функция поиск репозиториев
def search_repositories_by_name():
    print("\n-- Search Repositories --\n")
    query = input_string("Enter repository name or keyword: ")
    repos = search_repositories(query)
    if repos is None:
        return

    if not repos:
        print(f"\nNo repositories found for '{query}'\n")
        return

    print(f"\nFound {len(repos)} repositories matching '{query}':")
    say(1)
    for i, repo in enumerate(repos, 1):
        print(f"\n{i}. {repo['full_name']}")
        print(f"   URL:         {repo['url']}")
        print(f"   Language:    {repo['language']}")
        print(f"   Stars:       {repo['stars']}")
        print(f"   Forks:       {repo['forks']}")
        if repo['description'] != "No description":
            print(f"   Description: {repo['description']}")
        say(1)



# Главная Часть
say("s")
print("--- GitHub API Explorer ---\n")
while True:
    print("1) View user profile")
    print("2) View user repositories")
    print("3) Search repositories by name")
    print("4) Exit\n")
    select = input("> Select mode (1-4): ").strip()
    if select == "1":
        show_user_profile()
    elif select == "2":
        show_user_repositories()
    elif select == "3":
        search_repositories_by_name()
    elif select == "4":
        break
    else:
        say("er", "mode")
    say(1)  # Пустая строка для разделения
say("e")
