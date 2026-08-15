import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# URL utilizada para solicitar o token de acesso da Twitch
URL_TOKEN = "https://id.twitch.tv/oauth2/token"

def obter_credenciais():
    return client_id, client_secret

def obter_token():
    # Dados necessários para autenticação da aplicação
    dados = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    # Solicita um token de acesso à Twitch
    response = requests.post(
        URL_TOKEN,
        data=dados
    )

    try:
        response.raise_for_status()

    except requests.exceptions.HTTPError:
        print("Erro na comunicação com a Twitch.")
        return None

    resposta = response.json()

    # Retorna somente o token necessário para as requisições à API
    return resposta["access_token"]
