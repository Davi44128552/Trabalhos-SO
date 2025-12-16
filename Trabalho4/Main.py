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

lerPaginas()
fifo1, fifo2 = Paginacao.fifo(execucoes, 3)
print(f'Faltas de páginas = {fifo1} \nTrocas = {fifo2}')

lru1, lru2 = Paginacao.lru(execucoes, 3)
print(f'\nFaltas de páginas = {lru1} \nTrocas = {lru2}')

ot1, ot2 = Paginacao.otimo(execucoes, 3)
print(f'\nFaltas de páginas = {ot1} \nTrocas = {ot2}')

x = 3
nru1, nru2, nru_resident = Paginacao.NRU(execucoes, x)
print(f'\n Algoritmo: NRU \n Frames: {x} \nFaltas de páginas = {nru1} \n Taxa de faltas: {nru1/len(execucoes):.2f} \nEvicções = {nru2} \nConjunto residente final: {nru_resident}')
