from auth import obter_credenciais, obter_token

from igdb_api import (
    buscar_jogos,
    obter_detalhes_jogo,
    preparar_jogo
)

def exibir_jogo(
    nome,
    data_lancamento,
    generos,
    plataformas,
    resumo,
    rating
):
    print(f"Nome: {nome}")
    print(f"Data de lançamento: {data_lancamento}")
    print(f"Gêneros: {generos}")
    print(f"Plataformas: {plataformas}")
    print("Resumo:")
    print(resumo)
    print(f"Avaliação: {rating}")

# Obtém as credenciais da aplicação
client_id, client_secret = obter_credenciais()

# Obtém o token necessário para acessar a API
token = obter_token()

while True:
    nome_jogo = input("Digite o nome do jogo: ")

    if nome_jogo == "sair":
        break

    resultados = buscar_jogos(token, client_id, nome_jogo)

    if resultados is None:
        print("Não foi possível realizar a busca.")
        continue

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

    detalhes_jogo = obter_detalhes_jogo(
        token,
        client_id,
        jogo_id
    )

    if detalhes_jogo is None:
        print("Não foi possível obter os detalhes do jogo.")
        continue

    jogo_preparado = preparar_jogo(
        token,
        client_id,
        detalhes_jogo
    )

    if jogo_preparado is None:
        print("Não foi possível preparar os dados do jogo.")
        continue

    exibir_jogo(
        jogo_preparado["nome"],
        jogo_preparado["data_lancamento"],
        jogo_preparado["generos"],
        jogo_preparado["plataformas"],
        jogo_preparado["resumo"],
        jogo_preparado["rating"]
    )
