# Classe para os blocos de memória
class Bloco:

    # Atributos de bloco
    id: int
    comeco: int
    tamanho: int
    livre: bool

    # Construtor do bloco
    def __init__(self, id: int, comeco: int, tamanho:int, livre: bool):
        self.id = id
        self.comeco = comeco
        self.tamanho = tamanho
        self.livre = livre

# Classe da memória que realizará as operações
class Memoria:
    
    id: int = 1
    memoria: list
    tamanho: int

    # Inicializador da memória
    def __init__(self, tamanho: int):
        self.tamanho = tamanho

        # Iniciando a memória como um único bloco gigante
        self.memoria = [Bloco(None, 0, self.tamanho, True)]

    # Função para alocar o bloco
    def alloc(self, tamanho: int, algoritmo: str):

        # Pegando o bloco que vai ser alocado
        blocoAlocar = self.chooseBlock(algoritmo)

        # Removendo este bloco da memória
        self.memoria.remove(blocoAlocar)

        # Criando os dois blocos a partir do alocado
        blocoOcupado = Bloco(self.id, blocoAlocar.comeco, tamanho, False)
        self.memoria.append(blocoOcupado)
        self.id += 1
        
        blocoDisponivel = Bloco(self.id, (blocoAlocar.comeco + tamanho), (blocoAlocar.tamanho - tamanho), True)
        self.memoria.append(blocoDisponivel)
        self.id += 1

        # Ordenando a lista
        self.memoria.sort(key = lambda b: b.comeco)

    # Função para liberar o bloco
    def free_id(self, id: int):
        
        # Pegando o bloco a ser removido e o retirando da lista
        blocoRemovido = self.pegarBloco(id)
        self.memoria.remove(blocoRemovido)

        # Lista de blocos (para união)
        blocosUnificados = [blocoRemovido]
        comecoBlocoLivre = blocoRemovido.comeco # Pegando a posição inicial do bloco

        # Verificando se tem algum vizinho vazio (para juntar)
        posicaoBlocoRemovido = self.memoria.index(blocoRemovido)

            # Vizinho à esquerda
        if (posicaoBlocoRemovido != 0 and self.memoria[posicaoBlocoRemovido - 1].livre is True):
            blocosUnificados.append(self.memoria[posicaoBlocoRemovido - 1])
            comecoBlocoLivre = self.memoria[posicaoBlocoRemovido - 1].comeco # O novo começo vai ser o vizinho à esquerda
            self.memoria.remove(self.memoria[posicaoBlocoRemovido - 1])

            # Vizinho à direita
        if (posicaoBlocoRemovido != len(self.memoria) - 1 and self.memoria[posicaoBlocoRemovido + 1].livre is True):
            blocosUnificados.append(self.memoria[posicaoBlocoRemovido + 1])
            self.memoria.remove(self.memoria[posicaoBlocoRemovido + 1])

        # Construindo o bloco final
        tamanhoBloco = 0 # Tamanho do bloco final

        # Percorrendo os blocos para construir o único
        for bloco in blocosUnificados:

            # Calculando o tamanho do bloco
            tamanhoBloco += bloco.tamanho

        # Criando o bloco e adicionando à memória
        blocoUnificado = Bloco(self.id, comecoBlocoLivre, tamanhoBloco, True)
        self.memoria.append(blocoUnificado)
        self.memoria.sort(key = lambda b: b.comeco)

    # Função para escolher o bloco de memória a ser alocado
    def chooseBlock(self, algoritmo: str) -> Bloco:

        # Pegando os blocos disponiveis
        blocos_disponiveis = self.buscarBlocosLivres()
        blocoEscolhido = None

        # Escolhendo o bloco de acordo com o algoritmo escolhido
        algoritmo = algoritmo.lower()
        if (algoritmo == 'first'):

            # Pegamos simplesmente o primeiro valor da lista
            blocoEscolhido = blocos_disponiveis[0]

        elif (algoritmo == 'best'):
            
            # Procurando o melhor bloco
            for bloco in blocos_disponiveis:
                if (blocoEscolhido is None or bloco.tamanho < blocoEscolhido.tamanho): 
                    
                    # Se o tamanho do bloco atual for menor, ele é o melhor
                    blocoEscolhido = bloco

        elif (algoritmo == 'worst'):
            
            # Segue a mesma lógica do best-fit, mas agora verificamos o bloco maior
            for bloco in blocos_disponiveis:
                if (blocoEscolhido is None or bloco.tamanho > blocoEscolhido.tamanho):

                     # Se o tamanho do bloco atual for maior, ele é o melhor
                    blocoEscolhido = bloco

        # Algoritmo não reconhecido
        else:
            print("ERRO! Algoritmo não reconhecido!")

        return blocoEscolhido

    # Funções auxiliares
        # Buscar blocos disponíveis
    def buscarBlocosLivres(self) -> list:

        blocos_disponiveis = []

        # Loop para percorrer todos os blocos da lista
        for bloco in self.memoria:
            if (bloco.livre is True):
                blocos_disponiveis.append(bloco)

        return blocos_disponiveis
    
        # Pegar um bloco específico
    def pegarBloco(self, id: int):

        blocoEncontrado = None

        # Percorrendo os blocos procurando o desejado
        for bloco in self.memoria:
            if (bloco.id == id):
                blocoEncontrado = bloco
                break
    
        return blocoEncontrado