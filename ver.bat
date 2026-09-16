@echo off
cd /d "%~dp0docs"
echo Abriendo el ranking en http://localhost:8901 ...
start "" "http://localhost:8901/02-midnight-console.html"
python -m http.server 8901
