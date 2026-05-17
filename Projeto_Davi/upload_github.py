import os
import sys
import base64
import requests

TOKEN = "YOUR_GITHUB_TOKEN"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
REPO_NAME = "adocao-animais-trabalhobootcamp"

def get_username():
    res = requests.get("https://api.github.com/user", headers=HEADERS)
    if res.status_code == 200:
        return res.json().get("login")
    return None

def upload_file(username, filepath, repo_path):
    url = f"https://api.github.com/repos/{username}/{REPO_NAME}/contents/{repo_path}"
    
    # Read file content
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
    except Exception as e:
        print(f"Erro lendo {filepath}: {e}")
        return False
        
    encoded_content = base64.b64encode(content).decode('utf-8')
    data = {
        "message": f"Add {repo_path}",
        "content": encoded_content,
        "branch": "main"
    }
    
    # Check if exists to get sha
    get_res = requests.get(url, headers=HEADERS)
    if get_res.status_code == 200:
        sha = get_res.json().get("sha")
        data["sha"] = sha
        
    put_res = requests.put(url, headers=HEADERS, json=data)
    if put_res.status_code in [200, 201]:
        print(f"Sucesso: {repo_path}")
        return True
    else:
        print(f"Erro ao subir {repo_path}: {put_res.json()}")
        return False

def upload_all():
    username = get_username()
    if not username:
        print("Falha ao obter usuario")
        return
        
    print(f"Usuário: {username}")
    
    files_to_upload = [
        "src/main.py",
        "src/__init__.py",
        "tests/test_main.py",
        "tests/__init__.py",
        "requirements.txt",
        ".gitignore",
        "README.md",
        ".github/workflows/python-app.yml",
        "make_pdf.py",
        "VERSION",
        "LICENSE"
    ]
    
    for relative_path in files_to_upload:
        # relative_path is exactly the same as repo_path
        # We need to make sure the file exists locally
        if os.path.exists(relative_path):
            # Github requires forward slashes even on Windows, repo_path uses forward slashes naturally here
            upload_file(username, relative_path, relative_path)
        else:
            print(f"Arquivo não encontrado localmente: {relative_path}")

if __name__ == "__main__":
    upload_all()
