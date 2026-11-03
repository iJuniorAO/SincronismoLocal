import os
import sys
import shutil
import time
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Localiza o config.json na mesma pasta do script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")


def carregar_configuracao():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(
            f"Arquivo de configuração não encontrado: {CONFIG_PATH}"
        )
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


CONFIG = carregar_configuracao()
ORIGEM = CONFIG.get("origem")
DESTINO = CONFIG.get("destino")
TEMPO_ESPERA = CONFIG.get("tempo_espera_gravacao", 1.0)
IGNORAR_PREFIXOS = tuple(CONFIG.get("ignorar_prefixos", ["~$"]))
IGNORAR_EXTENSOES = tuple(CONFIG.get("ignorar_extensoes", [".tmp"]))


def log(mensagem):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{agora}] {mensagem}", flush=True)


class HandlerRelatorios(FileSystemEventHandler):
    def copiar_arquivo(self, src_path, tipo):
        nome_arquivo = os.path.basename(src_path)

        if nome_arquivo.startswith(IGNORAR_PREFIXOS) or nome_arquivo.endswith(
            IGNORAR_EXTENSOES
        ):
            return

        caminho_relativo = os.path.relpath(src_path, ORIGEM)
        caminho_destino = os.path.join(DESTINO, caminho_relativo)

        os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)

        try:
            time.sleep(TEMPO_ESPERA)
            shutil.copy2(src_path, caminho_destino)
            log(f"[{tipo}] Atualizado no Drive: {nome_arquivo}")
        except Exception as e:
            log(f"[ERRO] Falha ao copiar {nome_arquivo}: {e}")

    def on_created(self, event):
        if not event.is_directory:
            self.copiar_arquivo(event.src_path, "Criação")

    def on_modified(self, event):
        if not event.is_directory:
            self.copiar_arquivo(event.src_path, "Alteração")


if __name__ == "__main__":
    if not os.path.exists(ORIGEM):
        log(f"[ERRO] Não foi possível acessar a pasta de origem: {ORIGEM}")
        sys.exit(1)

    event_handler = HandlerRelatorios()
    observer = Observer()
    observer.schedule(
        event_handler, path=ORIGEM, recursive=CONFIG.get("recursivo", True)
    )

    log(f"Iniciando monitoramento em: {ORIGEM}")
    log(f"Destino configurado: {DESTINO}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log("Encerrando o monitoramento...")
        observer.stop()
    observer.join()
