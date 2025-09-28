# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <unistd.h>
# include <sys/types.h>
# include <sys/wait.h>

#define MAX_CMD_LEN 256
#define MAX_ARGS 32

// Array para armazenar PIDs de processos em background
pid_t bg_processes[10];
int bg_count = 0;
int loop = 1;
pid_t last_child_pid = 0; // Armazena PID do último processo filho

void parse_command(char *input, char **args, int *background) {
    int argc = 0; // Posicao dos argumentos
    char *token = strtok(input, " \t");

    // Lendo o comando e seus argumentos
    while (token != NULL && argc < MAX_ARGS){
        args[argc] = token; // Definindo este argumento pelo token lido por strtok
        argc++; // Incrementando argc para a sua proxima posicao
        token = strtok(NULL, " \t"); // Pegando o proximo argumento 
    }

    // Definindo o último argumento como Null para o exec
    args[argc] = NULL;
}

void execute_command(char **args, int background) {
    // TODO: Implementar execução
    // Usar fork() e execvp()
    // Gerenciar background se necessário
}

int is_internal_command(char **args) {
    // Verificando as strings para ver se alguma é um comando interno

    // Caso o comando tenha sido "exit"
    if (strcmp(args[0], "exit") == 0){
        return 1;
    }

    // Caso o comando tenha sido "pid"
    if (strcmp(args[0], "pid") == 0){
        return 1;
    }

    // Caso não tenha sido nenhum comando interno
    return 0;
}

void handle_internal_command(char **args) {
    
    // Caso o comando recebido tenha sido "exit"
    if (strcmp(args[0], "exit") == 0){
        loop = 0;
    }

}

int main() {
    char input[MAX_CMD_LEN];
    char *args[MAX_ARGS];
    int background;

    printf("Mini-Shell iniciado (PID: %d)\n", getpid());
    printf("Digite 'exit' para sair\n\n");

    while (loop == 1) {
        printf("minishell> ");
        fflush(stdout);

        // Ler entrada do usuário
        if (!fgets(input, sizeof(input), stdin)) {
            break;
        }

        // Remover quebra de linha
        input[strcspn(input, "\n")] = 0;

        // Ignorar linhas vazias
        if (strlen(input) == 0) {
            continue;
        }

        // Fazer parsing do comando
        parse_command(input, args, &background);

        // Executar comando
        if (is_internal_command(args)) {
            handle_internal_command(args);
        } 

        else {
            execute_command(args, background);
        }
    }

    printf("Shell encerrado!\n");
    return EXIT_SUCCESS;

}