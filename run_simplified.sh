#!/bin/bash

echo "===================================================="
echo "🌱 SISTEMA DE RIEGO INTELIGENTE PROFESIONAL"
echo "🚀 DASHBOARD STREAMLIT CON SIMULACIÓN 3D"
echo "===================================================="
echo ""

echo "🌐 Iniciando Dashboard Web Streamlit..."
echo "📈 Dashboard profesional con funcionalidades integradas:"
echo "   • 📊 Gráficos interactivos en tiempo real"
echo "   • 🌡️ Monitoreo de sensores avanzados"
echo "   • 🎮 Simulación 3D con Plotly"
echo "   • 🌳 Simulación 3D de Árboles con Three.js"
echo "   • 🎛️ Control de riego automático y manual"
echo "   • 📈 Historial y análisis de datos"
echo ""
echo "🔧 Verificando dependencias..."

# Verificar si streamlit está instalado
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt
fi

# Verificar otras dependencias críticas
echo "🔍 Verificando dependencias críticas..."
if ! python3 -c "import plotly" 2>/dev/null; then
    echo "📦 Instalando plotly..."
    pip install plotly
fi

if ! python3 -c "import numpy" 2>/dev/null; then
    echo "📦 Instalando numpy..."
    pip install numpy
fi

if ! python3 -c "import pandas" 2>/dev/null; then
    echo "📦 Instalando pandas..."
    pip install pandas
fi

echo ""
echo "🚀 Abriendo dashboard en el navegador..."
echo "📱 URL: http://localhost:8501"
echo ""
echo "🎯 PESTAÑAS DISPONIBLES:"
echo "   📊 Dashboard Principal - Gráficos y métricas en tiempo real"
echo "   🎮 Simulación 3D - Visualización interactiva con Plotly"
echo "   🌳 Árboles 3D - Simulación ultra-realista con Three.js"
echo ""
echo "🎮 CARACTERÍSTICAS:"
echo "   🌡️ Termómetros visuales en cada árbol"
echo "   🔧 Sistema de tuberías subterráneas"
echo "   💧 Dispersión de agua realista"
echo "   🎛️ Controles de temperatura, humedad y riego"
echo "   📈 Análisis automático de salud de plantas"
echo ""
echo "💡 Para detener: presiona Ctrl+C"
echo ""

# Iniciar Streamlit
streamlit run dashboard_streamlit.py
