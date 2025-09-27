/*
 * mini_shell.c
 * Implementação de um mini-shell com:
 *  - prompt interativo
 *  - execução de comandos externos (execvp)
 *  - comandos internos: exit, pid, jobs, wait
 *  - execução em background com '&'
 *  - gerenciamento de jobs (lista), limpeza de processos terminados (waitpid WNOHANG)
 *
 * Compile:
 *   gcc -Wall mini_shell.c -o minishell
 *
 * Uso:
 *   ./minishell
 *
 * Observação: código comentado detalhadamente abaixo.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <errno.h>

#define MAX_CMD_LEN 256
#define MAX_ARGS 64
#define MAX_BG 100

typedef struct {
    pid_t pid;
    int job_id;     // número do job (1,2,...)
} bg_entry_t;

static bg_entry_t bg_processes[MAX_BG];
static int bg_count = 0;
static int next_job_id = 1;
static pid_t last_child_pid = 0;  // PID do último filho criado (foreground ou background)

/* --- Prototipos --- */
void parse_command(char *input, char **args, int *background);
void execute_command(char **args, int background);
int is_internal_command(char **args);
void handle_internal_command(char **args, int background);
void add_bg_process(pid_t pid);
int remove_bg_process_by_pid(pid_t pid); // retorna job_id ou -1 se não encontrado
void clean_finished_processes(void);
void print_jobs(void);
void wait_all_bg(void);

/* Ignorar SIGINT no shell para que Ctrl+C não mate o shell;
 * nos filhos definimos SIG_DFL para que Ctrl+C afete o processo em foreground.
 */
int main() {
    char input[MAX_CMD_LEN];
    char *args[MAX_ARGS];
    int background;

    /* Ignorar Ctrl+C para o processo shell em si */
    signal(SIGINT, SIG_IGN);

    printf("Mini-Shell iniciado (PID: %d)\n", getpid());
    printf("Digite 'exit' para sair\n\n");

    while (1) {
        /* Antes de exibir prompt, limpamos processos terminados (evita zumbis) */
        clean_finished_processes();

        printf("minishell> ");
        fflush(stdout);

        if (!fgets(input, sizeof(input), stdin)) {
            /* EOF (Ctrl+D) — encerra shell */
            printf("\n");
            break;
        }

        /* remover '\n' */
        input[strcspn(input, "\n")] = 0;

        /* ignorar linhas vazias */
        if (strlen(input) == 0) continue;

        /* parse */
        parse_command(input, args, &background);

        /* se não houve tokens (por exemplo só tinha '&' ou espaços) */
        if (args[0] == NULL) continue;

        if (is_internal_command(args)) {
            handle_internal_command(args, background);
        } else {
            execute_command(args, background);
        }
    }

    /* Antes de encerrar, aguardar processos background restantes */
    if (bg_count > 0) {
        printf("Aguardando processos em background antes de sair...\n");
        wait_all_bg();
    }

    printf("Shell encerrado!\n");
    return 0;
}

/* ===============================
 * parse_command:
 *  - divide a string de entrada em tokens (args)
 *  - detecta se o último token é '&' (background)
 *  - coloca args[n] = NULL (required por execvp)
 * =============================== */
void parse_command(char *input, char **args, int *background) {
    const char *delim = " \t";
    int argc = 0;
    *background = 0;

    /* strtok modifica a string input; isso é ok porque input é buffer local */
    char *token = strtok(input, delim);
    while (token != NULL && argc < (MAX_ARGS - 1)) {
        args[argc++] = token;
        token = strtok(NULL, delim);
    }

    if (argc == 0) {
        args[0] = NULL;
        return;
    }

    /* detectar '&' como último token (ex: "sleep 5 &") ou anexado (ex: "sleep 5&") */
    if (strcmp(args[argc - 1], "&") == 0) {
        *background = 1;
        args[argc - 1] = NULL;
        argc--;
    } else {
        size_t len = strlen(args[argc - 1]);
        if (len > 0 && args[argc - 1][len - 1] == '&') {
            *background = 1;
            /* remover o & do final do token, ex: "5&" -> "5" */
            if (len == 1) {
                args[argc - 1] = NULL;
                argc--;
            } else {
                args[argc - 1][len - 1] = '\0';
            }
        }
    }

    args[argc] = NULL;
}

/* ===============================
 * execute_command:
 *  - fork()
 *  - child: restaura sinal de Ctrl+C para default e chama execvp()
 *  - parent: se foreground -> waitpid() no pid; se background -> adiciona à lista
 * =============================== */
void execute_command(char **args, int background) {
    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        return;
    }

    if (pid == 0) {
        /* Child process */
        /* permitir que Ctrl+C afete o filho (padrão) */
        signal(SIGINT, SIG_DFL);

        /* execvp procura em PATH e substitui imagem do processo */
        if (execvp(args[0], args) == -1) {
            perror("execvp");
            exit(EXIT_FAILURE); /* se falhar no exec, sair do filho */
        }
    } else {
        /* Parent process */
        last_child_pid = pid;

        if (background) {
            add_bg_process(pid);
            /* mostrar [job] pid */
            printf("[%d] %d\n", bg_processes[bg_count - 1].job_id, pid);
        } else {
            int status;
            /* aguardar especificamente pelo filho em foreground */
            if (waitpid(pid, &status, 0) == -1) {
                perror("waitpid");
            } else {
                /* opcional: podemos mostrar status de saída se quisermos */
                // if (WIFEXITED(status)) printf("Exit status: %d\n", WEXITSTATUS(status));
            }
        }
    }
}

/* ===============================
 * is_internal_command: verifica se args[0] é comando interno
 * =============================== */
int is_internal_command(char **args) {
    if (args[0] == NULL) return 0;
    if (strcmp(args[0], "exit") == 0) return 1;
    if (strcmp(args[0], "pid") == 0) return 1;
    if (strcmp(args[0], "jobs") == 0) return 1;
    if (strcmp(args[0], "wait") == 0) return 1;
    return 0;
}

/* ===============================
 * handle_internal_command: implementa exit, pid, jobs, wait
 *  - exit: encerra o shell (mas aguarda bg processes antes)
 *  - pid: exibe getpid() do shell e last_child_pid
 *  - jobs: lista processos em background
 *  - wait: aguarda todos os processos em background
 * =============================== */
void handle_internal_command(char **args, int background) {
    if (strcmp(args[0], "exit") == 0) {
        /* exit — se houver processos em background, avisa e aguarda */
        if (bg_count > 0) {
            printf("Há %d processo(s) em background. Use 'wait' para aguardar ou 'exit' novamente para forçar.\n", bg_count);
            /* se o usuário digitou "exit &" ou "exit" em background, tratamos aqui como tentativa de sair;
             * por simplicidade não forçamos destruição dos filhos — pedimos ao usuário rodar 'wait' ou digitar exit de novo.
             */
            /* Para comportar o enunciado, vamos aguardar: */
            printf("Aguardando processos background...\n");
            wait_all_bg();
        }
        exit(0);
    } else if (strcmp(args[0], "pid") == 0) {
        printf("PID do shell: %d\n", getpid());
        if (last_child_pid != 0) printf("Último PID filho: %d\n", last_child_pid);
        else printf("Nenhum filho criado ainda\n");
    } else if (strcmp(args[0], "jobs") == 0) {
        print_jobs();
    } else if (strcmp(args[0], "wait") == 0) {
        if (bg_count == 0) {
            printf("Nenhum processo em background\n");
        } else {
            printf("Aguardando processos em background...\n");
            wait_all_bg();
            printf("Todos os processos terminaram\n");
        }
    }
}

/* ===============================
 * add_bg_process: adiciona pid na lista de bg, atribui job_id
 * =============================== */
void add_bg_process(pid_t pid) {
    if (bg_count < MAX_BG) {
        bg_processes[bg_count].pid = pid;
        bg_processes[bg_count].job_id = next_job_id++;
        bg_count++;
    } else {
        fprintf(stderr, "Limite de processos em background alcançado\n");
    }
}

/* ===============================
 * remove_bg_process_by_pid: remove da lista e retorna job_id.
 *  - se não encontrado, retorna -1
 * =============================== */
int remove_bg_process_by_pid(pid_t pid) {
    for (int i = 0; i < bg_count; i++) {
        if (bg_processes[i].pid == pid) {
            int job = bg_processes[i].job_id;
            /* deslocar para preencher a lacuna */
            for (int j = i; j < bg_count - 1; j++) {
                bg_processes[j] = bg_processes[j + 1];
            }
            bg_count--;
            return job;
        }
    }
    return -1;
}

/* ===============================
 * clean_finished_processes:
 *  - chama waitpid(-1, &status, WNOHANG) em loop para reap children terminados
 *  - remove da lista de background e imprime [job]+ Done
 *  - evita processos zumbis
 * =============================== */
void clean_finished_processes(void) {
    int status;
    pid_t pid;
    /* WNOHANG: não bloqueia se nenhum filho terminou */
    while ((pid = waitpid(-1, &status, WNOHANG)) > 0) {
        int job = remove_bg_process_by_pid(pid);
        if (job != -1) {
            printf("[%d]+ Done %d\n", job, pid);
        } else {
            /* era provavelmente um filho foreground já reaped no waitpid do pai; não fazer nada */
        }
    }
    /* Se pid == -1 e errno == ECHILD, não há filhos */
}

/* ===============================
 * print_jobs: lista os processos em background ativos
 *  - usa kill(pid,0) para checar se processo existe (errno == ESRCH -> não existe)
 * =============================== */
void print_jobs(void) {
    if (bg_count == 0) {
        printf("Nenhum processo em background\n");
        return;
    }
    printf("Processos em background:\n");
    for (int i = 0; i < bg_count; i++) {
        pid_t pid = bg_processes[i].pid;
        int job = bg_processes[i].job_id;
        /* checar existência */
        if (kill(pid, 0) == -1) {
            if (errno == ESRCH) {
                printf("[%d] %d Terminated\n", job, pid);
            } else {
                printf("[%d] %d (status desconhecido)\n", job, pid);
            }
        } else {
            printf("[%d] %d Running\n", job, pid);
        }
    }
}

/* ===============================
 * wait_all_bg: bloqueia até que todos os bg processes terminem.
 *  - imprime mensagens [job]+ Done
 * =============================== */
void wait_all_bg(void) {
    int status;
    pid_t pid;
    while ((pid = wait(&status)) > 0) {
        int job = remove_bg_process_by_pid(pid);
        if (job != -1) {
            printf("[%d]+ Done %d\n", job, pid);
        }
    }
    /* Se pid == -1, errno provavelmente ECHILD (não há mais filhos) */
}
