# Importando bibliotecas necessárias
import json
import copy

# Criando as variáveis globais que serão usadas 
quantum: int = 0
aging: int = 0
pid_pc: int = 1
timer: int = 0

# Lista para armazenar os processos
processos = []

# Criando uma classe para o processo
class Processo:
    pid: int # CPF do processo

    # Prioridades
    prioridadeEst: int # Estática
    prioridadeDin: int # Dinâmica

    # Tempo de execução
    tempoTotalExec: int # Total
    tempoRestanteExec: int # Restante
    tempoInicializar: int # Momento que o processo se inicia

    # Funções do processo
    # Construtor
    def __init__(self, pid: int, prioridade: int, tempoTotal: int, tInicializar: int):

            # Definindo o PID do processo
            self.pid = pid 
            
            # Definindo as prioridades
            self.prioridadeEst = prioridade
            self.prioridadeDin = self.prioridadeEst # Como o processo foi criado agora, din = est

            # Definindo o tempo
            self.tempoTotalExec = tempoTotal
            self.tempoRestanteExec = self.tempoTotalExec # Mesma lógica (no início, restante = total)

            # Tempo de inicialização
            self.tempoInicializar = tInicializar

# Criando uma função para leitura de arquivo
def definirPropriedades(arquivo_config: str = "config.json"):
    # Chamando as variáveis globais
    global quantum
    global aging

    try:
        with open(arquivo_config, "r") as config:
            
            # Lendo o arquivo json para definir as propriedades para o escalonador
            dados = json.load(config)
            quantum = int(dados.get("quantum", quantum))
            aging = int(dados.get("aging", aging))

    except Exception as e:
         print("Erro na configuração dos arquivos!")

# Função para ler os processos e armazená-los em uma lista
def lerProcessos(arquivo: str = "processos.txt"):
    global pid_pc # Referenciando o pid anterior
    global processos

    try:
        with open(arquivo) as procs:
            for linha in procs:
                # Associando os valores lido a características dos processos
                tempInicial, tempExecucao, prioridade = map(int, linha.split())

                # Criando o processo
                processo = Processo(pid_pc, prioridade, tempExecucao, tempInicial)

                # Armazenando o processo na lista
                processos.append(processo)

                # Incrementando o pid
                pid_pc += 1

    except Exception as e:
         print("Erro na configuração dos arquivos!", e)

# Funções auxiliares
# Função para verificar se o processo está pronto
def processos_prontos(timer: int, listaProcessos: list[int]) -> list[int]:

    # Pegando os processos prontos para executar
    prontos = []
    for processo in listaProcessos:
        if processo.tempoInicializar <= timer:
            prontos.append(processo)

    return prontos


# Funções para os algoritmos de escalonamento de tarefas
# First Come First Served
def FCFS() -> list[int]:

    ordem_execucao = []
    processosCopia = processos.copy()

    global timer # Timer da execução

    # Percorrendo a lista de processos
    while (processosCopia):

        # Pegando os processos prontos 
        prontos = processos_prontos(timer, processosCopia)

        # Verificando se há processos prontos
        if (not prontos):
            timer += 1
            continue # Como o processo ainda não surgiu, pulamos

        # Pegando o processo que surgiu primeiro
        menor = min(prontos, key = lambda p: p.tempoInicializar)

        # Executando e removendo o processo da lista
        timer += menor.tempoTotalExec # Acrescentamos ao timer o tempo de execucao do processo

        # Adicionando a execução do processo na lista de execuções
        ordem_execucao.extend([menor.pid] * menor.tempoTotalExec)

        # Removemos o processo já finalizado da lista
        processosCopia.remove(menor)

    timer = 0
    return ordem_execucao

# Shortest Job First
def SJF() -> list[int]:

    ordem_execucao = []
    processosCopia = processos.copy()

    global timer # Timer da execução

    # Percorrendo a lista de processos
    while (processosCopia):

        # Pegando os processos prontos para executar
        prontos = processos_prontos(timer, processosCopia)
        
        # Verificando se há processos prontos
        if (not prontos):
            timer += 1
            continue # Como o processo ainda não surgiu, pulamos

        # Pegando o processo com menor tempo de execução
        menor = min(prontos, key = lambda p: p.tempoTotalExec)

        # Executando e removendo o processo da lista
        timer += menor.tempoTotalExec # Acrescentamos ao timer o tempo de execucao do processo

        # Adicionando a execução da tarefa à lista de execução
        ordem_execucao.extend([menor.pid] * menor.tempoTotalExec)

        # Removemos o processo já finalizado da lista
        processosCopia.remove(menor)

    timer = 0
    return ordem_execucao

# Shortest Remaining Time First
def SRTF() -> list[int]:
    ordem_execucao = []
    processosCopia = copy.deepcopy(processos)

    global timer

    # Percorrendo a lista de processos
    while (processosCopia):

        # Pegando os processos prontos para executar
        prontos = processos_prontos(timer, processosCopia)

        # Verificando se não há nenhuma tarefa disponível ainda
        if (not prontos):
            timer += 1
            continue

        # Pegando o processo com menor tempo de execucao pendente
        prox = min(prontos, key = lambda p: p.tempoRestanteExec)

        # Executando a tarefa em tempo += 1
        prox.tempoRestanteExec -= 1
        timer += 1
        ordem_execucao.append(prox.pid)

        # Verificando se essa tarefa já pode ser removida
        if (prox.tempoRestanteExec == 0):
            processosCopia.remove(prox)

    return ordem_execucao


# Escalonamento por prioridade sem preempção
def PrioC() -> list[int]:
    ordem_execucao = []
    processosCopia = processos.copy()

    global timer # Timer da execução

    # Percorrendo a lista de processos
    while (processosCopia):

        # Pegando os processos prontos para executar
        prontos = processos_prontos(timer, processosCopia)
        
        # Verificando se há processos prontos
        if (not prontos):
            timer += 1
            continue # Como o processo ainda não surgiu, pulamos

        # Pegando o processo com maior prioridade
        prioritario = max(prontos, key = lambda p: p.prioridadeEst)

        # Executando e removendo o processo da lista
        timer += prioritario.tempoTotalExec # Acrescentamos ao timer o tempo de execucao do processo

        # Adicionando a tarefa prioritária à lista de execução
        ordem_execucao.extend([prioritario.pid] * prioritario.tempoTotalExec)

        # Removemos o processo já finalizado da lista
        processosCopia.remove(prioritario)

    timer = 0
    return ordem_execucao

# Round-robin com quantum, sem prioridade
def RRSemPrioridade() -> list[int]:
    
    fila_prontos = [] # Pegando uma fila de prontos para não se confundir com os disponíveis
    processosAdicionados = set()
    ordem_execucao = []
    processosCopia = copy.deepcopy(processos) # Criando uma cópia profunda para não modificar os objetos de fato

    global timer # Timer da execução

    # Percorrendo a lista de processos
    while (processosCopia):

        # Pegando os processos prontos para executar
        prontos = processos_prontos(timer, processosCopia)

        # Filtrando as tarefas
        for p in prontos:
            if (p.tempoRestanteExec > 0 and p.pid not in processosAdicionados):
                fila_prontos.append(p)
                processosAdicionados.add(p.pid)

        # Verificando se não há nenhum processo pronto
        if (not fila_prontos):
            timer += 1
            continue

        # Pegando a próxima tarefa da fila a executar
        prox = fila_prontos.pop(0)

        # Executando a tarefa
        tempoExecucao = min(quantum, prox.tempoRestanteExec)
        timer += tempoExecucao
        prox.tempoRestanteExec -= tempoExecucao
        ordem_execucao.extend([prox.pid] * tempoExecucao) # Adicionando a execução à lista


        # Verificando se surgiu alguma tarefa durante a execução da tarefa
        prontos = processos_prontos(timer, processosCopia)
        for p in prontos:
            if (p.tempoRestanteExec > 0 and p.pid not in processosAdicionados):
                fila_prontos.append(p)
                processosAdicionados.add(p.pid)

        # Verificando se a tarefa ainda não terminou
        if (prox.tempoRestanteExec > 0):
            fila_prontos.append(prox) # Caso não tenha terminado, vai pro final da fila

        else:
            processosCopia.remove(prox) # Caso tenha terminado, o removemos da lista de tarefas pendentes
            processosAdicionados.discard(prox.pid)


    # Retornando a lista final
    timer = 0
    return ordem_execucao

# Prioridade preemptivo
def PrioP() -> list[int]:
    ordem_execucao = []
    processosCopia = copy.deepcopy(processos) # Criando uma cópia profunda para não modificar os objetos de fato

    global timer # Timer da execução

    while (processosCopia):

        # Pegando os processos prontos para executar
        prontos = processos_prontos(timer, processosCopia)
        
        # Verificando se há processos prontos
        if (not prontos):
            timer += 1
            continue # Como o processo ainda não surgiu, pulamos

        # Pegando o processo com maior prioridade
        prioritario = max(prontos, key = lambda p: p.prioridadeEst)

        # Executa por 1 unidade de tempo → simula a preempção
        prioritario.tempoRestanteExec -= 1
        ordem_execucao.append(prioritario.pid)
        timer += 1

        # Se o processo terminou, remove da lista
        if prioritario.tempoRestanteExec == 0:
            processosCopia.remove(prioritario)

    timer = 0
    return ordem_execucao

# Round-robin com prioridade e envelhecimento
def RRPrioEvelhecimento() -> list[int]:
    fila_prontos = [] # Pegando uma fila de prontos para não se confundir com os disponíveis
    processosAdicionados = set()
    ordem_execucao = []
    processosCopia = copy.deepcopy(processos) # Criando uma cópia profunda para não modificar os objetos de fato

    global timer # Timer da execução

    # Percorrendo a lista de processos
    while (processosCopia):

        # Pegando os processos prontos para executar
        prontos = processos_prontos(timer, processosCopia)

        # Filtrando as tarefas
        for p in prontos:
            if (p.tempoRestanteExec > 0 and p.pid not in processosAdicionados):
                fila_prontos.append(p)
                processosAdicionados.add(p.pid)

        # Verificando se não há nenhum processo pronto
        if (not fila_prontos):
            timer += 1
            continue

        # Pegando o processo com maior prioridade dinâmica
        prioritario = max(fila_prontos, key=lambda p: p.prioridadeDin)

        # Executando a tarefa
        tempoExecucao = min(quantum, prioritario.tempoRestanteExec)
        timer += tempoExecucao
        prioritario.tempoRestanteExec -= tempoExecucao
        ordem_execucao.extend([prioritario.pid] * tempoExecucao) # Adicionando a execução à lista

        # Restartando a prioridade da tarefa executada
        prioritario.prioridadeDin = prioritario.prioridadeEst

        # Verificando se surgiu alguma tarefa durante a execução da tarefa
        prontos = processos_prontos(timer, processosCopia)
        for p in prontos:
            if (p.tempoRestanteExec > 0 and p.pid not in processosAdicionados):
                fila_prontos.append(p)
                processosAdicionados.add(p.pid)

        # aumenta a prioridade dinâmica dos processos que estão esperando
        for p in fila_prontos:
            if p != prioritario and p.tempoRestanteExec > 0:
                p.prioridadeDin += aging


        # Verificando se a tarefa ainda não terminou
        if (prioritario.tempoRestanteExec > 0):
            fila_prontos.append(prioritario) # Caso não tenha terminado, vai pro final da fila

        else:
            # Caso tenha terminado, o removemos da lista de tarefas pendentes
            for p in processosCopia:
                if p.pid == prioritario.pid:
                    processosCopia.remove(p)
                    break
            #processosCopia.remove(prioritario) 
            processosAdicionados.discard(prioritario.pid)


    # Retornando a lista final
    timer = 0
    return ordem_execucao

definirPropriedades()
lerProcessos()
lista1 = SJF()
lista2 = FCFS()
lista3 = PrioC()
lista4 = RRSemPrioridade()
lista5 = SRTF()
lista6 = PrioP()
lista7 = RRPrioEvelhecimento()
print(f'''
      Lista de execução por FCFS: {lista2} \n
      Lista de execução por  SJF: {lista1} \n
      Lista de execução por PrioC: {lista3} \n
      Lista de execução por Round-Robin: {lista4} \n
      Lista de execução por SRTF: {lista5} \n
      Lista de execução Por prioridade, com preempção por prioridade: {lista6} \n
      Lista de execução Por Round-Robin, com prioridade e envelhecimento: {lista7} \n'''
     )