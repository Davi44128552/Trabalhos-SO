# Criando a classe de página
class Pagina:
    # Atributos
    id: int
    bit_referencia: int 
    bit_modificado: int #pertencente ao algoritmo NRU

    # Construtor
    def __init__(self, id: int):
        self.id = id
        self.bit_referencia = 1 # Ao ser carregada, ganha "uma chance" (bit = 1)
        self.bit_modificado = 0 # pertencente ao algoritmo NRU

    # Método para verificar igualdade
    def __eq__(self, other):
        if isinstance(other, Pagina):
            return self.id == other.id
        return self.id == other
    
    # Representação em string
    def __repr__(self):
        return str(self.id)

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

nru_paginas = {}   # id -> Pagina
nru_acessos = 0
def NRU(paginasFrames, execucoes, indice_atual):
    # Estratégia NRU compatível com paginacao()
    # paginasFrames: lista de INT (ids)

    import random
    global nru_paginas, nru_acessos
    nru_acessos += 1

    # Garante que todas as páginas do frame existam como objeto
    for pid in paginasFrames:
        if pid not in nru_paginas:
            nru_paginas[pid] = Pagina(pid)

    # Página atual
    pid_atual = execucoes[indice_atual]

    # Se página já existe, marca referência
    if pid_atual in nru_paginas:
        nru_paginas[pid_atual].bit_referencia = 1

    # Classificação NRU
    classes = {0: [], 1: [], 2: [], 3: []}

    for pid in paginasFrames:
        p = nru_paginas[pid]

        if p.bit_referencia == 0 and p.bit_modificado == 0:
            classes[0].append(pid)
        elif p.bit_referencia == 0 and p.bit_modificado == 1:
            classes[1].append(pid)
        elif p.bit_referencia == 1 and p.bit_modificado == 0:
            classes[2].append(pid)
        else:
            classes[3].append(pid)

    # Escolhe vítima da menor classe não vazia
    for c in range(4):
        if classes[c]:
            vitima = random.choice(classes[c])
            break

    # Reset periódico do bit R (simula clock)
    if nru_acessos % max(1, len(paginasFrames)) == 0:
        for pid in paginasFrames:
            nru_paginas[pid].bit_referencia = 0

    return vitima

def lfu(paginasFrames, execucoes, indice_atual):
    # LFU (Least Frequently Used): remove a página com menor frequência de uso
    # A contagem é feita baseada no histórico de execuções até o momento atual

    # Inicialização do contador 
    frequencias = {id_pag: 0 for id_pag in paginasFrames}
    
    # Percorre o histórico de execuções
    # Depois conta quantas vezes cada página foi acessada
    for i in range(indice_atual):
        pag = execucoes[i]
        if pag in frequencias:
            frequencias[pag] += 1
            
    # Vai encontrar a página com a menor frequência
    pagina_vitima = min(frequencias, key=frequencias.get)
    
    return pagina_vitima

def mfu(paginasFrames, execucoes, indice_atual):

    # MFU (Most Frequently Used): remove a página com maior frequência de uso
    # Lógica inversa ao LFU

    # Igual no lfu, inicialização do contador
    frequencias = {id_pag: 0 for id_pag in paginasFrames}
    
    # Conta as frequências no histórico
    for i in range(indice_atual):
        pag = execucoes[i]
        if pag in frequencias:
            frequencias[pag] += 1
            
    # Aqui encontra a página com a maior frequência
    pagina_vitima = max(frequencias, key=frequencias.get)
    
    return pagina_vitima

def relogio(execucoes: list, frames: int):
    
    # Variaveis usadas
    memoria = [] # Lista de objetos Pagina, memória circular
    ponteiro = 0 
    referencias = 0
    contFaltas = 0 # Contador de faltas de páginas
    contRemocoes = 0 # Contador de remoção de páginas
    qtdExecucoes = len(execucoes)

    # Percorrendo as execuções
    for i in range(qtdExecucoes):
        id_pagina = execucoes[i] # Pegando a pagina
        pagina_nova = Pagina(id_pagina) # Cria objeto com bit=1

        # Verificando inicialmente se a pagina esta na memoria
        encontrou = False
        for p in memoria:
            if p == id_pagina:
                p.bit_referencia = 1 # Se sim, dá a segunda chance
                encontrou = True
                break

        if encontrou:
            continue # A página é executada e nada acontece

        # Caso a página nova não esteja na memoria
        contFaltas += 1

        # Se a memória não estiver cheia, apenas adiciona
        if len(memoria) < frames:
            memoria.append(pagina_nova)
        
        # Se estiver cheia, executa o algoritmo do Relógio
        else:
            contRemocoes += 1
            while True:
                # Olha para a página apontada pelo ponteiro
                candidata = memoria[ponteiro]

                # Se bit for 1, dá segunda chance e zera o bit
                if candidata.bit_referencia == 1:
                    candidata.bit_referencia = 0
                referencias += 1
                if referencias % max(1, frames) == 0:
                    for p in memoria:
                        p.bit_referencia = 0
                    # Avança ponteiro circularmente
                    ponteiro = (ponteiro + 1) % frames 
                
                # Se bit for 0, é a nossa escolha
                else:
                    # Substitui a página no local do ponteiro
                    memoria[ponteiro] = pagina_nova 
                    # Avança o ponteiro para a próxima posição após a inserção
                    ponteiro = (ponteiro + 1) % frames
                    break

    # Convertendo a lista de Objetos Pagina de volta para inteiros
    lista_final_ids = [p.id for p in memoria]
    
    return contFaltas, contRemocoes, lista_final_ids

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