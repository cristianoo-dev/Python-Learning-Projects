from auth import obter_credenciais, obter_token
from twitch_api import buscar_jogos

# Obtém as credenciais da aplicação
client_id, client_secret = obter_credenciais()

# Obtém o token necessário para acessar a API
token = obter_token()

# Consulta a Twitch pelo jogo informado
resposta = buscar_jogos(token, client_id, "Minecraft")

# Verifica se houve erro na comunicação com a API
if resposta is None:
    print("Não foi possível buscar o jogo.")

else:
    # Verifica se a API encontrou algum jogo
    if resposta["data"]:
        print(resposta["data"][0]["name"])
    else:
        print("Jogo não encontrado.")
           