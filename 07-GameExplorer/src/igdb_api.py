import requests
from datetime import datetime

URL_JOGOS = "https://api.igdb.com/v4/games"

def buscar_jogos(token, client_id, nome_jogo):
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}"
    }

    body = f'''
        search "{nome_jogo}";
        fields id, name;
    '''

    response = requests.post(
        URL_JOGOS,
        headers=headers,
        data=body
    )
    return response

def buscar_detalhes_jogo(token, client_id, jogo_id):
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}"
    }

    body = f'''
        where id = {jogo_id};
        fields name, summary, first_release_date;
    '''

    response = requests.post(
        URL_JOGOS,
        headers=headers,
        data=body
    )
    return response

def formatar_data(timestamp):
    data = datetime.fromtimestamp(timestamp)
    return data.strftime("%d/%m/%Y")


if __name__ == "__main__":
    from auth import obter_credenciais, obter_token

    client_id, client_secret = obter_credenciais()
    token = obter_token()

    resposta = buscar_detalhes_jogo(token, client_id, 135400)

    print(resposta.status_code)
    print(resposta.text)
    print(formatar_data(1482105600))