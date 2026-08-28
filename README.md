<div align="center">
  <img src="https://raw.githubusercontent.com/mabeldata/argos-chromium/main/icon.svg" alt="Argos Chromium" width="120" height="120">
  <h1>hermes-argos-skill</h1>
  <p>Skill Hermes Agent para conectar ao <a href="https://github.com/mabeldata/argos-chromium">Argos Chromium</a>.</p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
</div>

---

## 📖 Sobre

Skill Python que permite ao **Hermes Agent** conectar e controlar um navegador Chromium remoto (Argos) via Chrome DevTools Protocol (CDP).

## 🚀 Instalacao

```bash
curl -fsSL https://raw.githubusercontent.com/mabeldata/hermes-argos-skill/main/scripts/install.sh | bash
```

Ou manual:

```bash
git clone https://github.com/mabeldata/hermes-argos-skill.git
cd hermes-argos-skill
./scripts/install.sh
```

## 🛠️ Uso

```python
import sys
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/argos-chromium"))

from argos_chromium import connect_argos, list_tabs

browser = connect_argos()  # auto-descoberta via localhost:9223
tabs = list_tabs(browser)
print(tabs)
```

## 🔌 Requisitos

- Python 3.10+
- Playwright (`pip install playwright`)
- Argos Chromium rodando (veja [argos-chromium](https://github.com/mabeldata/argos-chromium))

## 📚 Documentacao

Veja [SKILL.md](SKILL.md) para a documentacao completa.

## 🤝 Contribuindo

Contribuicoes sao bem-vindas! Abra uma issue ou PR.

## 📜 Licenca

MIT — veja [LICENSE](LICENSE).

## 🔗 Links

- 🐙 **Argos Chromium:** https://github.com/mabeldata/argos-chromium
- 🐳 **Docker Hub:** https://hub.docker.com/r/mabeldata/argos-chromium
- 🤖 **Hermes Agent:** https://hermes-agent.nousresearch.com/
- 📧 **Contato:** support@mabeldata.app
