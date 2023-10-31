import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import main  # Importe o módulo main para acessar a função iniciar_copia

def selecionar_diretorio(label):
    diretorio = filedialog.askdirectory()
    label.delete(0, tk.END)
    label.insert(0, diretorio)

def criar_interface():
    janela = tk.Tk()
    janela.title("Roboco.py")
    
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
    
    copiar_button = tk.Button(janela, text="Iniciar Cópia", command=main.iniciar_copia)  # Chame a função do módulo main
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