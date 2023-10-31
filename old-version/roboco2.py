## Nova versão em desenvolvimento que tratará os erros devidamente.

import subprocess
import tkinter as tk
from tkinter import filedialog
import os
import platform
import psutil
import datetime

class SistemaInfo:
    def obter_informacoes_sistema(self):
        mem = psutil.virtual_memory()
        print(f"Memória Total: {mem.total} bytes")
        print(f"Memória Disponível: {mem.available} bytes")
        print(f"Porcentagem de Memória Usada: {mem.percent}%")

        num_nucleos = psutil.cpu_count(logical=False)
        num_threads = psutil.cpu_count(logical=True)
        print(f"Número de Núcleos Físicos: {num_nucleos}")
        print(f"Número de Núcleos Lógicos: {num_threads}")

class RecursosLimitados:
    def limitar_recursos(self, memoria_limite, cpu_cores):
        if os.name == 'posix':
            try:
                psutil.Process(os.getpid()).cpu_affinity(cpu_cores)
            except Exception as e:
                print(f"Erro ao limitar o uso de CPU: {e}")

            try:
                limite_em_bytes = 1024 * 1024 * memoria_limite
                os.setrlimit(os.RLIMIT_AS, (limite_em_bytes, limite_em_bytes))
            except Exception as e:
                print(f"Erro ao limitar o uso de memória: {e}")
        elif os.name == 'nt':
            print("Limitações de recursos não suportadas no Windows.")

class Log:
    def __init__(self):
        self.log_file = "copia_log.txt"

    def registrar_mensagem(self, mensagem):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as file:
            file.write(f"[{timestamp}] {mensagem}\n")

    def limpar_log(self):
        open(self.log_file, "w").close()  # Limpa o arquivo de log

def selecionar_diretorio(label):
    diretorio = filedialog.askdirectory()
    label.delete(0, tk.END)
    label.insert(0, diretorio)

def iniciar_copia():
    origem = entrada_origem.get()
    destino = entrada_destino.get()

    if not origem or not destino:
        resultado.config(text="Por favor, selecione origem e destino.")
        return

    copiar_vazios = copiar_diretorios_vazios.get()
    copiar_ocultos = copiar_diretorios_ocultos.get()
    
    memoria_limite = int(entrada_memoria.get())  # Obtém a quantidade de memória da entrada
    cpu_cores = [int(core) for core in entrada_cores.get().split(",")]  # Obtém os núcleos da CPU da entrada

    sistema_operacional = platform.system()
    recursos_limitados = RecursosLimitados()
    log = Log()

    if sistema_operacional == "Windows":
        direcao_copia = "windows_para_windows"
    elif sistema_operacional == "Linux":
        direcao_copia = "linux_para_linux"
    else:
        resultado.config(text="Sistema operacional não suportado.")
        return

    copia_arquivos = CopiaArquivos()

    recursos_limitados.limitar_recursos(memoria_limite, cpu_cores)  # Limita recursos
    log.limpar_log()  # Limpa o arquivo de log antes da cópia

    try:
        if direcao_copia == "windows_para_windows":
            copia_arquivos.copiar_windows_para_windows(origem, destino, copiar_vazios, copiar_ocultos, log)
        elif direcao_copia == "linux_para_linux":
            copia_arquivos.copiar_linux_para_linux(origem, destino, copiar_vazios, copiar_ocultos, log)
        elif direcao_copia == "windows_para_linux":
            copia_arquivos.copiar_windows_para_linux(origem, destino, copiar_vazios, copiar_ocultos, log)
        elif direcao_copia == "linux_para_windows":
            copia_arquivos.copiar_linux_para_windows(origem, destino, copiar_vazios, copiar_ocultos, log)
        resultado.config(text="Cópia bem-sucedida.")
    except Exception as e:
        resultado.config(text=f"Erro ao copiar: {e}")

class CopiaArquivos:
    def copiar_windows_para_windows(self, origem, destino, copiar_vazios, copiar_ocultos, log):
        comando = ["robocopy", origem, destino]

        if copiar_vazios:
            comando.append("/E")  # Copiar diretórios vazios

        if copiar_ocultos:
            comando.append("/A+H")  # Copiar diretórios ocultos

        try:
            subprocess.run(comando, check=True)
        except subprocess.CalledProcessError as e:
            log.registrar_mensagem(f"Erro ao copiar: {e}")

    def copiar_linux_para_linux(self, origem, destino, copiar_vazios, copiar_ocultos, log):
        comando = ["rsync", "-av", origem, destino]

        if copiar_ocultos:
            comando.append("--exclude=.*")

        try:
            subprocess.run(comando, check=True)
        except subprocess.CalledProcessError as e:
            log.registrar_mensagem(f"Erro ao copiar: {e}")

    def copiar_windows_para_linux(self, origem, destino, copiar_vazios, copiar_ocultos, log):
        comando = ["scp", "-r", origem, f"{destino}/"]

        try:
            subprocess.run(comando, check=True)
        except subprocess.CalledProcessError as e:
            log.registrar_mensagem(f"Erro ao copiar: {e}")

    def copiar_linux_para_windows(self, origem, destino, copiar_vazios, copiar_ocultos, log):
        comando = ["smbclient", f"//{destino}", "-c", f"lcd {origem}; prompt; recurse; mget *"]

        try:
            subprocess.run(comando, check=True)
        except subprocess.CalledProcessError as e:
            log.registrar_mensagem(f"Erro ao copiar: {e}")

# Cria a janela principal
janela = tk.Tk()
janela.title("Roboco.py")

# Cria elementos da interface
origem_label = tk.Label(janela, text="Origem:")
entrada_origem = tk.Entry(janela)
selecionar_origem_button = tk.Button(janela, text="Selecionar", command=lambda: selecionar_diretorio(entrada_origem))

destino_label = tk.Label(janela, text="Destino:")
entrada_destino = tk.Entry(janela)
selecionar_destino_button = tk.Button(janela, text="Selecionar", command=lambda: selecionar_diretorio(entrada_destino))

copiar_diretorios_vazios = tk.BooleanVar()
copiar_diretorios_vazios_checkbox = tk.Checkbutton(janela, text="Copiar diretórios vazios", variable=copiar_diretorios_vazios)

copiar_diretorios_ocultos = tk.BooleanVar()
copiar_diretorios_ocultos_checkbox = tk.Checkbutton(janela, text="Copiar diretórios ocultos", variable=copiar_diretorios_ocultos)

memoria_label = tk.Label(janela, text="Limite de Memória (MB):")
entrada_memoria = tk.Entry(janela)

cores_label = tk.Label(janela, text="Cores da CPU (separados por vírgula):")
entrada_cores = tk.Entry(janela)

copiar_button = tk.Button(janela, text="Iniciar Cópia", command=iniciar_copia)
resultado = tk.Label(janela, text="")

origem_label.grid(row=0, column=0)
entrada_origem.grid(row=0, column=1)
selecionar_origem_button.grid(row=0, column=2)

destino_label.grid(row=1, column=0)
entrada_destino.grid(row=1, column=1)
selecionar_destino_button.grid(row=1, column=2)

copiar_diretorios_vazios_checkbox.grid(row=2, column=0, columnspan=3)
copiar_diretorios_ocultos_checkbox.grid(row=3, column=0, columnspan=3)

memoria_label.grid(row=4, column=0)
entrada_memoria.grid(row=4, column=1)

cores_label.grid(row=5, column=0)
entrada_cores.grid(row=5, column=1)

copiar_button.grid(row=6, column=0, columnspan=3)
resultado.grid(row=7, column=0, columnspan=3)

janela.mainloop()
