@echo off
chcp 65001 > nul
cls
echo.
echo ╔═══════════════════════════════════════════════════╗
echo ║   🎿 Система аренды спортивного инвентаря 🏂     ║
echo ╚═══════════════════════════════════════════════════╝
echo.

REM 
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker не найден!
    echo.
    echo 📥 Скачай и установи Docker Desktop:
    echo    https://www.docker.com/products/docker-desktop/
    echo.
    pause
    exit
)

echo ✅ Docker найден
echo.
echo 🚀 Запускаю проект...
echo 📌 При первом запуске это займёт 2-3 минуты
echo.
echo ⏳ Подожди пока увидишь:
echo    "Starting development server at http://0.0.0.0:8000/"
echo.
echo Потом открой браузер:
echo 🌐 http://localhost:8000/
echo.
echo Для остановки нажми Ctrl+C
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

docker-compose up

echo.
echo Проект остановлен.
pause