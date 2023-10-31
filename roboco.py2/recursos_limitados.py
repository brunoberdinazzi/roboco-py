import os
import psutil

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
