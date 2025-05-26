import os
import requests
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()

USERNAME = "cmoreno"
PASSWORD = "S@lintece2025"

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

def delete_file(file_path: str):
    """Elimina el archivo especificado."""
    if os.path.exists(file_path):
        os.remove(file_path)



@app.get("/download-dependecies/")
async def download(credentials: HTTPBasicCredentials = Depends(authenticate_user), background_tasks: BackgroundTasks = None):

    github_file_url = "https://media.githubusercontent.com/media/krendom85/ApiDependeciesMicrochip/main/static/ipe.zip"

    response = requests.get(github_file_url, stream=True)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Archivo ipe.zip no encontrado en GitHub")

    temp_file_path = "ipe.zip"
    with open(temp_file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return FileResponse(
        path=temp_file_path,
        media_type="application/zip",
        filename="ipe.zip"
    )