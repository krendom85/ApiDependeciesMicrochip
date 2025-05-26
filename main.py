import os
import zipfile
import subprocess
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


def fetch_file_from_git_lfs(file_path: str):
    try:
        subprocess.run(["git", "lfs", "pull"], check=True)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Archivo {file_path} no encontrado en Git LFS")
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error al descargar el archivo desde Git LFS: {str(e)}")

@app.get("/download-dependecies/")
async def download(credentials: HTTPBasicCredentials = Depends(authenticate_user), background_tasks: BackgroundTasks = None):

    lfs_file_path = "static/ipe.zip"
    fetch_file_from_git_lfs(lfs_file_path)
    if not os.path.exists(lfs_file_path):
        raise HTTPException(status_code=404, detail="Archivo ipe.zip no encontrado")
    
    background_tasks.add_task(delete_file, lfs_file_path)

    return FileResponse(
        path=lfs_file_path,
        media_type="application/zip",
        filename="ipe.zip"
    )