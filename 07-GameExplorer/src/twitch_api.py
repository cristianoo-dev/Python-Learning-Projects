URL_JOGOS = "https://api.twitch.tv/helix/games"
import requests

def buscar_jogos(token, client_id, nome_jogo):
    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Id": client_id
    }

    params = {
        "name": nome_jogo
    }

    response = requests.get(
        URL_JOGOS,
        headers=headers,
        params=params
    )

    return response.json()
