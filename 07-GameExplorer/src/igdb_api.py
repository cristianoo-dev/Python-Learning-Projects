import requests
from datetime import datetime

URL_JOGOS = "https://api.igdb.com/v4/games"
URL_GENEROS = "https://api.igdb.com/v4/genres"
URL_PLATAFORMAS = "https://api.igdb.com/v4/platforms"

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
        fields name, summary, first_release_date, rating, genres, platforms;
    '''

    response = requests.post(
        URL_JOGOS,
        headers=headers,
        data=body
    )
    return response

def buscar_generos(token, client_id, ids_generos):
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}"
    }

    ids = ",".join(map(str, ids_generos))

    body = f'''
        where id = ({ids});
        fields name;
    '''

    response = requests.post(
        URL_GENEROS,
        headers=headers,
        data=body
    )
    generos = response.json()
    nomes_generos = []

    for genero in generos:
        nomes_generos.append(genero["name"])
    return nomes_generos

def buscar_plataformas(token, client_id, ids_plataformas):
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}"
    }

    ids = ",".join(map(str, ids_plataformas))

    body = f'''
        where id = ({ids});
        fields name;
    '''

    response = requests.post(
        URL_PLATAFORMAS,
        headers=headers,
        data=body
    )

    plataformas = response.json()

    nomes_plataformas = []

    for plataforma in plataformas:
        nomes_plataformas.append(plataforma["name"])

    return nomes_plataformas

def formatar_data(timestamp):
    data = datetime.fromtimestamp(timestamp)
    return data.strftime("%d/%m/%Y")

def exibir_jogo(nome, data_lancamento, generos, plataformas, resumo, rating):
    print(f"Nome: {nome}")
    print(f"Data de lançamento: {data_lancamento}")
    print(f"Gêneros: {generos}")
    print(f"Plataformas: {plataformas}")
    print("Resumo:")
    print(resumo)
    print(f"Avaliação: {rating:.2f}")
