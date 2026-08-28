#!/usr/bin/env python3
"""Exemplo pro treinatouro: ler treinos do Calendar."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from argos_chromium import connect_argos, get_or_open_tab, disconnect_argos


def main():
    print("=== Treinatouro: Calendar via Argos")

    browser = connect_argos()
    try:
        cal = get_or_open_tab(browser, "https://calendar.google.com")
        time.sleep(5)

        events = cal.evaluate("""() => {
            return Array.from(document.querySelectorAll('[data-eventid]')).map(e => ({
                title: e.querySelector('[data-title]')?.innerText || '',
                time: e.querySelector('[data-time]')?.innerText || ''
            }));
        }""")

        print(f"\n{len(events)} eventos:")
        for i, e in enumerate(events, 1):
            print(f"  {i}. {e['time']} - {e['title']}")
    finally:
        disconnect_argos(browser)


if __name__ == "__main__":
    main()
