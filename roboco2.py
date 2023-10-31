## Nova versão em desenvolvimento que tratará os erros devidamente.

import subprocess
import tkinter as tk
from tkinter import filedialog
import os
import platform
import signal
import logging
from threading import Thread

logging.basicConfig(filename='log_copia_arquivos.log', level=logging.INFO, format='%(asctime)s - %(message)s')

copia_em_progresso = False

def selecionar_diretorio(label):
    diretorio = filedialog.askdirectory()
    label.delete(0, tk.END)
    label.insert(0, diretorio)

def copiar_windows_para_windows(origem, destino, copiar_vazios, copiar_ocultos):
    global copia_em_progresso
    copia_em_progresso = True

    def handler(sig, frame):
        nonlocal copia_em_progresso
        copia_em_progresso = False

    signal.signal(signal.SIGINT, handler)

    comando = ["robocopy", origem, destino]

    if copiar_vazios:
        comando.append("/E") 

    if copiar_ocultos:
        comando.append("/AH")  

    try:
        subprocess.run(comando, check=True)
        resultado.config(text="Cópia bem-sucedida.")
        logging.info(f'Cópia bem-sucedida: {origem} para {destino}')
    except subprocess.CalledProcessError as e:
        if copia_em_progresso:
            resultado.config(text=f"Erro ao copiar: {e}")
            logging.error(f'Erro ao copiar: {origem} para {destino}. Motivo: {e}')
        else:
            resultado.config(text="Cópia interrompida pelo usuário.")
            logging.warning(f'Cópia interrompida pelo usuário: {origem} para {destino}')

def iniciar_copia():
    origem = entrada_origem.get()
    destino = entrada_destino.get()

    if not origem or not destino:
        resultado.config(text="Por favor, selecione origem e destino.")
        return

    copiar_vazios = copiar_diretorios_vazios.get()
    copiar_ocultos = copiar_diretorios_ocultos.get()

    sistema_operacional = platform.system()

    if sistema_operacional == "Windows":
        direcao_copia = "windows_para_windows"  
    elif sistema_operacional == "Linux":
        direcao_copia = "linux_para_linux" 
    else:
        resultado.config(text="Sistema operacional não suportado.")
        return

    if direcao_copia == "windows_para_windows":
        copiar_windows_para_windows(origem, destino, copiar_vazios, copiar_ocultos)

def parar_copia():
    global copia_em_progresso
    copia_em_progresso = False
    resultado.config(text="Cópia interrompida pelo usuário.")
    logging.warning("Cópia interrompida pelo usuário.")

janela = tk.Tk()
janela.title("Cópia de Arquivos")

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

copiar_button = tk.Button(janela, text="Iniciar Cópia", command=iniciar_copia)
parar_button = tk.Button(janela, text="Parar Cópia", command=parar_copia)
resultado = tk.Label(janela, text="")

origem_label.grid(row=0, column=0)
entrada_origem.grid(row=0, column=1)
selecionar_origem_button.grid(row=0, column=2)

destino_label.grid(row=1, column=0)
entrada_destino.grid(row=1, column=1)
selecionar_destino_button.grid(row=1, column=2)

copiar_diretorios_vazios_checkbox.grid(row=2, column=0, columnspan=3)
copiar_diretorios_ocultos_checkbox.grid(row=3, column=0, columnspan=3)

copiar_button.grid(row=4, column=0, columnspan=3)
parar_button.grid(row=5, column=0, columnspan=3)
resultado.grid(row=6, column=0, columnspan=3)

janela.mainloop()
