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

    try:
        response.raise_for_status()

    except requests.exceptions.HTTPError:
        print("Erro na comunicação com a Twitch.")
        return None

    return response.json()
