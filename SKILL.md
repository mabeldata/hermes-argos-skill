---
name: argos-chromium
description: Conecta ao Argos Chromium (CDP) para automacao web. Auto-descobre o container, suporta Playwright/Puppeteer/Selenium. Detecta login e espera o usuario logar manualmente.
trigger: "Conectar ao Argos", "automacao Chromium", "CDP", "browser headless"
---

# argos-chromium

Skill Hermes Agent pra conectar ao [Argos Chromium](https://github.com/mabeldata/argos-chromium) — uma imagem Docker custom que expoe o Chrome DevTools Protocol (CDP) externamente.

## O que e o Argos?

Argos e um container Docker baseado no `linuxserver/chromium` com:

- Interface visual via noVNC/KasmVNC (voce pode ver e interagir manualmente)
- CDP exposto externamente via socat (resolve o problema de localhost binding)
- Flag `--remote-allow-origins=*` para aceitar conexoes externas
- Sessao persistente (cookies/logins sobrevivem a restart)

## Quick Start

### 1. Iniciar o Argos

```bash
docker run -d \
  --name argos \
  -p 3000:3000 -p 3001:3001 -p 9224:9224 \
  -v argos-config:/config \
  --shm-size=1gb \
  --security-opt seccomp=unconfined \
  mabeldata/argos-chromium:latest
```

### 2. Conectar (Python)

```python
import sys
sys.path.insert(0, "/caminho/para/argos-chromium")
from argos_chromium import connect_argos, list_tabs

browser = connect_argos()  # auto-descoberta
print(list_tabs(browser))
```

### 3. Conectar (qualquer linguagem)

```bash
# Healthcheck
curl http://localhost:9224/json/version

# WebSocket URL
curl -s http://localhost:9224/json/version | jq -r '.webSocketDebuggerUrl'
```

## Funcoes Principais

| Funcao | Descricao |
|--------|-----------|
| `connect_argos(url=None)` | Conecta via CDP (auto-descoberta por padrao) |
| `disconnect_argos(browser)` | Para Playwright (browser continua rodando) |
| `list_tabs(browser)` | Lista todas as abas abertas |
| `get_tab(browser, url_match)` | Acha aba por substring de URL |
| `open_tab(browser, url)` | Abre nova aba |
| `wait_for_login(page, timeout=120)` | Detecta login wall e espera |

## Configuracao via Variaveis de Ambiente

| Variavel | Default | Descricao |
|----------|---------|-----------|
| `ARGOS_HOST` | `localhost` | Hostname do container |
| `ARGOS_PORT` | `9224` | Porta CDP exposta (socat) |
| `ARGOS_URL` | `http://{HOST}:{PORT}` | URL completa CDP |

## Exemplos

### Preencher formulario

```python
from argos_chromium import connect_argos, open_tab

browser = connect_argos()
page = open_tab(browser, "https://minha-app.com/login")
page.fill('input[name="email"]', "user@example.com")
page.fill('input[name="password"]', "secret")
page.click('button[type="submit"]')
```

### Esperar login humano

```python
from argos_chromium import connect_argos, open_tab, wait_for_login

browser = connect_argos()
page = open_tab(browser, "https://app.com/login")
if not wait_for_login(page, timeout=180):
    print("Usuario nao fez login")
```

### Ler emails do Gmail

```python
from argos_chromium import connect_argos, get_tab, list_tabs

browser = connect_argos()
gmail = get_tab(browser, "mail.google.com")

emails = gmail.evaluate("""() => {
    return Array.from(document.querySelectorAll('tr.zA')).slice(0, 5).map(row => ({
        from: row.querySelector('.yW')?.innerText || '',
        subject: row.querySelector('.bog')?.innerText || ''
    }));
}""")
```

## Troubleshooting

### "Argos nao encontrado"

```bash
# Verifique se container esta rodando
docker ps | grep argos

# Verifique a porta
curl http://localhost:9224/json/version
```

### "Connection refused"

- Container parado? `docker start argos`
- Firewall bloqueando? Libere porta 9224
- Outra instancia usando a porta? Mude `ARGOS_PORT`

## Links

- 🐙 **Argos Chromium:** https://github.com/mabeldata/argos-chromium
- 🐳 **Docker Hub:** https://hub.docker.com/r/mabeldata/argos-chromium
- 📖 **Documentacao completa:** https://github.com/mabeldata/argos-chromium#readme
- 🤖 **Hermes Agent:** https://hermes-agent.nousresearch.com/

## Creditos

Criado por Breno Yano (Mabel Data) em 2026 para ser usado com o Hermes Agent.
