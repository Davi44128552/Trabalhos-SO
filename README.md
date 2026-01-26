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
- _First Come, First Served (FCFS)_: Algoritmo que funciona como uma FILA, em que os primeiros procesoss a chegarem serão os primeiros a sair;
- _Shortest Job First (SJF)_: Na medida que os processos vão entrando, o sistema dá prioridade àqueles que tem o menor tempo total de execução;
- _Shortest Remaining Time First (SRTF)_: Uma versão preemptiva de SJF, o algoritmo SRTF dá prioridade aos processos que tem o menor tempo de execução restante;
- _PRIOc_: Este algoritmo dá prioridade às tarefas que tem maior prioridade para serem executados, e, que os próximos serão escolhidos quando o que está rodando finaliza;
- _PRIOp_: Este algoritmo segue a ideia de PRIOc, mas dessa vez com preempção: Quando aparece um processo com prioridade maior, interrompemos a execução da tarefa atual e damos prioridade a que entrou;
- _Round-Robin cooperativo (RRc)_: A proposta do round-robin é dar um tempo de execução para cada tarefa. Quando esse tempo chega, o processo é pausado e é dado os recursos para outro que tá na fila;
- _Round-Robin preemptivo (RRp)_: Semelhante ao RRc, mas com uma pequena ideia diferente: Quando aparece um novo processo com maior prioridade, ele "fura" a fila e é executado com prioridade.

Para executar o trabalho, é necessário ter a biblioteca _matplotlib_ instalada na máquina, que pode ser instalada com pip, através do comando `pip install matplotlib`. Para executar o trabalho, é necessário rodar o código _guiSimulator.py_, por meio do comando `python guiSimulator.py`.

Após executar, basta definir os parâmetros desejados, criar os processos a serem executados, escolher o algoritmo desejado e apertar no botão _Executar Simulação_.

### Algoritmos de alocação de memória
Neste trabalho, são implementados em python os principais algoritmos de alocação de memória que, como seu nome sugere, são usados para alocar processos na memória.

Os algoritmos implementados foram os seguintes:
- _First-fit_: O processo é alocado no primeiro bloco de memória disponível em que cabe o processo por vir;
- _Best-fit_: O processo é alocado no menor bloco de memória disponível em que o processo cabe;
- _Worst-fit_: O processo é alocado no maior bloco de memória disponível em que o processo cabe.

Para executar o trabalho, basta rodar o arquivo `Main.py`, através do comando `python Main.py`.

Após executar, é mostrado um tutorial ao usuário ensinando o que ele pode fazer. O usuário pode realizar os seguintes comandos:

- `init <n>` - Inicia a memória com n bytes;
- `alloc <n> <alg>` - Aloca um bloco de n bytes na memória por meio do algoritmo _alg_;
- `freeid <id>` - Liberar o bloco com id especificado;
- `show` e `showp` - Mostra o mapa de memória e os blocos existentes;
- `help` - Mostra os comandos;
- `exit` - Encerra o programa.

### Algoritmos de Paginação

Esta implementação consiste nos algoritmos de paginação em disco, que tem como princípio a mudança de páginas ociosas da memória RAM para o disco, além de trazer outras páginas de volta do disco para a memória.

Os algoritmos implementados no trabalho podem ser vistos na lista abaixo:
- _First-In, First-Out (FIFO)_: Segue a estrutura da FILA, removendo o processo mais antigo que foi adicionado à memória;
- _Ótimo_: Retira a página que ficará mais tempo sem ser acessada;
- _Least Recently Used (LRU)_: Retira as páginas que estão há mais tempo sem serem acessadas;
- _Not Recently Used (NRU)_: Utiliza flags de referência e modificação em que definem o nível de importância de cada página;
- _Least Frequently Used (LFU)_: Remove as páginas que são acessadas com menos frequência;
- _Most Frequently Used (MFU)_: A execução é parecida com _LFU_, mas sua estratégia consiste em remover a página com maior frequência de uso;
- _Algoritmo do relógio (ou da 2ª chance)_: Se baseia no algoritmo _FIFO_, mas analisa o bit de referência de cada página candidata, dando uma "segunda chance" às usadas recentemente;

O algoritmo é rodado diretamente quando chamado pelo terminal, em que o código lê as "páginas" contidas em _silberschatz2001.trace_ para a execução de um algoritmo decidido pelo usuário. A execução do scrip se dá por meio do comando abaixo:
`./pager --algo _ALGORITMO_ --frames _FRAMES_ --trace _TRACE_`
ou
`python pager --algo _ALGORITMO_ --frames _FRAMES_ --trace _TRACE_`

em que:
- _ALGORITMO_: O algoritmo de paginação que se deseja testar;
- _FRAMES_: A quantidade de quadros que a memória tem para suportar os processos;
- _TRACE_: O arquivo _.trace_ que se deseja rodar o algoritmo.

### Fundamentação Teórica 

A implementação dos códigos da disciplina foram desenvolvidas com base em conceitos de Sistemas Operacionais na literatura da área. A base teórica utilizada na compreensão dos conceitos e mecanismos de Sistemas Operacionais empregados no código tem como principais referências as seguintes:
- MAZIERO, Carlos A. _Sistemas Operacionais: Conceitos e Mecanismos_
- TANENBAUM, Andres S.; BOS, Herbert. _Sistemas Operacionais Modernos._