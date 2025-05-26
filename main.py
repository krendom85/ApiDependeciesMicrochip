import os

from fastapi import FastAPI, Depends, HTTPException,status
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
async def Download(credentials: HTTPBasicCredentials = Depends(authenticate_user)):
    zip_file_path = os.path.join("static", "ipe.zip")

    if not os.path.exists(zip_file_path):
        return {"error": "File not found"}
    
    return FileResponse(
        path=zip_file_path,
        media_type="application/zip",
        filename="ipe.zip"
    )