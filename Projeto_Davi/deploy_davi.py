import os
import requests
import subprocess
import time

TOKEN = "YOUR_GITHUB_TOKEN"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def create_github_repo(repo_name):
    # Try to see if it already exists
    response = requests.get("https://api.github.com/user", headers=HEADERS)
    if response.status_code != 200:
        print("Erro ao acessar Github:", response.json())
        return None
    username = response.json().get("login")
    print(f"Logado como: {username}")
    
    repo_url = f"https://api.github.com/user/repos"
    payload = {"name": repo_name, "private": False}
    
    res = requests.post(repo_url, headers=HEADERS, json=payload)
    if res.status_code == 201:
        print(f"Repositório criado com sucesso!")
        return f"https://github.com/{username}/{repo_name}"
    elif res.status_code == 422: # Already exists
        print(f"Repositório provavlemente já existe. Tentando continuar.")
        return f"https://github.com/{username}/{repo_name}"
    else:
        print("Falha ao criar repositorio:", res.json())
        return None

def main():
    repo_name = "bootcamp-adocao-animais"
    repo_url = create_github_repo(repo_name)
    
    if not repo_url:
        print("Parando...")
        return
        
    print(f"URL do repo: {repo_url}")
    
    # Save repo url to text
    with open("repo_url.txt", "w") as f:
        f.write(repo_url)
    
    # Git init and push
    os.system("git init")
    os.system("git add .")
    os.system('git commit -m "Initial commit"')
    os.system("git branch -M main")
    os.system(f"git remote add origin https://{TOKEN}@github.com/{repo_url.split('github.com/')[1]}.git")
    os.system("git push -u origin main -f")
    print("Código enviado ao github com sucesso!")

if __name__ == "__main__":
    main()
