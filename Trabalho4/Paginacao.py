# Criando a classe de página
class Pagina:

    # Atributos
    id: int

    # Construtor
    def __init__(self, id: int):
        self.id = id
    
# Funções de paginação
def FIFO(execucoes: list, frames: int):

    # Variaveis usadas
    paginasFrames = [] # Lista das paginas nos frames
    contFaltas = 0 # Contador de faltas de páginas
    contRemocoes = 0 # Contador de remoção de páginas

    # Percorrendo a lista de execução de páginas
    for pagina in execucoes:
        
        # Verificando inicialmente se a pagina esta no frame
        if (pagina in paginasFrames):
            continue # A página é executada e nada acontece

        # Caso contrário, vamos adicionar a pagina aos Frames
        # Verificando se os frames estão cheios
        if (len(paginasFrames) == frames):

            # Se estiverem, vamos remover o mais velho (da posição inicial)
            paginasFrames.pop(0)
            contRemocoes += 1 # Adicionamos uma remoção à conta

        # Adicionando a pagina ao frames
        paginasFrames.append(pagina)

        # Iterando o contador de faltas de página
        contFaltas += 1

    # Retornando a quantidade de páginas trocadas e falta de páginas
    return contFaltas, contRemocoes

def LRU(execucoes: list, frames: int):

    # Variaveis usadas
    paginasFrames = [] # Lista das paginas nos frames
    contFaltas = 0 # Contador de faltas de páginas
    contRemocoes = 0 # Contador de remoção de páginas
    qtdExecucoes = len(execucoes)

    # Percorrendo as execuções
    i = 0
    while (i < qtdExecucoes):

        # Pegando a pagina
        pagina = execucoes[i]
        
        # Verificando inicialmente se a pagina esta no frame
        if (pagina in paginasFrames):
            i += 1
            continue # A página é executada e nada acontece

        # Caso contrário, vamos adicionar a pagina aos Frames
        # Verificando se os frames estão cheios
        if (len(paginasFrames) == frames):

            # Se estiverem cheios, vamos percorrer os valores anteriores atrás
            # Do menos usado recentemente
            usadosRecente = paginasFrames.copy()
            for j in range(i - 1, 0, -1):

                paginaAtual = execucoes[j]

                # Verificando se já encontramos o menos usado recentemente
                if (len(usadosRecente) == 1):
                    break

                # Removendo da lista de frames caso esteja lá
                if (paginaAtual in usadosRecente):
                    usadosRecente.remove(paginaAtual)

            paginasFrames.remove(usadosRecente[0])
            contRemocoes += 1 # Adicionamos uma remoção à conta

        # Adicionando a pagina ao frames
        paginasFrames.append(pagina)

        # Iterando o contador de faltas de página
        contFaltas += 1

        # Iterando i
        i += 1

    # Retornando a quantidade de páginas trocadas e falta de páginas
    return contFaltas, contRemocoes

def otimo(execucoes: list, frames: int):

    # Variaveis usadas
    paginasFrames = [] # Lista das paginas nos frames
    contFaltas = 0 # Contador de faltas de páginas
    contRemocoes = 0 # Contador de remoção de páginas
    qtdExecucoes = len(execucoes)

    # Percorrendo as execuções
    i = 0
    while (i < qtdExecucoes):

        # Pegando a pagina
        pagina = execucoes[i]
        
        # Verificando inicialmente se a pagina esta no frame
        if (pagina in paginasFrames):
            i += 1
            continue # A página é executada e nada acontece

        # Caso contrário, vamos adicionar a pagina aos Frames
        # Verificando se os frames estão cheios
        if (len(paginasFrames) == frames):

            # Se estiverem cheios, vamos percorrer os valores anteriores atrás
            # Do menos usado recentemente
            usadosRecente = paginasFrames.copy()
            for j in range(i + 1, qtdExecucoes - 1):

                paginaAtual = execucoes[j]

                # Verificando se já encontramos o menos usado recentemente
                if (len(usadosRecente) == 1):
                    break

                # Removendo da lista de frames caso esteja lá
                if (paginaAtual in usadosRecente):
                    usadosRecente.remove(paginaAtual)

            paginasFrames.remove(usadosRecente[0])
            contRemocoes += 1 # Adicionamos uma remoção à conta

        # Adicionando a pagina ao frames
        paginasFrames.append(pagina)

        # Iterando o contador de faltas de página
        contFaltas += 1

        # Iterando i
        i += 1

    # Retornando a quantidade de páginas trocadas e falta de páginas
    return contFaltas, contRemocoes