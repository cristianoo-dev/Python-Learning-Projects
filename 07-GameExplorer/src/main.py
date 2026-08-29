from auth import obter_credenciais, obter_token
from igdb_api import (
    buscar_jogos,
    buscar_detalhes_jogo,
    buscar_generos,
    buscar_plataformas,
    formatar_data,
    exibir_jogo
)

# Obtém as credenciais da aplicação
client_id, client_secret = obter_credenciais()

# Obtém o token necessário para acessar a API
token = obter_token()

while True:
    nome_jogo = input("Digite o nome do jogo: ")

    if nome_jogo == "sair":
        break

    resposta = buscar_jogos(token, client_id, nome_jogo)

    resultados = resposta.json()

    if not resultados:
        print("Jogo não encontrado.")
        continue

    for indice, jogo in enumerate(resultados, start=1):
        print(indice, "-", jogo["name"])

    try:
        escolha = int(input("Escolha um jogo: "))
    except ValueError:
        print("Escolha inválida.")
        continue

    if escolha < 1 or escolha > len(resultados):
        print("Escolha inválida.")
        continue

    jogo_escolhido = resultados[escolha - 1]

    jogo_id = jogo_escolhido["id"]

    resposta = buscar_detalhes_jogo(token, client_id, jogo_id)

    jogo = resposta.json()[0]

    nome = jogo["name"]
    resumo = jogo["summary"]

    timestamp = jogo["first_release_date"]
    data_lancamento = formatar_data(timestamp)

    ids_generos = jogo["genres"]

    nomes_generos = buscar_generos(
        token,
        client_id,
        ids_generos
    )

    generos = ", ".join(nomes_generos)

    ids_plataformas = jogo["platforms"]

    nomes_plataformas = buscar_plataformas(
        token,
        client_id,
        ids_plataformas
    )

    plataformas = ", ".join(nomes_plataformas)

    rating = round(jogo["rating"], 2)

    exibir_jogo(
        nome,
        data_lancamento,
        generos,
        plataformas,
        resumo,
        rating
    )
