from auth import obter_credenciais, obter_token
from twitch_api import buscar_jogos

# Obtém as credenciais da aplicação
client_id, client_secret = obter_credenciais()

# Obtém o token necessário para acessar a API
token = obter_token()

while True:
    nome_jogo = input("Digite o nome do jogo: ")

    if nome_jogo == "sair":
        break

    resposta = buscar_jogos(token, client_id, nome_jogo)

    if resposta is None:
        print("Não foi possível buscar o jogo.")

    else:
        if resposta["data"]:
            print(resposta["data"][0]["name"])
        else:
            print("Jogo não encontrado.")
 