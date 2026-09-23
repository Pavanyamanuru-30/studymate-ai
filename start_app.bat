@echo off
echo Starting StudyMate AI Advanced Architecture...

echo [1/2] Starting FastAPI Backend on Port 8002...
start cmd /k ".\venv\Scripts\activate && uvicorn backend.main:app --host 127.0.0.1 --port 8002"

echo [2/2] Starting Streamlit Frontend...
timeout /t 3 /nobreak > nul
start cmd /k ".\venv\Scripts\activate && set BACKEND_URL=http://127.0.0.1:8002 && streamlit run app.py"

echo Both services are now running!
