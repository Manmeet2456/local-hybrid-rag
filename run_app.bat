@echo off
echo ===================================================
echo Starting Local Hybrid RAG Assistant...
echo ===================================================

:: Ensure cache directory exists on D: drive
if not exist "D:\cache" mkdir "D:\cache"

:: Redirect all AI/ML caches to D:\cache
set "HF_HOME=D:\cache\huggingface"
set "HUGGINGFACE_HUB_CACHE=D:\cache\huggingface\hub"
set "TRANSFORMERS_CACHE=D:\cache\huggingface\transformers"
set "TORCH_HOME=D:\cache\torch"
set "SENTENCE_TRANSFORMERS_HOME=D:\cache\sentence_transformers"
set "DOCLING_CACHE_DIR=D:\cache\docling"
set "EASYOCR_MODULE_PATH=D:\cache\easyocr"
set "STREAMLIT_CACHE_DIR=D:\cache\streamlit"

echo [1/2] Launching FastAPI Backend on http://localhost:8000...
start "RAG Backend (FastAPI)" cmd /k "cd /d "%~dp0backend" && set "HF_HOME=D:\cache\huggingface" && set "TORCH_HOME=D:\cache\torch" && set "DOCLING_CACHE_DIR=D:\cache\docling" && ".\venv\Scripts\uvicorn.exe" main:app --reload --host 127.0.0.1 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Launching Streamlit Frontend on http://localhost:8501...
start "RAG Frontend (Streamlit)" cmd /k "cd /d "%~dp0frontend" && "..\backend\venv\Scripts\streamlit.exe" run app.py"

echo ===================================================
echo Backend and Frontend have been started in new windows!
echo - Frontend: http://localhost:8501
echo - Backend API Docs: http://localhost:8000/docs
echo ===================================================
pause
