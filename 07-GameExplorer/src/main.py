from auth import obter_credenciais, obter_token
import requests

client_id, client_secret = obter_credenciais()

token = obter_token()

headers = {
    "Authorization": f"Bearer {token}",
    "Client-Id": client_id
}

URL_JOGOS = "https://api.twitch.tv/helix/games"

params = {
    "name": "Minecraft"
}

response = requests.get(
    URL_JOGOS,
    headers=headers,
    params=params
)

print(response.status_code)

resposta = response.json()
print(resposta["data"][0]["name"])
