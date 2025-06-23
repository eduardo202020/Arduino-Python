#!/bin/bash

echo "===================================================="
echo "🌱 SISTEMA DE RIEGO INTELIGENTE CON HISTORIAL"
echo "🚀 ARDUINO-PYTHON - VERSIÓN AVANZADA"
echo "===================================================="
echo ""

echo "¿Qué quieres hacer?"
echo "1. 🔧 Simulador de riego (BACKEND)"
echo "2. 📊 Controlador de riego (TERMINAL)"
echo "3. 🌐 Dashboard Web Streamlit (PROFESIONAL)"
echo "4. 🚀 Demo completo automático"
echo "5. 🔍 Ver archivos del proyecto"
echo "6. 📋 Instrucciones de uso"
echo ""

read -p "Elige una opción (1-6): " option

case $option in
    1)
        echo ""
        echo "🔧 Iniciando simulador de riego..."
        echo "📊 Genera historial de 144 entradas (24 horas simuladas)"
        echo "🌐 Servidor en puerto 9999"
        echo "💡 Para detener: presiona Ctrl+C"
        echo ""
        python3 simulador_corregido.py
        ;;
    2)
        echo ""
        echo "📊 Iniciando controlador de riego..."
        echo "🔍 Dashboard interactivo con gráficos en terminal"
        echo "⚠️  IMPORTANTE: Asegúrate de que el simulador esté ejecutándose"
        echo ""
        python3 controlador_corregido.py
        ;;
    3)
        echo ""
        echo "🌐 Iniciando Dashboard Web Streamlit..."
        echo "📈 Dashboard profesional con gráficos interactivos"
        echo "🔧 Verificando dependencias..."
        
        # Verificar si streamlit está instalado
        if ! python3 -c "import streamlit" 2>/dev/null; then
            echo "📦 Instalando dependencias..."
            pip install -r requirements.txt
        fi
        
        echo "🚀 Abriendo dashboard en el navegador..."
        echo "📱 URL: http://localhost:8501"
        echo "💡 Para detener: presiona Ctrl+C"
        echo ""
        streamlit run dashboard_streamlit.py
        ;;
    4)
        echo ""
        echo "🚀 INICIANDO DEMO COMPLETO..."
        echo "🔧 Abriendo simulador en segundo plano..."
        python3 simulador_corregido.py &
        SIMULATOR_PID=$!
        
        echo "⏳ Esperando 4 segundos para que cargue el historial..."
        sleep 4
        
        echo "📊 Iniciando controlador..."
        python3 controlador_corregido.py
        
        echo "🔄 Deteniendo simulador..."
        kill $SIMULATOR_PID 2>/dev/null
        echo "✅ Demo finalizado"
        ;;
    5)
        echo ""
        echo "📁 ARCHIVOS DEL PROYECTO:"
        echo "=================================="
        echo "🔧 simulador_corregido.py - Simulador backend"
        echo "📊 controlador_corregido.py - Controlador terminal"
        echo "🌐 dashboard_streamlit.py - Dashboard web profesional"
        echo "🤖 sistema_riego.ino - Código Arduino"
        echo "📋 requirements.txt - Dependencias Python"
        echo "🚀 run.sh - Este menú"
        echo ""
        ls -la *.py *.ino *.txt 2>/dev/null
        ;;
    6)
        echo ""
        echo "📋 INSTRUCCIONES DE USO"
        echo "======================================================="
        echo ""
        echo "🌱 SISTEMA DE RIEGO INTELIGENTE"
        echo "• 2 Sensores de humedad del suelo"
        echo "• 2 Sensores de temperatura"
        echo "• 2 Bombas/válvulas de riego independientes"
        echo "• Historial de 144 entradas (24 horas)"
        echo "• Dashboard con gráficos en tiempo real"
        echo "• Control automático y manual"
        echo ""
        echo "🌐 DASHBOARD WEB STREAMLIT (RECOMENDADO):"
        echo "   Opción 3: Dashboard web profesional"
        echo "   • Gráficos interactivos con Plotly"
        echo "   • Métricas en tiempo real"
        echo "   • Interfaz moderna y responsive"
        echo "   • Control de bombas desde la web"
        echo ""
        echo "🔧 FORMA MANUAL (2 terminales):"
        echo "   Terminal 1: Opción 1 (Simulador)"
        echo "   Terminal 2: Opción 2 (Controlador terminal)"
        echo ""
        echo "🚀 DEMO AUTOMÁTICO:"
        echo "   Opción 4: Demo completo con controlador terminal"
        echo ""
        echo "🤖 PARA ARDUINO FÍSICO:"
        echo "   1. Sube sistema_riego.ino al Arduino"
        echo "   2. Conecta sensores según esquema"
        echo "   3. Modifica controlador para puerto serie"
        echo ""
        echo "📊 FUNCIONES DEL DASHBOARD WEB:"
        echo "   • Estado actual con métricas coloridas"
        echo "   • Gráficos de tendencias interactivos"
        echo "   • Estadísticas detalladas con charts"
        echo "   • Control de bombas via web"
        echo "   • Auto-actualización en tiempo real"
        echo "   • Visualización de eficiencia del sistema"
        echo ""
        echo "📦 INSTALACIÓN DE DEPENDENCIAS:"
        echo "   pip install -r requirements.txt"
        echo ""
        ;;
    *)
        echo "❌ Opción no válida"
        ;;
esac
