import os
import zipfile
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

    files = ["static/ipecmd.zip", "static/ipecmd.z01","static/ipecmd.z02","static/ipecmd.z03","static/ipecmd.z04"]
    zip_file_path = "/tmp/ipe_complete.zip"  

  
    try:
        with zipfile.ZipFile(zip_file_path, "w") as zipf:
            for file in files:
                if os.path.exists(file):
                    zipf.write(file, os.path.basename(file))
                else:
                    raise HTTPException(status_code=404, detail=f"Archivo {file} no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el archivo .zip: {str(e)}")

    background_tasks.add_task(delete_file, zip_file_path)

    return FileResponse(
        path=zip_file_path,
        media_type="application/zip",
        filename="ipe_complete.zip"
    )