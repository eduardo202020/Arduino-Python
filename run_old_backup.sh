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
echo "5. 🧪 Test nuevos sensores"
echo "6. 🎭 Demo sensores especializados"
echo "7. 🎮 Simulación 3D Web (PLOTLY)"
echo "8. 🗺️ Simulación 3D ASCII (TERMINAL)"
echo "9. 📊 Simulación 3D Matplotlib"
echo "10. 🔍 Ver archivos del proyecto"
echo "11. 📋 Instrucciones de uso"
echo "12. 🌳 Simulación 3D Árboles Three.js (NUEVA)"
echo ""

read -p "Elige una opción (1-12): " option

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
        echo "⚠️ IMPORTANTE: Asegúrate de que el simulador esté ejecutándose"
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
        echo "🧪 TESTING: NUEVOS SENSORES"
        echo "=============================="
        echo "🌿 Temperatura de la planta"
        echo "🌫️ Humedad relativa del entorno"
        echo ""
        python3 test_nuevos_sensores.py
        ;;
    6)
        echo ""
        echo "🎭 DEMO: SENSORES ESPECIALIZADOS"
        echo "================================="
        echo "🌿 Simulación de temperatura de planta"
        echo "🌫️ Simulación de humedad relativa"
        echo "⏱️ Demo de 20 segundos con ciclo día/noche"
        echo ""
        python3 demo_sensores.py
        ;;
    7)
        echo ""
        echo "🎮 SIMULACIÓN 3D WEB (PLOTLY)"
        echo "=============================="
        echo "🌐 Visualización 3D interactiva en navegador"
        echo "🌡️ Campos de temperatura y humedad"
        echo "🚿 Efectos de riego en tiempo real"
        echo ""
        echo "🔧 Verificando dependencias..."
        if ! python3 -c "import plotly" 2>/dev/null; then
            echo "📦 Instalando plotly..."
            pip install plotly
        fi
        echo "🚀 Generando simulación 3D web..."
        
        # Usar la versión funcional
        python3 simulacion_3d_web_funcional.py
        
        if [ -f "simulacion_riego_3d_funcional.html" ]; then
            echo ""
            echo "✅ ¡SIMULACIÓN 3D GENERADA EXITOSAMENTE!"
            echo "📂 Archivo: simulacion_riego_3d_funcional.html"
            echo "🌐 Abre este archivo en tu navegador para ver la simulación"
            echo "🎮 La simulación incluye:"
            echo "   • 🌡️ Campo de temperatura 3D"
            echo "   • 💧 Campo de humedad 3D"
            echo "   • 🌱 Vista combinada con jets de riego"
            echo "   • 📊 Estado en tiempo real de las plantas"
        else
            echo "❌ Error generando simulación 3D"
            echo "💡 Verifica que plotly esté instalado: pip install plotly"
        fi
        ;;
    8)
        echo ""
        echo "🗺️ SIMULACIÓN 3D ASCII (TERMINAL)"
        echo "=================================="
        echo "🎮 Vista 3D del terreno en terminal"
        echo "🌡️ Campos de temperatura visualizados"
        echo "💧 Efectos de riego en ASCII"
        echo "⚡ Sin dependencias externas"
        echo ""
        python3 simulacion_3d_ascii.py
        ;;
    9)
        echo ""
        echo "📊 SIMULACIÓN 3D MATPLOTLIB"
        echo "============================"
        echo "🎯 Visualización 3D con matplotlib"
        echo "📈 Gráficos científicos detallados"
        echo "🔄 Animación en tiempo real"
        echo ""
        echo "🔧 Verificando dependencias..."
        if ! python3 -c "import matplotlib" 2>/dev/null; then
            echo "📦 Instalando matplotlib..."
            pip install matplotlib
        fi
        echo "🚀 Iniciando simulación 3D matplotlib..."
        python3 simulacion_3d.py
        ;;
    10)
        echo ""
        echo "📁 ARCHIVOS DEL PROYECTO:"
        echo "=================================="
        echo "🔧 simulador_corregido.py - Simulador backend"
        echo "📊 controlador_corregido.py - Controlador terminal"
        echo "🌐 dashboard_streamlit.py - Dashboard web profesional"
        echo "🌳 simulacion_arbol_threejs.html - Simulación 3D árboles"
        echo "🤖 sistema_riego.ino - Código Arduino"
        echo "📋 requirements.txt - Dependencias Python"
        echo "🚀 run.sh - Este menú"
        echo ""
        ls -la *.py *.html *.ino *.txt *.sh 2>/dev/null | head -20
        ;;
    11)
        echo ""
        echo "📋 INSTRUCCIONES DE USO"
        echo "======================================================="
        echo ""
        echo "🌱 SISTEMA DE RIEGO INTELIGENTE"
        echo "• 2 Sensores de humedad del suelo"
        echo "• 2 Sensores de temperatura ambiente"
        echo "• 🌿 Sensor de temperatura de la planta"
        echo "• 🌫️ Sensor de humedad relativa del entorno"
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
        echo "   • 🌳 Nueva pestaña con árboles 3D realistas"
        echo ""
        echo "🔧 FORMA MANUAL (2 terminales):"
        echo "   Terminal 1: Opción 1 (Simulador)"
        echo "   Terminal 2: Opción 2 (Controlador terminal)"
        echo ""
        echo "🚀 DEMO AUTOMÁTICO:"
        echo "   Opción 4: Demo completo con controlador terminal"
        echo ""
        echo "🌳 SIMULACIÓN 3D ÁRBOLES (NUEVA):"
        echo "   Opción 12: Visualización ultra-realista con Three.js"
        echo "   • Árboles 3D con follaje multicapa"
        echo "   • Partículas de agua animadas"
        echo "   • Efectos ambientales (viento, luz)"
        echo "   • Cambios de color según salud"
        echo ""
        echo "🤖 PARA ARDUINO FÍSICO:"
        echo "   1. Sube sistema_riego.ino al Arduino"
        echo "   2. Conecta sensores según esquema"
        echo "   3. Modifica controlador para puerto serie"
        echo ""
        echo "📦 INSTALACIÓN DE DEPENDENCIAS:"
        echo "   pip install -r requirements.txt"
        echo ""
        ;;
    12)
        echo ""
        echo "🌳 SIMULACIÓN 3D ÁRBOLES THREE.JS"
        echo "=================================="
        echo "🌱 Visualización 3D ultra-realista con árboles"
        echo "🎮 Efectos ambientales avanzados"
        echo "💧 Partículas de agua animadas"
        echo ""
        echo "Opciones disponibles:"
        echo "a) 🌐 Simulación independiente (HTML)"
        echo "b) 📊 Integración en dashboard Streamlit"
        echo ""
        read -p "Selecciona opción (a/b): " threejs_option
        
        case $threejs_option in
            a)
                echo "🌳 Abriendo simulación Three.js independiente..."
                if [ -f "simulacion_arbol_threejs.html" ]; then
                    echo "📂 Archivo encontrado: simulacion_arbol_threejs.html"
                    echo "🌐 Abriendo en navegador predeterminado..."
                    if command -v xdg-open > /dev/null; then
                        xdg-open simulacion_arbol_threejs.html
                    elif command -v open > /dev/null; then
                        open simulacion_arbol_threejs.html
                    elif command -v start > /dev/null; then
                        start simulacion_arbol_threejs.html
                    else
                        echo "⚠️ No se pudo abrir automáticamente."
                        echo "📍 Abre manualmente: $(pwd)/simulacion_arbol_threejs.html"
                    fi
                    echo ""
                    echo "✅ ¡SIMULACIÓN THREE.JS CARGADA!"
                    echo "🎮 CONTROLES:"
                    echo "   • Arrastra para rotar la cámara"
                    echo "   • Scroll para zoom in/out"
                    echo "   • Ajusta temperatura y humedad"
                    echo "   • Activa riego para ver partículas"
                    echo "   • Observa el cambio de color de los árboles"
                else
                    echo "❌ Error: simulacion_arbol_threejs.html no encontrado"
                    echo "🔧 Ejecutando script para crear el archivo..."
                    python3 simulacion_arbol_threejs_streamlit.py
                fi
                ;;
            b)
                echo "🌳 Iniciando dashboard con simulación Three.js integrada..."
                echo "🌐 Dashboard con Three.js disponible en: http://localhost:8501"
                echo "📍 Ve a la pestaña '🌳 Árboles 3D' para ver la simulación realista"
                echo "💡 Para detener: presiona Ctrl+C"
                echo ""
                streamlit run dashboard_streamlit.py --server.port 8501 --server.headless true
                ;;
            *)
                echo "❌ Opción no válida"
                ;;
        esac
        ;;
    *)
        echo "❌ Opción no válida. Por favor, selecciona una opción del 1 al 12."
        ;;
esac
