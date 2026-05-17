import os
import requests
import base64

TOKEN = "YOUR_GITHUB_TOKEN"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
REPO_NAME = "adocao-animais-trabalhobootcamp"

def get_username():
    res = requests.get("https://api.github.com/user", headers=HEADERS)
    return res.json().get("login")

def reset_and_upload():
    username = get_username()
    # 1. Delete repo
    print("Deletando repositorio antigo...")
    requests.delete(f"https://api.github.com/repos/{username}/{REPO_NAME}", headers=HEADERS)
    
    # 2. Re-create repo
    print("Recriando repositorio...")
    res = requests.post("https://api.github.com/user/repos", headers=HEADERS, json={
        "name": REPO_NAME,
        "private": False,
        "auto_init": True # to create main branch
    })
    
    # wait a moment
    import time
    time.sleep(3)
    
    # 3. Create tree with all files
    files_to_upload = [
        "src/main.py",
        "src/__init__.py",
        "tests/test_main.py",
        "tests/__init__.py",
        "requirements.txt",
        ".gitignore",
        "README.md",
        ".github/workflows/python-app.yml",
        "VERSION",
        "LICENSE"
    ]
    
    tree_nodes = []
    print("Preparando arquivos para commit unico...")
    for file_path in files_to_upload:
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                content = f.read()
            
            # create blob
            blob_res = requests.post(
                f"https://api.github.com/repos/{username}/{REPO_NAME}/git/blobs",
                headers=HEADERS,
                json={
                    "content": base64.b64encode(content).decode('utf-8'),
                    "encoding": "base64"
                }
            )
            blob_sha = blob_res.json()["sha"]
            
            tree_nodes.append({
                "path": file_path,
                "mode": "100644",
                "type": "blob",
                "sha": blob_sha
            })
            print(f"Preparado {file_path}")
            
    # get base tree (from auto_init commit)
    ref_res = requests.get(f"https://api.github.com/repos/{username}/{REPO_NAME}/git/refs/heads/main", headers=HEADERS)
    base_commit_sha = ref_res.json()["object"]["sha"]
    
    commit_res = requests.get(f"https://api.github.com/repos/{username}/{REPO_NAME}/git/commits/{base_commit_sha}", headers=HEADERS)
    base_tree_sha = commit_res.json()["tree"]["sha"]
    
    # create new tree
    tree_res = requests.post(
        f"https://api.github.com/repos/{username}/{REPO_NAME}/git/trees",
        headers=HEADERS,
        json={
            "base_tree": base_tree_sha,
            "tree": tree_nodes
        }
    )
    new_tree_sha = tree_res.json()["sha"]
    
    # create new commit
    new_commit_res = requests.post(
        f"https://api.github.com/repos/{username}/{REPO_NAME}/git/commits",
        headers=HEADERS,
        json={
            "message": "First Release - Davi Augusto",
            "tree": new_tree_sha,
            "parents": [base_commit_sha]
        }
    )
    new_commit_sha = new_commit_res.json()["sha"]
    
    # update reference
    requests.patch(
        f"https://api.github.com/repos/{username}/{REPO_NAME}/git/refs/heads/main",
        headers=HEADERS,
        json={"sha": new_commit_sha}
    )
    
    print("Todos os commits unificados e repositorio limpado!")

if __name__ == "__main__":
    reset_and_upload()
