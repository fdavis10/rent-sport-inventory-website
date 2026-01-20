#!/bin/bash

clear
echo ""
echo "╔═══════════════════════════════════════════════════╗"
echo "║   🎿 Система аренды спортивного инвентаря 🏂     ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не найден!"
    echo ""
    echo "📥 Скачай и установи Docker Desktop:"
    echo "   https://www.docker.com/products/docker-desktop/"
    echo ""
    read -p "Нажми Enter для выхода..."
    exit 1
fi

echo "✅ Docker найден"
echo ""
echo "🚀 Запускаю проект..."
echo "📌 При первом запуске это займёт 2-3 минуты"
echo ""
echo "⏳ Подожди пока увидишь:"
echo '   "Starting development server at http://0.0.0.0:8000/"'
echo ""
echo "Потом открой браузер:"
echo "🌐 http://localhost:8000/"
echo ""
echo "Для остановки нажми Cmd+C"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""


cd "$(dirname "$0")"

docker-compose up

echo ""
echo "Проект остановлен."
read -p "Нажми Enter для выхода..."