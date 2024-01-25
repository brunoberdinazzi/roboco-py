import tkinter as tk
from tkinter import filedialog
import platform
from robocopySecondgen.robopy.sistema_info import SistemaInfo
from robocopySecondgen.robopy.recursos_limitados import RecursosLimitados
from robocopySecondgen.robopy.log import Log
from robocopySecondgen.robopy.copia_arquivos import CopiaArquivos

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

