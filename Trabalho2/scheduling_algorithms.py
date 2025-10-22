
import json
import copy

# Criando as variáveis globais que serão usadas 
quantum_val: int = 0
aging_val: int = 0

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

    # Métricas de desempenho
    tempoChegada: int # Instante de chegada (arrival time)
    tempoConclusao: int # Instante de conclusão
    tempoEspera: int # Tempo de espera
    tempoResposta: int # Tempo de resposta (primeira execução)
    primeiraExecucao: bool # Flag para primeira execução

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

            # Métricas
            self.tempoChegada = tInicializar
            self.tempoConclusao = 0
            self.tempoEspera = 0
            self.tempoResposta = -1 # -1 indica que ainda não foi executado
            self.primeiraExecucao = True

# Funções auxiliares
# Função para verificar se o processo está pronto
def processos_prontos(timer: int, listaProcessos: list[Processo]) -> list[Processo]:

    # Pegando os processos prontos para executar
    prontos = []
    for processo in listaProcessos:
        if processo.tempoInicializar <= timer:
            prontos.append(processo)

    return prontos

# Função para calcular métricas
def calcular_metricas(processos_originais: list[Processo], ordem_execucao: list[int], num_context_switches: int):
    # Criar um dicionário para mapear PID para o objeto Processo original
    processos_map = {p.pid: p for p in processos_originais}

    # Inicializar listas para armazenar os tempos de cada processo
    turnaround_times = []
    waiting_times = []

    # Calcular tempo de conclusão e tempo de resposta para cada processo
    execucao_atual = {}
    for p in processos_originais:
        execucao_atual[p.pid] = {
            'tempo_restante': p.tempoTotalExec,
            'tempo_chegada': p.tempoInicializar,
            'tempo_conclusao': 0,
            'tempo_espera': 0,
            'tempo_resposta': -1,
            'primeira_execucao': True,
            'ultimo_tempo_executado': p.tempoInicializar # Para calcular espera
        }

    tempo_global = 0
    for pid_executado in ordem_execucao:
        # Se for um processo válido (não ocioso)
        if pid_executado != 0:
            proc_info = execucao_atual[pid_executado]

            # Calcular tempo de resposta
            if proc_info['primeira_execucao']:
                proc_info['tempo_resposta'] = tempo_global - proc_info['tempo_chegada']
                proc_info['primeira_execucao'] = False
            
            # Calcular tempo de espera
            proc_info['tempo_espera'] += (tempo_global - proc_info['ultimo_tempo_executado'])
            proc_info['ultimo_tempo_executado'] = tempo_global + 1 # Atualiza para o próximo ciclo

            proc_info['tempo_restante'] -= 1
            if proc_info['tempo_restante'] == 0:
                proc_info['tempo_conclusao'] = tempo_global + 1
        tempo_global += 1

    # Coletar as métricas finais
    for pid, info in execucao_atual.items():
        original_process = processos_map[pid]
        tt = info['tempo_conclusao'] - original_process.tempoInicializar
        tw = info['tempo_espera'] # O tempo de espera já foi acumulado corretamente

        turnaround_times.append(tt)
        waiting_times.append(tw)

    # Calcular médias
    avg_tt = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0
    avg_tw = sum(waiting_times) / len(waiting_times) if waiting_times else 0

    return {
        "tempo_medio_vida": avg_tt,
        "tempo_medio_espera": avg_tw,
        "trocas_contexto": num_context_switches
    }


# Funções para os algoritmos de escalonamento de tarefas
# First Come First Served
def FCFS(processos_entrada: list[Processo]) -> tuple[list[int], int, list[tuple[int, int]]]:

    ordem_execucao = []
    processosCopia = copy.deepcopy(processos_entrada)
    processosCopia.sort(key=lambda p: p.tempoInicializar) # Ordena por tempo de chegada

    timer = 0 # Timer da execução
    num_context_switches = 0
    last_pid_executed = -1
    animation_steps = []

    # Percorrendo a lista de processos
    while (processosCopia):

        # Pegando os processos prontos 
        prontos = processos_prontos(timer, processosCopia)

        # Verificando se há processos prontos
        if (not prontos):
            ordem_execucao.append(0) # Tempo ocioso
            animation_steps.append((timer, 0))
            timer += 1
            continue # Como o processo ainda não surgiu, pulamos

        # Pegando o processo que surgiu primeiro
        # Já está ordenado, então o primeiro pronto é o FCFS
        menor = prontos[0]

        # Contagem de troca de contexto
        if last_pid_executed != -1 and last_pid_executed != menor.pid:
            num_context_switches += 1
        last_pid_executed = menor.pid

        # Executando e removendo o processo da lista
        for _ in range(menor.tempoTotalExec):
            ordem_execucao.append(menor.pid)
            animation_steps.append((timer, menor.pid))
            timer += 1

        # Removemos o processo já finalizado da lista
        processosCopia.remove(menor)

    return ordem_execucao, num_context_switches, animation_steps

# Shortest Job First
def SJF(processos_entrada: list[Processo]) -> tuple[list[int], int, list[tuple[int, int]]]:

    ordem_execucao = []
    processosCopia = copy.deepcopy(processos_entrada)

    timer = 0 # Timer da execução
    num_context_switches = 0
    last_pid_executed = -1
    animation_steps = []

    # Percorrendo a lista de processos
    while (processosCopia):

        # Pegando os processos prontos para executar
        prontos = processos_prontos(timer, processosCopia)
        
        # Verificando se há processos prontos
        if (not prontos):
            ordem_execucao.append(0) # Tempo ocioso
            animation_steps.append((timer, 0))
            timer += 1
            continue # Como o processo ainda não surgiu, pulamos

        # Pegando o processo com menor tempo de execução
        menor = min(prontos, key = lambda p: p.tempoTotalExec)

        # Contagem de troca de contexto
        if last_pid_executed != -1 and last_pid_executed != menor.pid:
            num_context_switches += 1
        last_pid_executed = menor.pid

        # Executando e removendo o processo da lista
        for _ in range(menor.tempoTotalExec):
            ordem_execucao.append(menor.pid)
            animation_steps.append((timer, menor.pid))
            timer += 1

        # Removemos o processo já finalizado da lista
        processosCopia.remove(menor)

    return ordem_execucao, num_context_switches, animation_steps

# Shortest Remaining Time First
def SRTF(processos_entrada: list[Processo]) -> tuple[list[int], int, list[tuple[int, int]]]:
    ordem_execucao = []
    processosCopia = copy.deepcopy(processos_entrada)

    timer = 0
    num_context_switches = 0
    last_pid_executed = -1
    animation_steps = []

    # Percorrendo a lista de processos
    while (processosCopia):

        # Pegando os processos prontos para executar
        prontos = processos_prontos(timer, processosCopia)

        # Verificando se não há nenhuma tarefa disponível ainda
        if (not prontos):
            ordem_execucao.append(0) # Tempo ocioso
            animation_steps.append((timer, 0))
            timer += 1
            continue

        # Pegando o processo com menor tempo de execucao pendente
        prox = min(prontos, key = lambda p: p.tempoRestanteExec)

        # Contagem de troca de contexto
        if last_pid_executed != -1 and last_pid_executed != prox.pid:
            num_context_switches += 1
        last_pid_executed = prox.pid

        # Executando a tarefa em tempo += 1
        prox.tempoRestanteExec -= 1
        ordem_execucao.append(prox.pid)
        animation_steps.append((timer, prox.pid))
        timer += 1

        # Verificando se essa tarefa já pode ser removida
        if (prox.tempoRestanteExec == 0):
            processosCopia.remove(prox)

    return ordem_execucao, num_context_switches, animation_steps


# Escalonamento por prioridade sem preempção
def PrioC(processos_entrada: list[Processo]) -> tuple[list[int], int, list[tuple[int, int]]]:
    ordem_execucao = []
    processosCopia = copy.deepcopy(processos_entrada)

    timer = 0 # Timer da execução
    num_context_switches = 0
    last_pid_executed = -1
    animation_steps = []

    # Percorrendo a lista de processos
    while (processosCopia):

        # Pegando os processos prontos para executar
        prontos = processos_prontos(timer, processosCopia)
        
        # Verificando se há processos prontos
        if (not prontos):
            ordem_execucao.append(0) # Tempo ocioso
            animation_steps.append((timer, 0))
            timer += 1
            continue # Como o processo ainda não surgiu, pulamos

        # Pegando o processo com maior prioridade
        prioritario = max(prontos, key = lambda p: p.prioridadeEst)

        # Contagem de troca de contexto
        if last_pid_executed != -1 and last_pid_executed != prioritario.pid:
            num_context_switches += 1
        last_pid_executed = prioritario.pid

        # Executando e removendo o processo da lista
        for _ in range(prioritario.tempoTotalExec):
            ordem_execucao.append(prioritario.pid)
            animation_steps.append((timer, prioritario.pid))
            timer += 1

        # Removemos o processo já finalizado da lista
        processosCopia.remove(prioritario)

    return ordem_execucao, num_context_switches, animation_steps

# Round-robin com quantum, sem prioridade
def RRSemPrioridade(processos_entrada: list[Processo], quantum: int) -> tuple[list[int], int, list[tuple[int, int]]]:
    
    fila_prontos = [] # Pegando uma fila de prontos para não se confundir com os disponíveis
    processosAdicionados = set()
    ordem_execucao = []
    processosCopia = copy.deepcopy(processos_entrada) # Criando uma cópia profunda para não modificar os objetos de fato

    timer = 0 # Timer da execução
    num_context_switches = 0
    last_pid_executed = -1
    animation_steps = []

    # Percorrendo a lista de processos
    while (processosCopia or fila_prontos):

        # Adiciona processos que chegam no tempo atual à fila de prontos
        for p in [proc for proc in processosCopia if proc.tempoInicializar <= timer and proc.pid not in processosAdicionados]:
            fila_prontos.append(p)
            processosAdicionados.add(p.pid)
        
        # Se não há processos na fila e ainda há processos a chegar, avança o tempo
        if not fila_prontos and processosCopia:
            ordem_execucao.append(0) # Tempo ocioso
            animation_steps.append((timer, 0))
            timer += 1
            continue
        
        # Se não há processos na fila e nem a chegar, encerra
        if not fila_prontos and not processosCopia:
            break

        # Pegando a próxima tarefa da fila a executar
        prox = fila_prontos.pop(0)

        # Contagem de troca de contexto
        if last_pid_executed != -1 and last_pid_executed != prox.pid:
            num_context_switches += 1
        last_pid_executed = prox.pid

        # Executando a tarefa
        tempoExecucao = min(quantum, prox.tempoRestanteExec)
        
        for _ in range(tempoExecucao):
            ordem_execucao.append(prox.pid)
            animation_steps.append((timer, prox.pid))
            timer += 1
            # Adiciona processos que chegam durante a execução atual
            for p in [proc for proc in processosCopia if proc.tempoInicializar <= timer and proc.pid not in processosAdicionados]:
                fila_prontos.append(p)
                processosAdicionados.add(p.pid)

        prox.tempoRestanteExec -= tempoExecucao

        # Verificando se a tarefa ainda não terminou
        if (prox.tempoRestanteExec > 0):
            fila_prontos.append(prox) # Caso não tenha terminado, vai pro final da fila

        else:
            # Removemos o processo já finalizado da lista de processosCopia
            # Encontra o processo original em processosCopia para remover
            for i, p in enumerate(processosCopia):
                if p.pid == prox.pid:
                    processosCopia.pop(i)
                    break
            processosAdicionados.discard(prox.pid) # Remove do set de adicionados

    return ordem_execucao, num_context_switches, animation_steps

# Prioridade preemptivo
def PrioP(processos_entrada: list[Processo]) -> tuple[list[int], int, list[tuple[int, int]]]:
    ordem_execucao = []
    processosCopia = copy.deepcopy(processos_entrada) # Criando uma cópia profunda para não modificar os objetos de fato

    timer = 0 # Timer da execução
    num_context_switches = 0
    last_pid_executed = -1
    animation_steps = []

    while (processosCopia):

        # Pegando os processos prontos para executar
        prontos = processos_prontos(timer, processosCopia)
        
        # Verificando se há processos prontos
        if (not prontos):
            ordem_execucao.append(0) # Tempo ocioso
            animation_steps.append((timer, 0))
            timer += 1
            continue # Como o processo ainda não surgiu, pulamos

        # Pegando o processo com maior prioridade
        prioritario = max(prontos, key = lambda p: p.prioridadeEst)

        # Contagem de troca de contexto
        if last_pid_executed != -1 and last_pid_executed != prioritario.pid:
            num_context_switches += 1
        last_pid_executed = prioritario.pid

        # Executa por 1 unidade de tempo → simula a preempção
        prioritario.tempoRestanteExec -= 1
        ordem_execucao.append(prioritario.pid)
        animation_steps.append((timer, prioritario.pid))
        timer += 1

        # Se o processo terminou, remove da lista
        if prioritario.tempoRestanteExec == 0:
            processosCopia.remove(prioritario)

    return ordem_execucao, num_context_switches, animation_steps

# Round-robin com prioridade e envelhecimento
def RRPrioEvelhecimento(processos_entrada: list[Processo], quantum: int, aging: int) -> tuple[list[int], int, list[tuple[int, int]]]:
    fila_prontos = []
    processosAdicionados = set() # Para controlar quais PIDs já foram adicionados à fila
    ordem_execucao = []
    processosCopia = copy.deepcopy(processos_entrada)

    timer = 0
    num_context_switches = 0
    last_pid_executed = -1
    animation_steps = []

    # Dicionário para rastrear o tempo que cada processo está esperando na fila
    tempo_espera_fila = {p.pid: 0 for p in processosCopia}

    while (processosCopia or fila_prontos):
        # Adiciona processos que chegam no tempo atual à fila de prontos
        for p in [proc for proc in processosCopia if proc.tempoInicializar <= timer and proc.pid not in processosAdicionados]:
            fila_prontos.append(p)
            processosAdicionados.add(p.pid)
            tempo_espera_fila[p.pid] = 0 # Reinicia o contador de espera na fila

        # Aplica envelhecimento aos processos na fila que não estão sendo executados
        # A prioridade dinâmica é aumentada para processos que estão esperando
        for p_fila in fila_prontos:
            if p_fila.pid != last_pid_executed: # Não envelhece o processo que acabou de ser executado
                tempo_espera_fila[p_fila.pid] += 1
                if tempo_espera_fila[p_fila.pid] >= aging: # Se atingiu o limite de envelhecimento
                    p_fila.prioridadeDin += 1 # Aumenta a prioridade dinâmica
                    tempo_espera_fila[p_fila.pid] = 0 # Reseta o contador de espera

        # Se não há processos na fila e ainda há processos a chegar, avança o tempo
        if not fila_prontos and processosCopia:
            ordem_execucao.append(0) # Tempo ocioso
            animation_steps.append((timer, 0))
            timer += 1
            continue

        # Se não há processos na fila e nem a chegar, encerra
        if not fila_prontos and not processosCopia:
            break

        # Escolhe o processo com maior prioridade dinâmica da fila
        # Se houver empate, usa FCFS (o que entrou primeiro na fila)
        fila_prontos.sort(key=lambda p: (-p.prioridadeDin, p.tempoInicializar)) # Maior prioridade primeiro, depois FCFS
        prox = fila_prontos.pop(0)

        # Contagem de troca de contexto
        if last_pid_executed != -1 and last_pid_executed != prox.pid:
            num_context_switches += 1
        last_pid_executed = prox.pid

        # Executando a tarefa
        tempoExecucao = min(quantum, prox.tempoRestanteExec)

        for _ in range(tempoExecucao):
            ordem_execucao.append(prox.pid)
            animation_steps.append((timer, prox.pid))
            timer += 1
            # Adiciona processos que chegam durante a execução atual
            for p in [proc for proc in processosCopia if proc.tempoInicializar <= timer and proc.pid not in processosAdicionados]:
                fila_prontos.append(p)
                processosAdicionados.add(p.pid)
                tempo_espera_fila[p.pid] = 0 # Reinicia o contador de espera na fila

            # Aplica envelhecimento durante a execução do quantum
            for p_fila in fila_prontos:
                if p_fila.pid != prox.pid: # Não envelhece o processo que está sendo executado
                    tempo_espera_fila[p_fila.pid] += 1
                    if tempo_espera_fila[p_fila.pid] >= aging:
                        p_fila.prioridadeDin += 1
                        tempo_espera_fila[p_fila.pid] = 0

        prox.tempoRestanteExec -= tempoExecucao

        # Verificando se a tarefa ainda não terminou
        if (prox.tempoRestanteExec > 0):
            prox.prioridadeDin = prox.prioridadeEst # Reseta prioridade dinâmica ao voltar para a fila
            fila_prontos.append(prox) # Caso não tenha terminado, vai pro final da fila
            tempo_espera_fila[prox.pid] = 0 # Reinicia o contador de espera na fila
        else:
            # Removemos o processo já finalizado da lista de processosCopia
            for i, p in enumerate(processosCopia):
                if p.pid == prox.pid:
                    processosCopia.pop(i)
                    break
            processosAdicionados.discard(prox.pid)
            if prox.pid in tempo_espera_fila: # Limpa o registro de espera
                del tempo_espera_fila[prox.pid]

    return ordem_execucao, num_context_switches, animation_steps

