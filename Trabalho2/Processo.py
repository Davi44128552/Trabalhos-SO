# Importando bibliotecas necessárias
import json

# Criando as variáveis globais que serão usadas 
quantum: int = 0
aging: int = 0

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

# Criando uma função para leitura de arquivo
def definirPropriedades(arquivo_config):
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


definirPropriedades("config.json")
print(quantum, aging)   
