import os

import uvicorn
import tempfile
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.user_api import router as user_router
from api.sport_api import router as sport_router
from api.event_api import router as event_router
from api.match_api import router as match_router
from api.squad_api import router as squad_router
from api.country_api import router as country_router
from api.athlete_api import router as athlete_router
from api.schedule_api import router as schedule_router


app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")
app.include_router(sport_router, prefix="/sport")
app.include_router(match_router, prefix="/match")
app.include_router(squad_router, prefix="/squad")
app.include_router(country_router, prefix="/country")
app.include_router(athlete_router, prefix="/athlete")
app.include_router(schedule_router, prefix="/schedule")

allowed_origins = ["http://localhost:3000",
                   "http://www.kheldekho.in",
                   "http://www.kheldekho.in:3000",
                   "http://www.kheldekho.in:3000/",
                   "http://kheldekho.in:3000/",
                   "http://kheldekho.in:3000"
                   "http://20.197.9.130"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ssl_certfile = r"cert\ssl_cert.crt"
# ssl_keyfile =  r"cert\ssl_key.key"

os.environ['AZURE_CLIENT_ID'] = '<your-client-id>'
os.environ['AZURE_TENANT_ID'] = '<your-tenant-id>'
os.environ['AZURE_CLIENT_SECRET'] = '<your-client-secret>'

PEM_FILE_SECRET_NAME = "kheldekho-cert-file"
# Replace with your Azure Key Vault URL
KEY_VAULT_URL = "https://kheldekho-vault.vault.azure.net/"


# Authenticate to Azure Key Vault
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

# Retrieve the SSL key and certificate from Key Vault
pem_file_content = client.get_secret(PEM_FILE_SECRET_NAME).value

# Create temporary files in memory to hold the SSL key and certificate
with tempfile.NamedTemporaryFile(delete=False) as pem_file:
    pem_file_name = pem_file.name
    pem_file.write(pem_file_content.encode())


if __name__ == "__main__":
    uvicorn.run(app,
                host="0.0.0.0",
                port=8000,
                ssl_keyfile=pem_file_name,
                ssl_certfile=pem_file_name,
                )
