import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from scheduling_algorithms import Processo, FCFS, SJF, SRTF, PrioC, RRSemPrioridade, PrioP, RRPrioEvelhecimento, calcular_metricas
import copy
import json
import os

class CollapsibleFrame(ttk.Frame):
    def __init__(self, parent, text="", *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        
        self.show = tk.BooleanVar()
        self.show.set(True)
        
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)
        
        ttk.Label(self.title_frame, text=text, font=('TkDefaultFont', 10, 'bold')).pack(side="left", fill="x", expand=1, padx=5)
        
        self.toggle_button = ttk.Button(
            self.title_frame,
            text="▼",
            width=3,
            command=self.toggle
        )
        self.toggle_button.pack(side="right")
        
        self.content_frame = ttk.Frame(self)
        
    def toggle(self):
        if self.show.get():
            self.content_frame.pack_forget()
            self.toggle_button.configure(text="►")
            self.show.set(False)
        else:
            self.content_frame.pack(fill="both", expand=1)
            self.toggle_button.configure(text="▼")
            self.show.set(True)

class ProcessSchedulingSimulatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Simulador de Escalonamento de Processos")

        self.processes = [] # Lista de dicionários para a GUI
        self.original_processes_for_simulation = [] # Lista de objetos Processo para simulação

        # Configurações de quantum e aging
        # Carregar configurações do config.json
        config_path = "config.json"

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    default_quantum = config.get('quantum', 2)
                    default_aging = config.get('aging', 1)
            except:
                pass

        self.quantum = tk.IntVar(value=default_quantum)
        self.aging = tk.IntVar(value=default_aging)
        
        # Frame para entrada de processos (colapsável)
        self.process_input_frame = CollapsibleFrame(master, text="Adicionar Processo")
        self.process_input_frame.pack(padx=10, pady=10, fill="x")
        self.process_input_frame.content_frame.pack(fill="x", expand=True)

        # Campos de entrada para o processo
        ttk.Label(self.process_input_frame.content_frame, text="Instante de Criação:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.arrival_time_entry = ttk.Entry(self.process_input_frame.content_frame)
        self.arrival_time_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.process_input_frame.content_frame, text="Duração (segundos):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.duration_entry = ttk.Entry(self.process_input_frame.content_frame)
        self.duration_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.process_input_frame.content_frame, text="Prioridade Estática:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.priority_entry = ttk.Entry(self.process_input_frame.content_frame)
        self.priority_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.add_process_button = ttk.Button(self.process_input_frame.content_frame, text="Adicionar Processo", command=self.add_process)
        self.add_process_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Frame para remover processos
        self.process_remove_frame = ttk.LabelFrame(master, text="Remover Processo")
        self.process_remove_frame.pack(padx=10, pady=10, fill="x")

        self.remove_process_button = ttk.Button(self.process_remove_frame, text="Remover Processo Selecionado", command=self.remove_process)
        self.remove_process_button.pack(padx=5, pady=5)

        # Frame para configurações de quantum e aging
        self.config_frame = ttk.LabelFrame(master, text="Configurações")
        self.config_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(self.config_frame, text="Quantum:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self.config_frame, textvariable=self.quantum).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.config_frame, text="Aging:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self.config_frame, textvariable=self.aging).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.save_config_button = ttk.Button(self.config_frame, text="Salvar Configurações", command=self.save_config)
        self.save_config_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Frame para exibir processos adicionados (colapsável)
        self.process_list_frame = CollapsibleFrame(master, text="Processos Adicionados")
        self.process_list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.process_list_frame.content_frame.pack(fill="both", expand=True)

        self.process_tree = ttk.Treeview(self.process_list_frame.content_frame, columns=("PID", "Criação", "Duração", "Prioridade"), show="headings")
        self.process_tree.heading("PID", text="PID")
        self.process_tree.heading("Criação", text="Criação")
        self.process_tree.heading("Duração", text="Duração")
        self.process_tree.heading("Prioridade", text="Prioridade")
        self.process_tree.pack(fill="both", expand=True)

        # Frame para seleção de algoritmo e execução
        self.control_frame = ttk.LabelFrame(master, text="Controles")
        self.control_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(self.control_frame, text="Algoritmo de Escalonamento:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.algorithm_selection = ttk.Combobox(self.control_frame,
                                                values=["FCFS", "SJF", "SRTF", "Prioridade (Não Preemptivo)", "Round Robin (Sem Prioridade)", "Prioridade (Preemptivo)", "Round Robin (Com Prioridade e Envelhecimento)"])
        self.algorithm_selection.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.algorithm_selection.set("FCFS") # Default value

        self.run_simulation_button = ttk.Button(self.control_frame, text="Executar Simulação", command=self.run_simulation)
        self.run_simulation_button.grid(row=0, column=2, padx=5, pady=5)

        # Frame para exibir métricas de desempenho (colapsável)
        self.metrics_frame = CollapsibleFrame(master, text="Métricas de Desempenho")
        self.metrics_frame.pack(padx=10, pady=10, fill="x")
        self.metrics_frame.content_frame.pack(fill="x", expand=True)

        # Frame para o Diagrama de Gantt
        self.gantt_frame = ttk.LabelFrame(master, text="Diagrama de Gantt")
        self.gantt_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.gantt_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.ax.set_xlabel("Tempo")
        self.ax.set_ylabel("Processo")
        self.ax.set_yticks([])
        self.ax.set_title("Diagrama de Gantt da Execução")
        self.fig.tight_layout()

        self.metrics_tree = ttk.Treeview(self.metrics_frame.content_frame, columns=("Métrica", "Valor"), show="headings")
        self.metrics_tree.heading("Métrica", text="Métrica")
        self.metrics_tree.heading("Valor", text="Valor")
        self.metrics_tree.pack(fill="both", expand=True)

    def add_process(self):
        try:
            arrival = int(self.arrival_time_entry.get())
            duration = int(self.duration_entry.get())
            priority = int(self.priority_entry.get())

            if arrival < 0 or duration <= 0 or priority <= 0:
                messagebox.showerror("Erro de Entrada", "Todos os valores devem ser positivos. Duração e Prioridade devem ser maiores que zero.")
                return

            pid = len(self.processes) + 1
            self.processes.append({"pid": pid, "arrival": arrival, "duration": duration, "priority": priority})
            self.process_tree.insert("", "end", values=(pid, arrival, duration, priority))

            # Limpar campos
            self.arrival_time_entry.delete(0, tk.END)
            self.duration_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, insira valores inteiros válidos para todos os campos.")

    def remove_process(self):
        # Pega o item selecionado na árvore
        selected_item = self.process_tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione um processo para remover.")
            return
        
        # Pega os valores do item selecionado
        item_values = self.process_tree.item(selected_item[0], 'values')
        pid_to_remove = int(item_values[0])
        
        # Remove da lista de processos
        self.processes = [p for p in self.processes if p["pid"] != pid_to_remove]
        
        # Remove da visualização da árvore
        self.process_tree.delete(selected_item[0])
        
        # Reajusta os PIDs para serem sequenciais novamente
        for i, process in enumerate(self.processes):
            old_pid = process["pid"]
            new_pid = i + 1
            process["pid"] = new_pid
            
            # Atualiza na árvore também
            for item in self.process_tree.get_children():
                values = self.process_tree.item(item, 'values')
                if int(values[0]) == old_pid:
                    self.process_tree.item(item, values=(new_pid, values[1], values[2], values[3]))
                    break

    def save_config(self):
        try:
            quantum_val = self.quantum.get()
            aging_val = self.aging.get()

            if quantum_val <= 0 or aging_val <= 0:
                messagebox.showerror("Erro de Configuração", "Quantum e Aging devem ser valores positivos.")
                return

            config = {
                "quantum": quantum_val,
                "aging": aging_val
            }

            with open("config.json", 'w') as f:
                json.dump(config, f, indent=4)

            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")

        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, insira valores inteiros válidos para Quantum e Aging.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar as configurações: {e}")

    def run_simulation(self):
        if not self.processes:
            messagebox.showwarning("Nenhum Processo", "Por favor, adicione processos antes de executar a simulação.")
            return
        
        # Limpar métricas e gráfico antes de cada simulação
        self.metrics_tree.delete(*self.metrics_tree.get_children())
        self.draw_gantt_chart([]) # Limpa o gráfico estático, a animação vai desenhar do zero

        # Criar objetos Processo para a simulação
        self.original_processes_for_simulation = []
        for p_data in self.processes:
            self.original_processes_for_simulation.append(Processo(p_data["pid"], p_data["priority"], p_data["duration"], p_data["arrival"]))

        selected_algorithm = self.algorithm_selection.get()
        execution_order = []
        num_context_switches = 0
        animation_steps = []

        try:
            if selected_algorithm == "FCFS":
                execution_order, num_context_switches, animation_steps = FCFS(self.original_processes_for_simulation)
            elif selected_algorithm == "SJF":
                execution_order, num_context_switches, animation_steps = SJF(self.original_processes_for_simulation)
            elif selected_algorithm == "SRTF":
                execution_order, num_context_switches, animation_steps = SRTF(self.original_processes_for_simulation)
            elif selected_algorithm == "Prioridade (Não Preemptivo)":
                execution_order, num_context_switches, animation_steps = PrioC(self.original_processes_for_simulation)
            elif selected_algorithm == "Round Robin (Sem Prioridade)":
                quantum_val = self.quantum.get()
                if quantum_val <= 0:
                    messagebox.showerror("Erro de Configuração", "Quantum deve ser um valor positivo.")
                    return
                execution_order, num_context_switches, animation_steps = RRSemPrioridade(self.original_processes_for_simulation, self.quantum.get())
            elif selected_algorithm == "Prioridade (Preemptivo)":
                execution_order, num_context_switches, animation_steps = PrioP(self.original_processes_for_simulation)
            elif selected_algorithm == "Round Robin (Com Prioridade e Envelhecimento)":
                quantum_val = self.quantum.get()
                aging_val = self.aging.get()
                if quantum_val <= 0 or aging_val <= 0:
                    messagebox.showerror("Erro de Configuração", "Quantum e Aging devem ser valores positivos.")
                    return
                execution_order, num_context_switches, animation_steps = RRPrioEvelhecimento(self.original_processes_for_simulation, self.quantum.get(), self.aging.get())
            else:
                messagebox.showerror("Erro", "Algoritmo não reconhecido.")
                return

            # Calcular e exibir métricas
            metrics = calcular_metricas(self.original_processes_for_simulation, execution_order, num_context_switches)
            self.metrics_tree.insert("", "end", values=("Tempo Médio de Vida (TT)", f"{metrics['tempo_medio_vida']:.2f}"))
            self.metrics_tree.insert("", "end", values=("Tempo Médio de Espera (TW)", f"{metrics['tempo_medio_espera']:.2f}"))
            self.metrics_tree.insert("", "end", values=("Trocas de Contexto", metrics['trocas_contexto']))

            # Iniciar animação do diagrama de Gantt
            self.animate_gantt_chart(animation_steps)

        except Exception as e:
            messagebox.showerror("Erro na Simulação", f"Ocorreu um erro durante a simulação: {e}")

    def animate_gantt_chart(self, animation_steps):
        self.ax.clear()
        self.ax.set_xlabel("Tempo")
        self.ax.set_ylabel("Processo")
        self.ax.set_title("Diagrama de Gantt da Execução")

        unique_pids = sorted(list(set([pid for _, pid in animation_steps if pid != 0])))
        if not unique_pids:
            self.canvas.draw_idle()
            return

        colors = plt.cm.get_cmap("tab10", len(unique_pids))
        pid_to_color = {pid: colors(i) for i, pid in enumerate(unique_pids)}

        y_labels = [f"P{pid}" for pid in unique_pids]
        self.ax.set_yticks(range(len(y_labels)))
        self.ax.set_yticklabels(y_labels)
        self.ax.invert_yaxis()

        self.current_animation_step = 0
        self.animation_steps = animation_steps
        self.pid_to_color = pid_to_color
        self.unique_pids = unique_pids

        self.update_animation()

    def update_animation(self):
        if self.current_animation_step < len(self.animation_steps):
            time, pid = self.animation_steps[self.current_animation_step]

            if pid != 0:
                y_pos = self.unique_pids.index(pid)
                self.ax.barh(y_pos, 1, left=time, color=self.pid_to_color[pid], edgecolor="black", height=0.5)

            self.ax.set_xlim(0, time + 1)
            self.canvas.draw_idle()

            self.current_animation_step += 1
            self.master.after(200, self.update_animation) # 200ms de delay

    def draw_gantt_chart(self, execution_order):
        # Esta função não é mais usada para desenhar o gráfico final, mas a mantemos para não quebrar a chamada inicial
        # A animação é tratada por animate_gantt_chart
        self.ax.clear()
        self.canvas.draw_idle()

def close_janela():
    root.destroy()
    root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessSchedulingSimulatorGUI(root)
    root.protocol("WM_DELETE_WINDOW", close_janela)
    root.mainloop()



