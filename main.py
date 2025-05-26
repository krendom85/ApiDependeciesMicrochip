import os
import zipfile  # Cambiado de shutil a zipfile
from fastapi import FastAPI, Depends, HTTPException, status
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

@app.get("/download-dependecies/")
async def download(credentials: HTTPBasicCredentials = Depends(authenticate_user)):
    # Archivos a incluir en el .zip
    files = ["static/ipe.zip", "static/ipe.z01"]
    zip_file_path = "static/ipe_combined.zip"

    # Crear un archivo .zip temporal
    try:
        with zipfile.ZipFile(zip_file_path, "w") as zipf:  # Cambiado a zipfile.ZipFile
            for file in files:
                if os.path.exists(file):
                    zipf.write(file, os.path.basename(file))
                else:
                    raise HTTPException(status_code=404, detail=f"Archivo {file} no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el archivo .zip: {str(e)}")

    # Enviar el archivo .zip como respuesta
    return FileResponse(
        path=zip_file_path,
        media_type="application/zip",
        filename="ipe_combined.zip"
    )