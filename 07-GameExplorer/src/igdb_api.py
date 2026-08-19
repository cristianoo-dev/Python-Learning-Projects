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
        fields name, summary, first_release_date, rating;
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
    jogo = resposta.json()[0]
    timestamp = jogo["first_release_date"]

    print(resposta.status_code)
    print(resposta.text)
    data_lancamento = formatar_data(timestamp)
    print(data_lancamento)
    