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
    response = requests.post(URL_TOKEN)
    print(response.status_code)
