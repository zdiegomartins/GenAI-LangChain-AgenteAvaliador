# GenAI-LangChain-AgenteAvaliador

Primeiro trabalho: a partir das avaliações obtidas da API, conforme o código do repositório, desenvolver um agente que indique se a avaliação é positiva ou negativa.

## Como funciona

A chain reúne os três componentes:

1. `ChatPromptTemplate` orienta a classificação e limita a resposta às categorias Positiva ou Negativa.
2. `ChatOllama` executa localmente o modelo `llama3.2:1b`, recomendado na aula para computadores com recursos limitados.
3. `StrOutputParser` converte a resposta do modelo em texto.

O operador `|` conecta os componentes: `chain = prompt | modelo | parser`. A função `classificar` chama `chain.invoke` com a avaliação recebida.

O programa pode buscar avaliações na API usada pelo esqueleto do projeto ou receber avaliações digitadas no terminal. A opção manual também fica disponível se a API não responder.

## Requisitos

- Python 3.10 ou superior
- Ollama instalado e em execução

No terminal, baixe o modelo local:

```bash
ollama pull llama3.2:1b
```

## Executar no Windows / VS Code

Abra um terminal na pasta do projeto e execute:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python agente_avaliacoes.py
```

Escolha `1` para buscar avaliações na API ou `2` para digitá-las. No modo manual, digite `sair` para encerrar. Se o Ollama não estiver iniciado ou o modelo ainda não tiver sido baixado, inicie o Ollama e execute `ollama pull llama3.2:1b`.