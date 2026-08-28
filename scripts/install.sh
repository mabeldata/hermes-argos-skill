#!/bin/bash
# install.sh - Instala a skill argos-chromium no ~/.hermes/skills/

set -e

SKILL_DIR="${HOME}/.hermes/skills/argos-chromium"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Argos Chromium Skill Installer"
echo "=============================="
echo ""

# 1. Verifica dependencias
echo "[1/4] Verificando dependencias..."
if ! command -v python3 &>/dev/null; then
    echo "ERRO: python3 nao encontrado"
    exit 1
fi
if ! python3 -c "import playwright" 2>/dev/null; then
    echo "AVISO: playwright nao instalado. Instalando..."
    pip install playwright
    playwright install chromium
fi

# 2. Cria diretorio
echo "[2/4] Criando ${SKILL_DIR}..."
mkdir -p "${SKILL_DIR}"
mkdir -p "${SKILL_DIR}/examples"
mkdir -p "${SKILL_DIR}/references"

# 3. Copia arquivos
echo "[3/4] Copiando arquivos..."
cp "${SCRIPT_DIR}/SKILL.md" "${SKILL_DIR}/"
cp "${SCRIPT_DIR}/argos_chromium.py" "${SKILL_DIR}/"
cp "${SCRIPT_DIR}/README.md" "${SKILL_DIR}/"
cp "${SCRIPT_DIR}/scripts/"*.sh "${SKILL_DIR}/" 2>/dev/null || true
cp -r "${SCRIPT_DIR}/examples/"* "${SKILL_DIR}/examples/" 2>/dev/null || true

chmod +x "${SKILL_DIR}/scripts/"*.sh 2>/dev/null || true

# 4. Valida
echo "[4/4] Validando instalacao..."
if python3 -c "import sys; sys.path.insert(0, '${SKILL_DIR}'); from argos_chromium import connect_argos; print('Import OK')"; then
    echo ""
    echo "Argos Chromium skill instalada em ${SKILL_DIR}"
    echo ""
    echo "Proximos passos:"
    echo "  1. Inicie o Argos:    docker run -d -p 9223:9223 mabeldata/argos-chromium:latest"
    echo "  2. Teste a conexao:    python3 ${SKILL_DIR}/argos_chromium.py"
    echo "  3. Use em qualquer script Python:"
    echo "     import sys; sys.path.insert(0, '${SKILL_DIR}')"
    echo "     from argos_chromium import connect_argos"
    echo "     browser = connect_argos()"
else
    echo "ERRO: falha na validacao"
    exit 1
fi
