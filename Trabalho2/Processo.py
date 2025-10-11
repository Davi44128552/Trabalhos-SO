# Importando bibliotecas necessárias
import json

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
         print("Erro na configuração dos arquivos!")

# Funções para os algoritmos de escalonamento de tarefas

# Shortest Job First
def SJF():

    ordem_execucao = []

    global timer # Timer da execução

    # Percorrendo a lista de processos
    while (processos):

        # Pegando os processos prontos para executar
        prontos = []
        for processo in processos:
            if processo.tempoInicializar <= timer:
                prontos.append(processo)
        
        # Verificando se há processos prontos
        if (not prontos):
            timer += 1
            continue # Como o processo ainda não surgiu, pulamos

        # Pegando o processo com menor tempo de execução
        menor = min(prontos, key = lambda p: p.tempoTotalExec)

        # Caso contrário, o executamos e removemos da lista
        timer += menor.tempoTotalExec # Acrescentamos ao timer o tempo de execucao do processo

        ordem_execucao.append(menor.pid)

        # Removemos o processo já finalizado da lista
        processos.remove(menor)

    return ordem_execucao

lerProcessos()

lista = SJF()
print(lista)
