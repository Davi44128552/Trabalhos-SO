# Trabalhos-SO :penguin:

### Integrantes
- Davi Iury Lopes Souza - 554054
- Livian Jhennifer Nascimento Lima - 554850
- Maria Ianne Braz Castro - 554396
- Maria Luiza Felipe Carolino - 552655
- Naila Ketley de Freitas Bruno - 555248

### Introdução
Este repositório é dedicado à implementação dos trabalhos práticos da disciplina de Sistemas Operacionais (CK0234) do Departamento de Computação (DC), pela Universidade Federal do Ceará (UFC).

A disciplina teve em sua totalidade 4 trabalhos práticos de implementação, com o intuito de aprofundar os conhecimentos nos conteúdos da cadeira.

Abaixo, podemos ver quais foram os trabalhos:

- Minishell
- Algoritmos de escalonamento de processos
- Algoritmos de alocação de memória
- Algoritmos de Paginação 

### Minishell
Neste trabalho, foi impelementado um minishell na linguagem C, com o propósito de enteder mais como funcionam os terminais de Sistemas Operacionais como windows e linux, com foco na compreensão do processo de criação de gerenciamento de processos do sistema.

Para usar do minishell, precisamos compilar o arquivo mini_shell.c, usando o comando `gcc mini_shell.c -o executavel`

Após compilar, executamos com o comando `.\executavel`

O minishell possui os seguintes comandos:
- `exit`: Encerra o minishell
- `pid`: Mostra o PID do minishell do último processo em foreground
- `jobs`: Lista os processos em background ativos
- `wait`: Bloqueia o minishell até que todos os processos ativos em background se encerrem
- Comandos externos do sistema em que a aplicação está rodando, através do comando `execvp`, presente internamente no código
- Comandos em background, por meio da adição de _&_ no comando

### Algoritmos de escalonamento de processos
No segundo trabalho, são implementados em python os algoritmos de escalonamento de tarefas que são responsáveis por controlar a execução de processos no sistema operacional, juntamente a uma interface gráfica que ajuda a entender como cada algoritmo executa.

Os algoritmos implementados podem ser vistos na lista abaixo:
- First Come, First Served (FCFS): Algoritmo que funciona como uma FILA, em que os primeiros procesoss a chegarem serão os primeiros a sair.
- Shortest Job First (SJF): Na medida que os processos vão entrando, o sistema dá prioridade àqueles que tem o menor tempo total de execução.
- Shortest Remaining Time First (SRTF): Uma versão preemptiva de SJF, o algoritmo SRTF dá prioridade aos processos que tem o menor tempo de execução restante.
- PRIOc: Este algoritmo dá prioridade às tarefas que tem maior prioridade para serem executados, e, que os próximos serão escolhidos quando o que está rodando finaliza
- PRIOp: Este algoritmo segue a ideia de PRIOc, mas dessa vez com preempção: Quando aparece um processo com prioridade maior, interrompemos a execução da tarefa atual e damos prioridade a que entrou.
- Round-Robin cooperativo (RRc): A proposta do round-robin é dar um tempo de execução para cada tarefa. Quando esse tempo chega, o processo é pausado e é dado os recursos para outro que tá na fila.
- Round-Robin preemptivo (RRp): Semelhante ao RRc, mas com uma pequena ideia diferente: Quando aparece um novo processo com maior prioridade, ele "fura" a fila e é executado com prioridade.

Para executar o trabalho, é necessário ter a biblioteca _matplotlib_ instalada na máquina, que pode ser instalada com pip, através do comando `pip install matplotlib`. Para executar o trabalho, é necessário rodar o código _guiSimulator.py_, por meio do comando `python guiSimulator.py`.

Após executar, basta definir os parâmetros desejados, criar os processos a serem executados, escolher o algoritmo desejado e apertar no botão _Executar Simulação_.

### Algoritmos de alocação de memória
Neste trabalho, são implementados em python os principais algoritmos de alocação de memória que, como seu nome sugere, são usados para alocar processos na memória.

Os algoritmos implementados foram os seguintes:
- First-fit: O processo é alocado no primeiro bloco de memória disponível em que cabe o processo por vir;
- Best-fit: O processo é alocado no menor bloco de memória disponível em que o processo cabe;
- Worst-fit: O processo é alocado no maior bloco de memória disponível em que o processo cabe.

Para executar o trabalho, basta rodar o arquivo `Main.py`, através do comando `python Main.py`.

Após executar, é mostrado um tutorial ao usuário ensinando o que ele pode fazer. O usuário pode realizar os seguintes comandos:

- `init <n>` - Inicia a memória com n bytes
- `alloc <n> <alg>` - Aloca um bloco de n bytes na memória por meio do algoritmo _alg_
- `freeid <id>` - Liberar o bloco com id especificado
- `show` e `showp` - Mostra o mapa de memória e os blocos existentes
- `help` - Mostra os comandos
- `exit` - Encerra o programa

### Algoritmos de Paginação