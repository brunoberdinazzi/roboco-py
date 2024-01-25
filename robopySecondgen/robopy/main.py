import subprocess
import tkinter as tk
from tkinter import filedialog
import os
import platform
import psutil
import datetime
from robocopySecondgen.robopy.sistema_info import SistemaInfo
from robocopySecondgen.robopy.recursos_limitados import RecursosLimitados
from robocopySecondgen.robopy.log import Log
from robocopySecondgen.robopy.copia_arquivos import CopiaArquivos

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