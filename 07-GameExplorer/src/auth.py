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
    if not client_id or not client_secret:
        print("As credenciais da Twitch não foram configuradas.")
        return None

    # Dados necessários para autenticação da aplicação
    dados = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    # Solicita um token de acesso à Twitch
    try:
        response = requests.post(
            URL_TOKEN,
            data=dados,
            timeout=10
        )

        response.raise_for_status()

    except requests.exceptions.Timeout:
        print("A comunicação com a Twitch excedeu o tempo limite.")
        return None

    except requests.exceptions.HTTPError:
        print(f"Erro na comunicação com a Twitch. Código: {response.status_code}")
        return None

    except requests.exceptions.RequestException:
        print("Não foi possível conectar à Twitch.")
        return None

    try:
        resposta = response.json()
    except ValueError:
        print("A resposta da Twitch não está em um formato válido.")
        return None

    token = resposta.get("access_token")

    if not token:
        print("A resposta da Twitch não contém um token de acesso válido.")
        return None

    return token