import requests
from datetime import datetime

URL_JOGOS = "https://api.igdb.com/v4/games"
URL_GENEROS = "https://api.igdb.com/v4/genres"
URL_PLATAFORMAS = "https://api.igdb.com/v4/platforms"

def criar_headers(token, client_id):

    return {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}"
    }

def buscar_jogos(token, client_id, nome_jogo):

    headers = criar_headers(token, client_id)

    body = f'''
        search "{nome_jogo}";
        fields id, name;
    '''

    response = requests.post(
        URL_JOGOS,
        headers=headers,
        data=body
    )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Erro na comunicação com a IGDB.")
        return None

    return response.json()

def buscar_detalhes_jogo(token, client_id, jogo_id):

    headers = criar_headers(token, client_id)

    body = f'''
        where id = {jogo_id};
        fields name, summary, first_release_date, rating, genres, platforms;
    '''

    response = requests.post(
        URL_JOGOS,
        headers=headers,
        data=body
    )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Erro na comunicação com a IGDB.")
        return None

    return response

def buscar_nomes(token, client_id, url, ids):

    headers = criar_headers(token, client_id)

    ids_formatados = ",".join(map(str, ids))

    body = f'''
        where id = ({ids_formatados});
        fields name;
    '''

    response = requests.post(
        url,
        headers=headers,
        data=body
    )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Erro na comunicação com a IGDB.")
        return None

    dados = response.json()

    nomes = []

    for item in dados:
        nomes.append(item["name"])

    return nomes

def buscar_generos(token, client_id, ids_generos):

    return buscar_nomes(
        token,
        client_id,
        URL_GENEROS,
        ids_generos
    )
def buscar_plataformas(token, client_id, ids_plataformas):

    return buscar_nomes(
        token,
        client_id,
        URL_PLATAFORMAS,
        ids_plataformas
    )

def formatar_data(timestamp):

    data = datetime.fromtimestamp(timestamp)

    return data.strftime("%d/%m/%Y")

def preparar_jogo(token, client_id, jogo):

    nome = jogo["name"]

    resumo = jogo.get("summary", "Não disponível.")

    timestamp = jogo.get("first_release_date")

    if timestamp is not None:
        data_lancamento = formatar_data(timestamp)
    else:
        data_lancamento = "Não disponível."

    ids_generos = jogo.get("genres", [])

    if ids_generos:
        nomes_generos = buscar_generos(
            token,
            client_id,
            ids_generos
        )

        if nomes_generos is None:
            return None

        generos = ", ".join(nomes_generos)
    else:
        generos = "Não disponível."

    ids_plataformas = jogo.get("platforms", [])

    if ids_plataformas:
        nomes_plataformas = buscar_plataformas(
            token,
            client_id,
            ids_plataformas
        )

        if nomes_plataformas is None:
            return None

        plataformas = ", ".join(nomes_plataformas)
    else:
        plataformas = "Não disponível."

    rating = jogo.get("rating")

    if rating is not None:
        rating = round(rating, 2)
    else:
        rating = "Não disponível."

    return {
        "nome": nome,
        "data_lancamento": data_lancamento,
        "generos": generos,
        "plataformas": plataformas,
        "resumo": resumo,
        "rating": rating
    }

def obter_detalhes_jogo(token, client_id, jogo_id):

    resposta = buscar_detalhes_jogo(
        token,
        client_id,
        jogo_id
    )

    if resposta is None:
        return None

    dados = resposta.json()

    if not dados:
        return None

    return dados[0]
