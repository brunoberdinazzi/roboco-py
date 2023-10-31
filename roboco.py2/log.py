import datetime

class Log:
    def __init__(self):
        self.log_file = "copia_log.txt"

    def registrar_mensagem(self, mensagem):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as file:
            file.write(f"[{timestamp}] {mensagem}\n")

    def limpar_log(self):
        open(self.log_file, "w").close()  # Limpa o arquivo de log
