# Importando a memoria
from Memoria import Memoria

# Função help, para orientar o usuário
def help():
    print("="*40, " COMANDOS ", "="*40)

    # Init
    print("init <n> - Inicia a memória com n bytes")

    # Alloc
    print("alloc <n> <alg> - Aloca um bloco de n bytes na memória por meio do algoritmo alg")
    print("\t [ first ] First-Fit   [ best ] Best-Fit   [ worst ] Worst-Fit")

    # Freeid
    print("freeid <id> - Liberar o bloco com id especificado")

    # Stats
    print("stats - Mostra os status da memória")

    # Show
    print("show - Mostra o mapa de memória e os blocos existentes pelo tamanho da memória")

    # Show proporcional
    print("showp - Mostra o mapa de memória em que a memória tem um tamanho específico")

    # Help
    print("help - Mostra novamente os comandos")

    # Exit
    print("exit - Encerra o programa")

    print("=" * 92)

# Função Main
def main():
    # Declarando a memória inicialmente vazia
    memoria = None

    # Iniciando com help
    help()

    # Loop principal
    while (True):
        try:
            comando = input("> ").strip().lower().split() # Lendo o comando do usuário

        except (EOFError, KeyboardInterrupt):
            # Caso o usuário tenha teclado um atalho para encerrar
            print("\nPrograma encerrado!")
            break

        # Leitura de um exit
        if (comando[0] == 'exit'):

            # Verificando se o comando está inválido
            if (len(comando) != 1):
                print("ERRO! Número de argumentos inválido para o comando!")
                continue

            # Encerrando a aplicação
            break

        # Leitura de um help
        if (comando[0] == 'help'):

            # Verificando se os argumentos são válidos
            if (len(comando) != 1):
                print("ERRO! Número de argumentos inválido para o comando!")
                continue

            # Mostrando os comandos novamente
            help()
        
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
                print("ERRO! Não existe memória para liberar blocos!")
                continue
        
            # Verificando se a quantidade de argumentos é válida
            if (len(comando) != 2):
                print("ERRO! Número de argumentos inválido para o comando!")
                continue

            # Verificando se o usuário quer liberar um bloco vazio
            if (comando[1] == 0):
                print("ERRO! Não tem como liberar um bloco vazio!")
                continue

            # Realizando a liberação do bloco solicitada
            memoria.free_id(int(comando[1]))

        # Mostrar os status da memória
        elif (comando[0] == 'stats'):

            # Verificando se existe uma memória para mostrar seu mapa
            if (memoria is None):
                print("ERRO! Não existe memória para mostrar status!")
                continue

            # Verificando se a quantidade de argumentos é válida
            if (len(comando) != 1):
                print("ERRO! Número de argumentos inválido para o comando!")
                continue

            # Caso esteja tudo certo, executamos o comando
            memoria.stats()

        # Mostrar o mapa de memória
        elif (comando[0] == 'show'):

            # Verificando se existe uma memória para mostrar seu mapa
            if (memoria is None):
                print("ERRO! Não existe memória para mostrar mapa!")
                continue

            # Verificando se a quantidade de argumentos é válida
            if (len(comando) != 1):
                print("ERRO! Número de argumentos inválido para o comando!")
                continue

            # Caso esteja tudo certo, executamos o comando
            memoria.show()

        # Mostrar o mapa de memória
        elif (comando[0] == 'showp'):

            # Verificando se existe uma memória para mostrar seu mapa
            if (memoria is None):
                print("ERRO! Não existe memória para mostrar mapa!")
                continue

            # Verificando se a quantidade de argumentos é válida
            if (len(comando) != 1):
                print("ERRO! Número de argumentos inválido para o comando!")
                continue

            # Caso esteja tudo certo, executamos o comando
            memoria.show_proporcional()

# Executando a main
if __name__ == "__main__":
    main()
