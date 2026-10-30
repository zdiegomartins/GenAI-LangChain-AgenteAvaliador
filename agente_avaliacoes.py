"""Classifica avaliações como Positiva ou Negativa usando Ollama e LangChain."""

import requests
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


URL_AVALIACOES = "https://apis.codante.io/api/reviews-api/reviews"
MODELO_LOCAL = "llama3.2:1b"

# A chain segue o padrão dos exemplos: prompt | modelo | parser.
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Classifique o sentimento predominante de uma avaliação de produto. "
            "Responda somente com uma destas palavras: Positiva ou Negativa. "
            "Elogios indicam Positiva; reclamações indicam Negativa. "
            "Se houver sentimentos mistos, escolha o predominante.",
        ),
        ("human", "Avaliação: {avaliacao}"),
    ]
)

modelo = ChatOllama(model=MODELO_LOCAL, temperature=0)
parser = StrOutputParser()
chain = prompt | modelo | parser


def classificar(avaliacao):
    """Envia uma avaliação à chain e retorna a classificação em texto."""
    return chain.invoke({"avaliacao": avaliacao}).strip()


def buscar_avaliacoes():
    """Busca avaliações de exemplo na API indicada no projeto."""
    resposta = requests.get(URL_AVALIACOES, timeout=30)
    resposta.raise_for_status()
    dados = resposta.json()
    return [item["description"] for item in dados.get("data", []) if item.get("description")]


def classificar_avaliacoes(avaliacoes):
    for numero, avaliacao in enumerate(avaliacoes, start=1):
        try:
            print(f"Avaliação {numero}: {avaliacao}")
            print(f"Classificação: {classificar(avaliacao)}\n")
        except Exception as erro:
            print(f"Não foi possível classificar a avaliação {numero}: {erro}\n")


def modo_manual():
    print("Digite uma avaliação por vez. Digite 'sair' para encerrar.\n")
    while True:
        avaliacao = input("Avaliação: ").strip()
        if avaliacao.lower() in {"sair", "exit"}:
            break
        if not avaliacao:
            continue
        try:
            print(f"Classificação: {classificar(avaliacao)}\n")
        except Exception as erro:
            print(f"Não foi possível classificar: {erro}\n")


def main():
    print("Agente classificador de avaliações (LLM local: Ollama / llama3.2)")
    print("1 - Classificar avaliações obtidas da API")
    print("2 - Digitar avaliações manualmente")
    opcao = input("Escolha uma opção [1/2]: ").strip()

    if opcao == "2":
        modo_manual()
        return

    try:
        avaliacoes = buscar_avaliacoes()
    except requests.RequestException as erro:
        print(f"Não foi possível acessar a API: {erro}")
        print("Você pode continuar digitando avaliações manualmente.")
        modo_manual()
        return

    if not avaliacoes:
        print("A API não retornou avaliações.")
        return
    classificar_avaliacoes(avaliacoes)


if __name__ == "__main__":
    main()
