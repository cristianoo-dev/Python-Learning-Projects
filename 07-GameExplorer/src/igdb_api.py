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

def fazer_requisicao(url, headers, body):

    try: 
        response = requests.post(
            url,
            headers=headers,
            data=body,
            timeout=10
        )

        response.raise_for_status()

    except requests.exceptions.Timeout:
        print("A comunicação com a IGDB excedeu o tempo limite.")
        return None

    except requests.exceptions.HTTPError:
        print(f"Erro na comunicação com a IGDB. Código: {response.status_code}")
        return None

    except requests.exceptions.ConnectionError:
        print("Não foi possível estabelecer conexão com a IGDB.")
        return None

    except requests.exceptions.RequestException:
        print("Ocorreu um erro durante a requisição à IGDB.")
        return None

    return response

def obter_json(response):

    try:
        return response.json()

    except ValueError:
        print("A resposta da IGDB não está em um formato válido.")
        return None

def buscar_jogos(token, client_id, nome_jogo):

    headers = criar_headers(token, client_id)

    body = f'''
        search "{nome_jogo}";
        fields id, name;
    '''

    response = fazer_requisicao(
        URL_JOGOS,
        headers,
        body
    )

    if response is None:
        return None

    dados = obter_json(response)

    if dados is None:
        return None

    if not isinstance(dados, list):
        print("A resposta da IGDB não está no formato esperado.")
        return None

    for jogo in dados:
        if not isinstance(jogo, dict) or not isinstance(jogo.get("name"), str):
            print("Os resultados da busca não estão no formato esperado.")
            return None

    return dados

def buscar_detalhes_jogo(token, client_id, jogo_id):

    if (
        isinstance(jogo_id, bool)
        or not isinstance(jogo_id, int)
        or jogo_id <= 0
    ):
        print("O ID do jogo está em um formato inválido.")
        return None

    headers = criar_headers(token, client_id)

    body = f'''
        where id = {jogo_id};
        fields name, summary, first_release_date, rating, genres, platforms;
    '''

    response = fazer_requisicao(
        URL_JOGOS,
        headers,
        body
    )

    if response is None:
        return None

    return response

def buscar_nomes(token, client_id, url, ids):

    if not isinstance(ids, list) or any(
        isinstance(id_jogo, bool)
        or not isinstance(id_jogo, int)
        or id_jogo <= 0
        for id_jogo in ids
    ):
        print("Os IDs recebidos estão em um formato inválido.")
        return None

    headers = criar_headers(token, client_id)

    ids_formatados = ",".join(map(str, ids))

    body = f'''
        where id = ({ids_formatados});
        fields name;
    '''

    response = fazer_requisicao(
        url,
        headers,
        body
    )

    if response is None:
        return None

    dados = obter_json(response)

    if dados is None:
        return None

    if not isinstance(dados, list):
        print("A resposta da IGDB não está no formato esperado.")
        return None

    nomes = []

    for item in dados:
        if (
            not isinstance(item, dict)
            or not isinstance(item.get("name"), str)
            or not item["name"]
        ):
            print("A resposta da IGDB não está no formato esperado.")
            return None

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

    nome = jogo.get("name")

    if not isinstance(nome, str) or not nome:
        print("Os dados do jogo não contêm um nome válido.")
        return None

    resumo = jogo.get("summary")

    if resumo is None:
        resumo = "Não disponível."
    elif not isinstance(resumo, str) or not resumo.strip():
        print("O resumo do jogo está em um formato inválido.")
        return None

    timestamp = jogo.get("first_release_date")

    if timestamp is None:
        data_lancamento = "Não disponível."
    elif not isinstance(timestamp, (int, float)):
        print("A data de lançamento está em um formato inválido.")
        return None
    else:
        data_lancamento = formatar_data(timestamp)

    ids_generos = jogo.get("genres", [])

    if not isinstance(ids_generos, list):
        print("Os gêneros do jogo estão em um formato inválido.")
        return None

    if ids_generos:
        nomes_generos = buscar_generos(
            token,
            client_id,
            ids_generos
        )

        if nomes_generos is None:
            return None

        if nomes_generos:
            generos = ", ".join(nomes_generos)
        else:
            generos = "Não disponível."
    else:
        generos = "Não disponível."

    ids_plataformas = jogo.get("platforms", [])

    if not isinstance(ids_plataformas, list):
        print("As plataformas do jogo estão em um formato inválido.")
        return None

    if ids_plataformas:
        nomes_plataformas = buscar_plataformas(
            token,
            client_id,
            ids_plataformas
        )

        if nomes_plataformas is None:
            return None

        if nomes_plataformas:
            plataformas = ", ".join(nomes_plataformas)
        else:
            plataformas = "Não disponível."
    else:
        plataformas = "Não disponível."

    rating = jogo.get("rating")

    if rating is None:
        rating = "Não disponível."
    elif isinstance(rating, bool) or not isinstance(rating, (int, float)):
        print("A avaliação do jogo está em um formato inválido.")
        return None
    else:
        rating = round(rating, 2)

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

    dados = obter_json(resposta)

    if dados is None:
        return None

    if not isinstance(dados, list):
        print("A resposta da IGDB não está no formato esperado.")
        return None

    if not dados:
        return None

    if not isinstance(dados[0], dict):
        print("Os detalhes do jogo não estão no formato esperado.")
        return None

    nome = dados[0].get("name")

    if not isinstance(nome, str) or not nome.strip():
        print("Os detalhes do jogo não contêm um nome válido.")
        return None

    return dados[0]
