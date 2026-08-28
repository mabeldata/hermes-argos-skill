"""
argos_chromium.py - Skill Hermes pra conectar ao Argos Chromium via CDP.

Uso basico:
    from argos_chromium import connect_argos
    browser = connect_argos()
    page = browser.contexts[0].pages[0]
    print(page.title())
"""
import os
import sys
import time
import socket
from pathlib import Path


# Configuracoes (com fallback)
ARGOS_HOST = os.environ.get("ARGOS_HOST", "localhost")
ARGOS_PORT = int(os.environ.get("ARGOS_PORT", "9224"))
ARGOS_URL = os.environ.get("ARGOS_URL", f"http://{ARGOS_HOST}:{ARGOS_PORT}")


def is_port_open(host, port, timeout=2):
    """Verifica se porta ta aberta."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def discover_argos(search_range=None):
    """
    Descobre o Argos na rede local.
    Retorna URL ou None.
    """
    if search_range is None:
        search_range = range(9220, 9230)

    # Tenta localhost primeiro (padrao Argos: 9224 externa)
    if is_port_open("127.0.0.1", 9224):
        return "http://127.0.0.1:9224"
    if is_port_open("localhost", 9224):
        return "http://localhost:9224"

    # Tenta descobrir via mDNS/avahi (nao implementado ainda)
    # TODO: implementar mDNS lookup

    # Tenta portas alternativas
    for port in search_range:
        if is_port_open("127.0.0.1", port):
            return f"http://127.0.0.1:{port}"

    return None


def connect_argos(url=None, auto_discover=True):
    """
    Conecta ao Argos Chromium via CDP.

    Args:
        url: URL CDP exata (ex: http://localhost:9224). Se None, usa ARGOS_URL.
        auto_discover: Se True, tenta descobrir automaticamente.

    Returns:
        browser Playwright conectado.
    """
    from playwright.sync_api import sync_playwright

    # Auto-discovery
    if url is None and auto_discover:
        url = discover_argos()
        if url:
            print(f"[argos] Descoberto em: {url}", file=sys.stderr)
    elif url is None:
        url = ARGOS_URL

    print(f"[argos] Conectando em {url}...", file=sys.stderr)

    # Verifica conectividade primeiro
    if not is_port_open(ARGOS_HOST, ARGOS_PORT):
        raise ConnectionError(
            f"Argos nao encontrado em {url}. "
            f"Verifique se o container esta rodando: docker ps | grep argos"
        )

    # Conecta via Playwright
    pw = sync_playwright().start()
    try:
        browser = pw.chromium.connect_over_cdp(url)
        # Anexa _pw pra poder desconectar
        browser._argos_pw = pw
        return browser
    except Exception as e:
        pw.stop()
        raise RuntimeError(f"Falha ao conectar ao Argos em {url}: {e}")


def disconnect_argos(browser):
    """Para a conexao Playwright (browser continua rodando)."""
    pw = getattr(browser, "_argos_pw", None)
    if pw:
        try:
            pw.stop()
        except Exception:
            pass


def list_tabs(browser):
    """Lista todas as abas abertas."""
    result = []
    for ctx in browser.contexts:
        for page in ctx.pages:
            result.append({"url": page.url, "title": page.title(), "page": page})
    return result


def get_tab(browser, url_match=None, title_match=None):
    """Acha aba por URL ou titulo."""
    for ctx in browser.contexts:
        for page in ctx.pages:
            if url_match and url_match in page.url:
                return page
            if title_match and title_match in page.title():
                return page
    return None


def open_tab(browser, url):
    """Abre nova aba no primeiro contexto."""
    ctx = browser.contexts[0] if browser.contexts else None
    if not ctx:
        raise RuntimeError("Nenhum contexto disponivel no browser")
    page = ctx.new_page()
    if url:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
    return page


def wait_for_login(page, timeout=120):
    """Detecta login wall e espera o usuario logar manualmente."""
    login_keywords = ["login", "signin", "auth", "sso"]
    title_keywords = ["Login", "Sign in", "Entrar", "Bem-vindo"]

    start = time.time()
    while time.time() - start < timeout:
        url_lower = page.url.lower()
        title = page.title()
        is_login = any(k in url_lower for k in login_keywords) or any(k in title for k in title_keywords)
        if not is_login:
            return True
        time.sleep(5)
    return False


# Aliases em portugues
conectar = connect_argos
desconectar = disconnect_argos
listar_abas = list_tabs
achar_aba = get_tab
abrir_aba = open_tab


if __name__ == "__main__":
    print("=== argos-chromium skill teste ===")
    print(f"ARGOS_URL: {ARGOS_URL}")
    print(f"ARGOS_HOST: {ARGOS_HOST}:{ARGOS_PORT}")
    print()

    browser = connect_argos(auto_discover=True)
    try:
        tabs = list_tabs(browser)
        print(f"\n{len(tabs)} aba(s):")
        for t in tabs[:10]:
            print(f"  - {t['title'][:60]} | {t['url'][:80]}")
    finally:
        disconnect_argos(browser)
    print("\nOK!")
