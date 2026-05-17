import requests

TOKEN = "YOUR_GITHUB_TOKEN"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
OLD_REPO = "bootcamp-adocao-animais"
NEW_REPO = "adocao-animais-trabalhobootcamp"

def rename():
    res = requests.get("https://api.github.com/user", headers=HEADERS)
    username = res.json().get("login")
    
    url = f"https://api.github.com/repos/{username}/{OLD_REPO}"
    payload = {"name": NEW_REPO}
    
    # Try to rename
    patch_res = requests.patch(url, headers=HEADERS, json=payload)
    if patch_res.status_code == 200:
        print("Renomeado com sucesso!")
    else:
        # If it doesn't exist, maybe we just create it
        if patch_res.status_code == 404:
            post_url = "https://api.github.com/user/repos"
            requests.post(post_url, headers=HEADERS, json={"name": NEW_REPO, "private": False})
            print("Criado novo repositorio")
        else:
            print("Erro ao renomear:", patch_res.json())

if __name__ == "__main__":
    rename()
