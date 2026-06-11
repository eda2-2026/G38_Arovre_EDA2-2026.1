#!/bin/bash

# Cores para o terminal
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Configurando o ambiente para o Organizador de Pelada (AVL)...${NC}"

# Criar venv se não existir
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Ativar venv e instalar dependências
source venv/bin/activate
pip install -r requirements.txt

echo -e "${GREEN}Iniciando o servidor FastAPI...${NC}"
echo -e "${GREEN}Acesse: http://127.0.0.1:8000${NC}"

# Iniciar o servidor
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
