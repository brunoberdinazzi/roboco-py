import psutil

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
