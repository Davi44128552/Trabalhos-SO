# Importando a memoria
from Memoria import Memoria

# Declarando a memória inicialmente vazia
memoria = None

# Loop principal
while (True):
    try:
        comando = input("> ").strip().lower().split() # Lendo o comando do usuário

    except (EOFError, KeyboardInterrupt):
        # Caso o usuário tenha teclado um atalho para encerrar
        print("\nPrograma encerrado!")
        break

    print(comando)
    # Leitura de um init
    if (comando[0] == 'init'):

        # Verificando se a quantidade de argumento é válida
        if len(comando != 2):
            print("ERRO! Número de argumentos inválido para o comando!")
            continue
        
        # Inicializando a memória 
        memoria = Memoria(comando[1])