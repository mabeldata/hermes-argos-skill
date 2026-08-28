#!/usr/bin/env python3
"""
Exemplo pro jornalista-aranha: ler emails do Gmail do usuario via Argos.

Uso:
    ./jornalista_gmail.py
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from argos_chromium import connect_argos, get_or_open_tab, disconnect_argos


def main():
    print("=== Jornalista Aranha: Gmail via Argos ===")

    browser = connect_argos()
    try:
        # Pega ou abre aba do Gmail
        gmail = get_or_open_tab(browser, "https://mail.google.com")
        print(f"Titulo: {gmail.title()}")
        print(f"URL: {gmail.url}")

        # Espera carregar
        time.sleep(5)

        # Pega top 5 emails
        emails = gmail.evaluate("""(max) => {
            return Array.from(document.querySelectorAll('tr.zA')).slice(0, max).map(row => ({
                from: row.querySelector('.yW .bA4 span')?.innerText || '',
                subject: row.querySelector('.bog')?.innerText || '',
                snippet: row.querySelector('.y2')?.innerText || ''
            }));
        }""", 5)

        print(f"\n{len(emails)} emails:")
        for i, e in enumerate(emails, 1):
            print(f"  {i}. {e['from'][:30]}")
            print(f"     Subject: {e['subject'][:60]}")
            print(f"     Snippet: {e['snippet'][:80]}")

    finally:
        disconnect_argos(browser)


if __name__ == "__main__":
    main()
