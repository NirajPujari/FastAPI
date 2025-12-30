@echo off

echo Loading .env...

set "PORT="
for /f "usebackq tokens=1,2 delims==" %%A in (".env") do (
    if /i "%%A"=="PORT" set "PORT=%%B"
)

if "%PORT%"=="" (
    echo PORT not found in .env, using default 8000
    set PORT=8000
)

echo Creating virtual environment if it does not exist...
IF NOT EXIST venv (
    python -m venv venv
)

echo Starting FastAPI server on port %PORT%...
call venv\Scripts\activate

echo Installing requirements...
pip install -r requirements.txt

echo FastAPI running at: http://127.0.0.1:%PORT%/
echo.

uvicorn main:app --host 127.0.0.1 --port %PORT% --reload --log-level debug

pause
