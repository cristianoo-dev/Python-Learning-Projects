import os
import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

URL_TOKEN = "https://id.twitch.tv/oauth2/token"

def obter_credenciais():
    return client_id, client_secret

def obter_token():
    dados = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    response = requests.post(
        URL_TOKEN,
        data=dados
    )

    print(response.status_code)

    resposta = response.json()
    print(resposta)