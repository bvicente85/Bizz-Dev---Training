@echo off
chcp 65001 >nul
title SKOLAE — BIZZ DEV AI
cd /d "%~dp0"

echo ============================================================================
echo   SKOLAE FORMACAO — BIZZ DEV AI (Desktop Local App)
echo   A iniciar o servidor FastAPI em http://127.0.0.1:8080 ...
echo ============================================================================

:: Abrir a janela desktop nativa (Edge / Chrome em modo App sem barra de endereco) apos 2 segundos
start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; if (Test-Path 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe') { Start-Process 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe' -ArgumentList '--app=http://127.0.0.1:8080','--window-size=1440,900' } elseif (Test-Path 'C:\Program Files\Google\Chrome\Application\chrome.exe') { Start-Process 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList '--app=http://127.0.0.1:8080','--window-size=1440,900' } else { Start-Process 'http://127.0.0.1:8080' }"

python "%~dp0app_bizzdev\server.py"
pause
