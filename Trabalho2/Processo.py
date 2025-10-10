# Criando as variáveis globais que serão usadas 

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
    def __init__(self, prioridade: int, tempoTotal: int, tInicializar: int):
            
            # Definindo as prioridades
            self.prioridadeEst = prioridade
            self.prioridadeDin = self.prioridadeEst # Como o processo foi criado agora, din = est

            # Definindo o tempo
            self.tempoTotalExec = tempoTotal
            self.tempoRestanteExec = self.tempoTotalExec # Mesma lógica (no início, restante = total)

            # Tempo de inicialização
            self.tempoInicializar = tInicializar
