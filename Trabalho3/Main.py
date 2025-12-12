# Importando a memoria
from Memoria import Memoria
from show import show
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

    # Se o usuário não digitou nada, voltar para o início do loop
    if not comando:
        continue

    # Leitura de um exit
    if (comando[0] == 'exit'):
        break
    
    # Leitura de um init
    if (comando[0] == 'init'):

        # Verificando se a quantidade de argumento é válida
        if (len(comando) != 2):
            print("ERRO! Número de argumentos inválido para o comando!")
            continue
        
        # Inicializando a memória 
        memoria = Memoria(int(comando[1]))

    # Leitura de um alloc
    elif (comando[0] == 'alloc'):

        # Verificando se existe uma memória para ser alocado
        if (memoria is None):
            print("ERRO! Não existe memória para alocar!")
            continue

        # Verificando se a quantidade de argumentos é válida
        if (len(comando) != 3):
            print("ERRO! Número de argumentos inválido para o comando!")
            continue

        # Realizando a alocação de um bloco
        memoria.alloc(int(comando[1]), comando[2])

    # Liberação de um bloco de memória
    elif (comando[0] == 'freeid'):

        # Verificando se existe uma memória para ser alocado
        if (memoria is None):
            print("ERRO! Não existe memória para alocar!")
            continue
    
        # Verificando se a quantidade de argumentos é válida
        if (len(comando) != 2):
            print("ERRO! Número de argumentos inválido para o comando!")

        # Realizando a liberação do bloco solicitada
        memoria.free_id(int(comando[1]))

    #chamando show
    elif (comando[0] == 'show'):

        # Verificando se existe uma memória para ser alocado
        if (memoria is None):
            print("ERRO! Não existe memória para alocar!")
            continue

        # Importando a função show
        from show import show

        # Mostrando o estado atual da memória
        show(memoria)