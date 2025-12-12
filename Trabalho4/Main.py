# Importando as bibliotecas necessárias
import sys
import Paginacao

# Variáveis globais
paginas: list = []
execucoes: list = []

# Função para ler o trace
def lerPaginas(arquivo: str = "silberschatz2001.trace"):

    # Variaveis
    global paginas

    try:
        # Abrindo o arquivo
        with open(arquivo) as trace:

            # Percorrendo as linhas do arquivo
            for linha in trace:
                execucoes.append(int(linha.strip()))
                paginas.append(Paginacao.Pagina(int(linha.strip()))) # Criando objeto página

    except FileNotFoundError:
        print("Arquivo não encontrado!")
