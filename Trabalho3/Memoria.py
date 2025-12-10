# Classe para os blocos de memória
class Bloco:

    # Atributos de bloco
    id: int
    comeco: int
    tamanho: int
    tamanho_alocado: int
    livre: bool

    # Construtor do bloco
    def __init__(self, id: int, comeco: int, tamanho:int, livre: bool):
        self.id = id
        self.tamanho = tamanho
        self.livre = livre

# Classe da memória que realizará as operações
class Memoria:
    
    id: int
    memoria: list()
    tamanho: int

    # Inicializador da memória
    def __init__(self, id: int, tamanho: int):
        self.id = id
        self.tamanho = tamanho

        # Iniciando a memória como um único bloco gigante
        self.memoria = [Bloco(None, 0, self.tamanho, True)]

    # Função para alocar o bloco
    

    # Função para escolher o bloco de memória a ser alocado
    def chooseBlock(self, tamanho: int, algoritmo: str) -> Bloco:

        # Pegando os blocos disponiveis
        blocos_disponiveis = buscarBlocosLivres()
        blocoEscolhido = None

        # Escolhendo o bloco de acordo com o algoritmo escolhido
        algoritmo = algoritmo.lower()
        if (algoritmo == 'first'):

            # Pegamos simplesmente o primeiro valor da lista
            blocoEscolhido = blocos_disponiveis[0]

        elif (algoritmo == 'best'):
            
            # Procurando o melhor bloco
            for bloco in blocos_disponiveis:
                if (bloco.tamanho < blocoEscolhido.tamanho or blocoEscolhido is None): 
                    
                    # Se o tamanho do bloco atual for menor, ele é o melhor
                    blocoEscolhido = bloco

        elif (algoritmo == 'worst'):
            
            # Segue a mesma lógica do best-fit, mas agora verificamos o bloco maior
            for bloco in blocos_disponiveis:
                if (bloco.tamanho > blocoEscolhido.tamanho or blocoEscolhido is None):

                     # Se o tamanho do bloco atual for maior, ele é o melhor
                    blocoEscolhido = bloco

        # Algoritmo não reconhecido
        else:
            print("ERRO! Algoritmo não reconhecido!")

        return blocoEscolhido

    # Funções auxiliares
        # Buscar blocos disponíveis
    def buscarBlocosLivres(self) -> list():

        blocos_disponiveis = []

        # Loop para percorrer todos os blocos da lista
        for bloco in self.memoria:
            if (bloco.livre is True):
                blocos_disponiveis.append(bloco)

        return bloco