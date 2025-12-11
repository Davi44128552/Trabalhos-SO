from Memoria import Memoria, Bloco
def memoria_e_bloco_unico(memoria):
    if len(memoria.memoria) != 1:
        return False
    bloco = memoria.memoria[0]
    return bloco.livre and bloco.id == 0 and bloco.comeco == 0 and bloco.tamanho == memoria.tamanho

def show(memoria: Memoria):
    print(f"Mapa de Memória (tamanho={memoria.tamanho})")
    print("-" * (memoria.tamanho + 2))
    if memoria_e_bloco_unico(memoria):# Verifica se há apenas um bloco livre que ocupa toda a memória
        print("[" + " . " * memoria.tamanho + "]")
        print("[" + " . " * memoria.tamanho + "]")
        print("-" * (memoria.tamanho + 2))
    else:
        # Inicializar listas com '.' para cada byte da memória
        lista1 = ['.'] * memoria.tamanho
        lista2 = ['.'] * memoria.tamanho
        
        # Percorrer os blocos e marcar as posições
        for bloco in memoria.memoria:
            for i in range(bloco.comeco, bloco.comeco + bloco.tamanho):
                if not bloco.livre:  # Se o bloco está ocupado
                    lista1[i] = '#'
                    lista2[i] = str(bloco.id)
        
        # Montar as linhas com espaços entre os caracteres
        linha1 = "[" + " ".join(lista1) + "]"
        linha2 = "[" + " ".join(lista2) + "]"
        print(linha1)
        print(linha2)
        print("-" * (memoria.tamanho + 2))
    def print_block(block: Bloco):
        status = "Livre" if block.livre else "Ocupado"
        print(f"Bloco ID: {block.id}, Início: {block.comeco}, Tamanho: {block.tamanho}, Status: {status}")
    for bloco in memoria.memoria:
        print_block(bloco)
