import requests

# Endpoint utilizado para consultar os jogos na Twitch
URL_JOGOS = "https://api.twitch.tv/helix/games"

def buscar_jogos(token, client_id, nome_jogo):
    # Informações necessárias para autenticar a requisição
    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Id": client_id
    }

    # Nome do jogo que será pesquisado
    params = {
        "name": nome_jogo
    }

    response = requests.get(
        URL_JOGOS,
        headers=headers,
        params=params
    )

    try:
        response.raise_for_status()

    except requests.exceptions.HTTPError:
        print("Erro na comunicação com a Twitch.")
        return None

    # Retorna os dados recebidos da API em formato Python
    return response.json()
