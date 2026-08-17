import requests


URL_JOGOS = "https://api.igdb.com/v4/games"


def buscar_jogos(token, client_id, nome_jogo):
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}"
    }

    body = f'''
        search "{nome_jogo}";
        fields name;
    '''

    response = requests.post(
        URL_JOGOS,
        headers=headers,
        data=body
    )
    return response


if __name__ == "__main__":
    from auth import obter_credenciais, obter_token

    client_id, client_secret = obter_credenciais()
    token = obter_token()

    resposta = buscar_jogos(token, client_id, "Minecraft")

    print(resposta.status_code)
    print(resposta.text)