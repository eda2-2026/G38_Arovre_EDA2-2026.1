@echo off
echo Configurando o ambiente para o Organizador de Pelada (AVL)...

:: Criar venv se nao existir
if not exist venv (
    python -m venv venv
)

:: Ativar venv e instalar dependencias
call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo Iniciando o servidor FastAPI...
echo Acesse: http://127.0.0.1:8000
echo.

:: Abrir o navegador automaticamente
start http://127.0.0.1:8000

:: Iniciar o servidor
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause
