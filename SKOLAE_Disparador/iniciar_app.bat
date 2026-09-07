@echo off
title SKOLAE - Divulgações
echo A ler o teu Excel e a filtrar pessoas em periodo de descanso...
start cmd /k "python app.py"
timeout /t 3 /nobreak > NUL
start http://localhost:5000
