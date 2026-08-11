from auth import obter_credenciais, obter_token
from twitch_api import buscar_jogos


client_id, client_secret = obter_credenciais()

token = obter_token()

resposta = buscar_jogos(token, client_id, "Minecraft")

print(resposta["data"][0]["name"])
