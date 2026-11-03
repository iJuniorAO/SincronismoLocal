# Sincronizador de Arquivos em Tempo Real

Script em Python para monitoramento e sincronização automática de arquivos e pastas em tempo real utilizando a biblioteca [Watchdog](https://github.com/gorakhargosh/watchdog). Ideal para espelhar relatórios e diretórios locais em pastas de rede ou sincronizadores de nuvem (como Google Drive, OneDrive ou Dropbox).

---

## 🚀 Funcionalidades

- **Monitoramento em Tempo Real:** Detecta eventos de criação (`on_created`) e alteração (`on_modified`) de arquivos.
- **Suporte Recursivo:** Monitora subpastas e replica a mesma estrutura de diretórios na pasta de destino.
- **Filtros Configuráveis:** Ignora arquivos temporários por prefixo (ex.: `~$` do Microsoft Office) e por extensão (ex.: `.tmp`, `.crdownload`).
- **Tempo de Espera para Gravação:** Evita erros de arquivo bloqueado (*file lock*) aguardando o término da escrita antes da cópia.
- **Preservação de Metadados:** Utiliza `shutil.copy2` para preservar datas de criação e modificação dos arquivos.
- **Execução Facilitada:** Acompanha arquivo de lote (`.bat`) para inicialização com um clique no Windows.

---

## 📁 Estrutura do Projeto

```text
├── app.py              # Script principal com a lógica do Watchdog e cópia de arquivos
├── config.json         # Arquivo de configuração (caminhos, filtros e tempos)
├── sincronizador.bat   # Script em lote para inicialização rápida no Windows
└── README.md           # Documentação do projeto
```

---

## 🛠️ Pré-requisitos

- **Python 3.8** ou superior instalado no sistema.
- Biblioteca **Watchdog**:

```bash
pip install watchdog
```

---

## ⚙️ Configuração (`config.json`)

Antes de iniciar a execução, ajuste o arquivo `config.json` de acordo com os diretórios desejados:

```json
{
    "origem": "C:\\caminho\\para\\pasta_origem",
    "destino": "C:\\caminho\\para\\pasta_destino",
    "tempo_espera_gravacao": 1.0,
    "recursivo": true,
    "ignorar_prefixos": [
        "~$"
    ],
    "ignorar_extensoes": [
        ".tmp",
        ".crdownload"
    ]
}
```

### Parâmetros:

| Parâmetro | Tipo | Descrição |
| :--- | :--- | :--- |
| `origem` | `string` | Caminho absoluto da pasta que será monitorada. |
| `destino` | `string` | Caminho absoluto da pasta onde os arquivos serão replicados. |
| `tempo_espera_gravacao` | `float` | Segundos de espera antes de copiar o arquivo (garante que o processo de escrita terminou). |
| `recursivo` | `boolean` | Se `true`, monitora todas as subpastas dentro da pasta de origem. |
| `ignorar_prefixos` | `list` | Lista de prefixos de arquivos a ignorar (ex.: `~$` para travas do Office). |
| `ignorar_extensoes` | `list` | Lista de extensões a ignorar durante a cópia (ex.: `.tmp`, `.crdownload`). |

> **Nota para Windows:** Ao definir caminhos no JSON, utilize barras invertidas duplas (`\\`) ou barras normais (`/`).

---

## ▶️ Como Usar

### Opção 1: Linha de comando

Abra o terminal na pasta do projeto e execute:

```bash
python app.py
```

### Opção 2: Arquivo Batch (`sincronizador.bat`)

Dê dois cliques no arquivo `sincronizador.bat`. Ele iniciará o terminal com saída desbufferizada (`-u`), exibindo os logs em tempo real.

> **Importante:** Se você mover a pasta do projeto, atualize o caminho do `app.py` dentro de `sincronizador.bat`.

---

## 📝 Exemplo de Saída dos Logs

```text
[03/11/2026 00:20:15] Iniciando monitoramento em: C:\Users\Downloads\teste_local
[03/11/2026 00:20:15] Destino configurado: C:\Users\Downloads\teste_drive
[03/11/2026 00:21:02] [Criação] Atualizado no Drive: relatorio_mensal.xlsx
[03/11/2026 00:21:40] [Alteração] Atualizado no Drive: notas.txt
```

Para interromper a execução, pressione `Ctrl + C` no terminal.

