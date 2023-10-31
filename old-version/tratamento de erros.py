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

# Resto do código permanece o mesmo

class CopiaArquivos:
    def copiar_windows_para_windows(self, origem, destino, copiar_vazios, copiar_ocultos, log):
        comando = ["robocopy", origem, destino]

        if copiar_vazios:
            comando.append("/E")  # Copiar diretórios vazios

        if copiar_ocultos:
            comando.append("/AH")  # Copiar diretórios ocultos

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

if __name__ == "__main__":
    main()
