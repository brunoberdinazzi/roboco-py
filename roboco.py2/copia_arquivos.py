import subprocess

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
