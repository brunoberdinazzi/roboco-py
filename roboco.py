## Versão Inicial

import subprocess
import tkinter as tk
from tkinter import filedialog
import os
import platform
from threading import Thread

def selecionar_diretorio(label):
    diretorio = filedialog.askdirectory()
    label.delete(0, tk.END)
    label.insert(0, diretorio)

def copiar_windows_para_windows(origem, destino, copiar_vazios, copiar_ocultos):
    comando = ["robocopy", origem, destino]

    if copiar_vazios:
        comando.append("/E")  # Copiar diretórios vazios

    if copiar_ocultos:
        comando.append("/AH")  # Copiar diretórios ocultos

    try:
        subprocess.run(comando, check=True)
        resultado.config(text="Cópia bem-sucedida.")
    except subprocess.CalledProcessError as e:
        resultado.config(text=f"Erro ao copiar: {e}")

def copiar_linux_para_linux(origem, destino, copiar_vazios, copiar_ocultos):
    comando = ["rsync", "-av", origem, destino]

    if copiar_ocultos:
        comando.append("--exclude=.*")  

    try:
        subprocess.run(comando, check=True)
        resultado.config(text="Cópia bem-sucedida de Linux para Linux.")
    except subprocess.CalledProcessError as e:
        resultado.config(text=f"Erro ao copiar: {e}")

def copiar_windows_para_linux(origem, destino, copiar_vazios, copiar_ocultos):
    comando = ["scp", "-r", origem, f"{destino}/"]

    try:
        subprocess.run(comando, check=True)
        resultado.config(text="Cópia bem-sucedida de Windows para Linux.")
    except subprocess.CalledProcessError as e:
        resultado.config(text=f"Erro ao copiar: {e}")

def copiar_linux_para_windows(origem, destino, copiar_vazios, copiar_ocultos):

    comando = ["smbclient", f"//{destino}", "-c", f"lcd {origem}; prompt; recurse; mget *"]

    try:
        subprocess.run(comando, check=True)
        resultado.config(text="Cópia bem-sucedida de Linux para Windows.")
    except subprocess.CalledProcessError as e:
        resultado.config(text=f"Erro ao copiar: {e}")

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
        direcao_copia = "windows_para_windows"  # Defina a direção padrão para Windows
    elif sistema_operacional == "Linux":
        direcao_copia = "linux_para_linux"  # Defina a direção padrão para Linux
    else:
        resultado.config(text="Sistema operacional não suportado.")
        return

    if direcao_copia == "windows_para_windows":
        copiar_windows_para_windows(origem, destino, copiar_vazios, copiar_ocultos)
    elif direcao_copia == "linux_para_linux":
        copiar_linux_para_linux(origem, destino, copiar_vazios, copiar_ocultos)
    elif direcao_copia == "windows_para_linux":
        copiar_windows_para_linux(origem, destino, copiar_vazios, copiar_ocultos)
    elif direcao_copia == "linux_para_windows":
        copiar_linux_para_windows(origem, destino, copiar_vazios, copiar_ocultos)

# Cria a janela principal
janela = tk.Tk()
janela.title("Cópia de Arquivos")

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

copiar_button = tk.Button(janela, text="Iniciar Cópia", command=iniciar_copia)
resultado = tk.Label(janela, text="")

# Organizar elementos na interface
origem_label.grid(row=0, column=0)
entrada_origem.grid(row=0, column=1)
selecionar_origem_button.grid(row=0, column=2)

destino_label.grid(row=1, column=0)
entrada_destino.grid(row=1, column=1)
selecionar_destino_button.grid(row=1, column=2)

copiar_diretorios_vazios_checkbox.grid(row=2, column=0, columnspan=3)
copiar_diretorios_ocultos_checkbox.grid(row=3, column=0, columnspan=3)

copiar_button.grid(row=4, column=0, columnspan=3)
resultado.grid(row=5, column=0, columnspan=3)

janela.mainloop()
