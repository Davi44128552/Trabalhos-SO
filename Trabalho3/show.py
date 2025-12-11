from Memoria import Memoria, Bloco
def memoria_e_bloco_unico(memoria):
    if len(memoria.memoria) != 1:
        return False
    bloco = memoria.memoria[0]
    return bloco.livre and bloco.id == 0 and bloco.comeco == 0 and bloco.tamanho == memoria.tamanho

def show(memoria: Memoria):
    print(f"Mapa de Memória (tamanho={memoria.tamanho})")
    print("-" * memoria.tamanho+2)
    if memoria_e_bloco_unico(memoria):# Verifica se há apenas um bloco livre que ocupa toda a memória
        print("[" + " . " * memoria.tamanho + "]")
        print("[" + " . " * memoria.tamanho + "]")
        print("-" * memoria.tamanho+2)
    elif len(memoria.memoria) <= 1:  # Se houver 0 ou 1 blocos, imprime de forma simples
        linha1 = "["
        linha2 = "["
        for bloco in memoria.memoria:
            simbolo = " . " if bloco.livre else " X "
            linha1 += simbolo * bloco.tamanho
            linha2 += f"{bloco.id}".center(bloco.tamanho * 3)
        linha1 += "]"
        linha2 += "]"
        print(linha1)
        print(linha2)
        print("-" * memoria.tamanho+2)
    def print_block(block: Bloco):
        status = "Livre" if block.livre else "Ocupado"
        print(f"Bloco ID: {block.id}, Início: {block.comeco}, Tamanho: {block.tamanho}, Status: {status}")
    for bloco in memoria.memoria:
        print_block(bloco)
