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

    # Informações do bloco
    def __repr__(self):
        return f'Bloco(id = {self.id}, comeco = {self.comeco}, tamanho = {self.tamanho})'

# Classe da memória que realizará as operações
class Memoria:
    
    id: int
    memoria: list
    tamanho: int

    # Inicializador da memória
    def __init__(self, tamanho: int):
        self.id = 1
        self.tamanho = tamanho

        # Iniciando a memória como um único bloco gigante
        self.memoria = [Bloco(0, 0, self.tamanho, True)]

    # Função para alocar o bloco
    def alloc(self, tamanho: int, algoritmo: str):

        # Pegando o bloco que vai ser alocado
        blocoAlocar = self.chooseBlock(tamanho, algoritmo)

        # Verificando se não existe bloco livre para alocar
        if (blocoAlocar is None):
            print("Falha na alocação! Bloco livre para o requisitado indisponível")
            return

        # Removendo este bloco da memória
        self.memoria.remove(blocoAlocar)

        # Criando o bloco ocupado
        blocoOcupado = Bloco(self.id, blocoAlocar.comeco, tamanho, False)
        print("Bloco Alocado!")
        print(blocoOcupado)
        self.memoria.append(blocoOcupado)
        self.id += 1
        
        # Criando um bloco vazio caso ainda sobre espaço
        if (blocoAlocar.tamanho - tamanho > 0):
            blocoDisponivel = Bloco(0, (blocoAlocar.comeco + tamanho), (blocoAlocar.tamanho - tamanho), True)
            self.memoria.append(blocoDisponivel)

        # Ordenando a lista
        self.memoria.sort(key = lambda b: b.comeco)

    # Função para liberar o bloco
    def free_id(self, id: int):
        
        # Pegando o bloco a ser removido e o retirando da lista
        blocoRemovido = self.pegarBloco(id)

        # Verificando se o bloco removido existe (id válido)
        if (blocoRemovido is None):
            print("ERRO! Não existe bloco com este ID!")
            return 

        posicaoBlocoRemovido = self.memoria.index(blocoRemovido)

        # Lista de blocos (para união)
        blocosUnificados = [blocoRemovido]
        comecoBlocoLivre = blocoRemovido.comeco # Pegando a posição inicial do bloco

        # Verificando se tem algum vizinho vazio (para juntar)
            # Vizinho à esquerda
        if (posicaoBlocoRemovido != 0 and self.memoria[posicaoBlocoRemovido - 1].livre is True):
            blocosUnificados.append(self.memoria[posicaoBlocoRemovido - 1])
            comecoBlocoLivre = self.memoria[posicaoBlocoRemovido - 1].comeco # O novo começo vai ser o vizinho à esquerda

            # Vizinho à direita
        if (posicaoBlocoRemovido != len(self.memoria) - 1 and self.memoria[posicaoBlocoRemovido + 1].livre is True):
            blocosUnificados.append(self.memoria[posicaoBlocoRemovido + 1])

        # Construindo o bloco final
        tamanhoBloco = 0 # Tamanho do bloco final

        # Percorrendo os blocos para construir o único
        for bloco in blocosUnificados:

            # Calculando o tamanho do bloco
            tamanhoBloco += bloco.tamanho
            
        # Removendo os blocos
        for bloco in blocosUnificados:
            self.memoria.remove(bloco)

        # Criando o bloco e adicionando à memória
        blocoUnificado = Bloco(0, comecoBlocoLivre, tamanhoBloco, True)
        self.memoria.append(blocoUnificado)
        self.memoria.sort(key = lambda b: b.comeco)

    # Função para escolher o bloco de memória a ser alocado
    def chooseBlock(self, tamanho: int, algoritmo: str) -> Bloco:

        # Pegando os blocos disponiveis
        blocos_disponiveis = self.buscarBlocosDisponiveis(tamanho)
        blocoEscolhido = None

        # Verificando se realmente há blocos disponíveis
        if (not blocos_disponiveis):
            return None

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
            return None

        return blocoEscolhido

    # Função para mostrar os status da memória
    def stats(self):

        total = self.tamanho
        memoria_ocupada = sum(bloco.tamanho for bloco in self.memoria if not bloco.livre)
        memoria_livre = total - memoria_ocupada

        # Fragmentação externa: quantidade de blocos livres separados
        buracos = 0
        for bloco in self.memoria:
            if bloco.livre:
                buracos += 1

        uso_efetivo = (memoria_ocupada / total) * 100 if total > 0 else 0

        print("==== Stats =====")
        print(f"Tamanho total: {total} bytes")
        print(f"Memoria Ocupada: {memoria_ocupada} bytes")
        print(f"Memoria Livre: {memoria_livre} bytes")
        print(f"Quantidade de Buracos (fragmentação externa): {buracos}")
        print(f"Uso efetivo: {uso_efetivo:.2f}%")

    def show(self):
        print(f"Mapa de Memória (tamanho={self.tamanho})")
        print("--" * (self.tamanho))
        if (self.memoria_e_bloco_unico()):# Verifica se há apenas um bloco livre que ocupa toda a memória
            print("[" + " . " * self.tamanho + "]")
            print("[" + " . " * self.tamanho + "]")
            print("--" * (self.tamanho))
        else:
            # Inicializar listas com '.' para cada byte da memória
            lista1 = ['.'] * self.tamanho
            lista2 = ['.'] * self.tamanho
            
            # Percorrer os blocos e marcar as posições
            for bloco in self.memoria:
                for i in range(bloco.comeco, bloco.comeco + bloco.tamanho):
                    if not bloco.livre:  # Se o bloco está ocupado
                        lista1[i] = '#'
                        lista2[i] = str(bloco.id)
            
            # Montar as linhas com espaços entre os caracteres
            linha1 = "[" + " ".join(lista1) + "]"
            linha2 = "[" + " ".join(lista2) + "]"
            print(linha1)
            print(linha2)
            print("--" * (self.tamanho))

        # Função para printar bloco
        def print_block(block: Bloco):
            status = "Livre" if block.livre else "Ocupado"
            print(f"Bloco ID: {block.id}, Início: {block.comeco}, Tamanho: {block.tamanho}, Status: {status}")
            
        for bloco in self.memoria:
            print_block(bloco)

    # Funções auxiliares
        # Buscar blocos disponíveis
    def buscarBlocosDisponiveis(self, tamanho: int) -> list:

        blocos_disponiveis = []

        # Loop para percorrer todos os blocos da lista
        for bloco in self.memoria:
            if (bloco.livre is True and bloco.tamanho >= tamanho):
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

        # Verificar se a memório é bloco único
    def memoria_e_bloco_unico(self):
        if len(self.memoria) != 1:
            return False
        bloco = self.memoria[0]
        return bloco.livre and bloco.id == 0 and bloco.comeco == 0 and bloco.tamanho == self.tamanho