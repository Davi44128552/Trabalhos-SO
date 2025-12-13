# Criando a classe de página
class Pagina:
    # Atributos
    id: int
    # Construtor
    def __init__(self, id: int):
        self.id = id

def fifo(paginasFrames, execucoes, indice_atual):
    # No FIFO, se estiverem cheios, vamos remover o mais velho (da posição inicial)
    return paginasFrames[0]

def lru(paginasFrames, execucoes, indice_atual):
    # Se estiverem cheios, vamos percorrer os valores anteriores atrás
    # Do menos usado recentemente
    usadosRecente = paginasFrames.copy()
    
    # Range para ir do índice atual para trás até o começo
    for j in range(indice_atual - 1, -1, -1): 
        paginaAtual = execucoes[j]

        # Verificando se já encontramos o menos usado recentemente
        if (len(usadosRecente) == 1):
            break

        # Removendo da lista de frames caso esteja lá
        if (paginaAtual in usadosRecente):
            usadosRecente.remove(paginaAtual)
            
    return usadosRecente[0]

def otimo(paginasFrames, execucoes, indice_atual):
    qtdExecucoes = len(execucoes)
    # Se estiverem cheios, vamos percorrer os valores futuros
    # Do que vai demorar mais para ser usado
    usadosRecente = paginasFrames.copy()
    
    # Range para ir do índice atual para frente até o fim
    for j in range(indice_atual + 1, qtdExecucoes): 
        paginaAtual = execucoes[j]

        # Verificando se já encontramos o menos usado recentemente
        if (len(usadosRecente) == 1):
            break

        # Removendo da lista de frames caso esteja lá
        if (paginaAtual in usadosRecente):
            usadosRecente.remove(paginaAtual)
            
    return usadosRecente[0]

def paginacao(execucoes: list, frames: int, estrategia_escolha):
        
    # Variaveis usadas
    paginasFrames = [] # Lista das paginas nos frames
    contFaltas = 0 # Contador de faltas de páginas
    contRemocoes = 0 # Contador de remoção de páginas
    qtdExecucoes = len(execucoes)

    # Percorrendo as execuções
    for i in range(qtdExecucoes):
        
        # Pegando a pagina
        pagina = execucoes[i]

        # Verificando inicialmente se a pagina esta no frame
        if (pagina in paginasFrames):
            continue # A página é executada e nada acontece

        # Caso contrário, vamos adicionar a pagina aos Frames
        # Verificando se os frames estão cheios
        if (len(paginasFrames) == frames):

            # Aqui definimos a ESCOLHA de quem vai sair baseada na estratégia passada
            escolha = estrategia_escolha(paginasFrames, execucoes, i)
            
            # Removendo a escolha feita
            paginasFrames.remove(escolha)
            contRemocoes += 1 # Adicionamos uma remoção à conta

        # Adicionando a pagina ao frames
        paginasFrames.append(pagina)

        # Iterando o contador de faltas de página
        contFaltas += 1

    # Retornando a quantidade de páginas trocadas e falta de páginas
    return contFaltas, contRemocoes, paginasFrames
