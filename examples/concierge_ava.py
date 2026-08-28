#!/usr/bin/env python3
"""Exemplo pro concierge: automatizar AVA Univesp."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from argos_chromium import connect_argos, get_or_open_tab, disconnect_argos


def main():
    print("=== Concierge: AVA Quiz via Argos")

    browser = connect_argos()
    try:
        page = get_or_open_tab(browser, "https://ava.univesp.br")
        time.sleep(3)

        # Aqui: navegar ate a atividade, extrair Q&A, perguntar ao Gemini, etc.
        print("Conectado! Prossiga com a logica do quiz.")
    finally:
        disconnect_argos(browser)


if __name__ == "__main__":
    main()
