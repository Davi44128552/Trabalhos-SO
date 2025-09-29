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
pid_t last_child_pid = 0; // Armazena PID do último processo filho

void clean_finished_processes(void) {
    while (bg_count > 0) {
        pid_t pid = waitpid(-1, NULL, WNOHANG);
        if (pid <= 0) break; // Nenhum processo terminou
        // Remover PID da lista de bg_processes
        for (int i = 0; i < bg_count; i++) {
            if (bg_processes[i] == pid) {
                // Deslocar elementos para preencher a lacuna
                for (int j = i; j < bg_count - 1; j++) {
                    bg_processes[j] = bg_processes[j + 1];
                }
                bg_count--;
                printf("minishell>[job %d] (%d) + Done\n", i + 1, pid);
                break;
            }
        }
    }
}
       
void parse_command(char *input, char **args, int *background) {
    int argc = 0;
    *background = 0;
    char *token = strtok(input, " \t");
    while (token != NULL && argc < MAX_ARGS) {
        if (strcmp(token, "&") == 0) {
            *background = 1;
        } else {
            args[argc++] = token;
        }
        token = strtok(NULL, " \t");
    }
    args[argc] = NULL;
}

void execute_command(char **args, int background) {
    pid_t pid = fork();
    if (pid < 0) {
        perror("Erro ao criar o processo filho");
        exit(1);
    }
    if (pid == 0) {
        if (execvp(args[0], args) == -1) {
            perror("Erro ao tentar executar o comando execvp no minishell");
            exit(1);
        }
    } else {
        last_child_pid = pid;
        if (background) {
            if (bg_count < 10) {
                bg_processes[bg_count++] = pid;
                printf("[minishell] Processo %d rodando em background\n", pid);
            } else {
                printf("Limite de processos em background atingido!\n");
            }
        } else {
            int status;
            if (waitpid(last_child_pid, &status, 0) == -1) {
                perror("Erro ao tentar rodar o waitpid");
            }
        }
    }
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
        printf("Shell encerrado!\n");
        exit(0); // Simplesmente encerramos o programa e retornamos 0
    }

    // Caso o comando recebido tenha sido "pid"
    else if (strcmp(args[0], "pid") == 0){

        // Printando o pid do shell
        printf("valor PID da execucao do shell: %d \n", getpid());

        // Verificando se ha um processo filho para ser mostrado
        if (last_child_pid != 0){
            // Caso haja um filho, pegamos o seu valor de processo
            printf("O valor do último filho do processo e %d \n", last_child_pid);
        }

    }
    else if(strcmp(args[0], "wait") == 0){
        if (bg_count == 0) {
            printf("Nenhum processo em background\n");
        } else {
            while (bg_count > 0) {
                clean_finished_processes();
                sleep(1); // Espera um pouco antes de checar de novo
            }
            printf("Todos os processos terminaram\n");
        }
    }

}

int main() {
    char input[MAX_CMD_LEN];
    char *args[MAX_ARGS];
    int background;

    printf("Mini-Shell iniciado (PID: %d)\n", getpid());
    printf("Digite 'exit' para sair\n\n");

    while (1) {
        clean_finished_processes();
        printf("minishell> ");
        fflush(stdout);

        if (!fgets(input, sizeof(input), stdin)) {
            break;
        }
        input[strcspn(input, "\n")] = 0;
        if (strlen(input) == 0) {
            continue;
        }
        parse_command(input, args, &background);
        if (is_internal_command(args)) {
            handle_internal_command(args);
        } else {
            execute_command(args, background);
        }
    }

}