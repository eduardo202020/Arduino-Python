#!/bin/becho "¿Qué quieres hacer?"
echo "1. 🔧 Simulador de riego (BACKEND)"
echo "2. 📊 Controlador de riego (FRONTEND)"
echo "3. 🌐 Dashboard Web Streamlit (PROFESIONAL)"
echo "4. 🚀 Demo completo automático"
echo "5. 🔍 Ver archivos del proyecto"
echo "6. 📋 Instrucciones de uso"
echo ""

read -p "Elige una opción (1-6): " option "===================================================="
echo "🌱 SISTEMA DE RIEGO INTELIGENTE CON HISTORIAL"
echo "🚀 ARDUINO-PYTHON - VERSIÓN AVANZADA"
echo "===================================================="
echo ""

echo "¿Qué quieres hacer?"
echo "1. 🔧 Simulador de riego (BACKEND)"
echo "2. � Controlador de riego (FRONTEND)"
echo "3. 🚀 Demo completo automático"
echo "4. 🔍 Ver archivos del proyecto"
echo "5. 📋 Instrucciones de uso"
echo ""

read -p "Elige una opción (1-5): " option

case $option in
    1)
        echo ""
        echo "🔧 Iniciando simulador de riego..."
        echo "� Genera historial de 144 entradas (24 horas simuladas)"
        echo "🌐 Servidor en puerto 9999"
        echo "💡 Para detener: presiona Ctrl+C"
        echo ""
        python3 simulador_corregido.py
        ;;
    2)
        echo ""
        echo "� Iniciando controlador de riego..."
        echo "🔍 Dashboard interactivo con gráficos"
        echo "⚠️  IMPORTANTE: Asegúrate de que el simulador esté ejecutándose"
        echo ""
        python3 controlador_corregido.py
        ;;
    3)
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
    4)
        echo ""
        echo "📁 ARCHIVOS DEL PROYECTO:"
        echo "=================================="
        echo "� simulador_corregido.py - Simulador backend"
        echo "📊 controlador_corregido.py - Controlador frontend"
        echo "🤖 sistema_riego.ino - Código Arduino"
        echo "🚀 run.sh - Este menú"
        echo ""
        ls -la *.py *.ino 2>/dev/null
        ;;
    5)
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
        echo "🚀 FORMA FÁCIL (RECOMENDADA):"
        echo "   Opción 3: Demo completo automático"
        echo ""
        echo "� FORMA MANUAL (2 terminales):"
        echo "   Terminal 1: Opción 1 (Simulador)"
        echo "   Terminal 2: Opción 2 (Controlador)"
        echo ""
        echo "🤖 PARA ARDUINO FÍSICO:"
        echo "   1. Sube sistema_riego.ino al Arduino"
        echo "   2. Conecta sensores según esquema"
        echo "   3. Modifica controlador para puerto serie"
        echo ""
        echo "📊 FUNCIONES DEL DASHBOARD:"
        echo "   • Ver estado actual de sensores"
        echo "   • Historial y estadísticas"
        echo "   • Gráficos de temperatura y humedad"
        echo "   • Control manual de bombas"
        echo "   • Modo automático inteligente"
        echo ""
        ;;
    *)
        echo "❌ Opción no válida"
        ;;
esacn/becho "¿Qué quieres hacer?"
echo "1. 🤖 Simulador básico (sin historial)"
echo     8)
        echo ""
        echo "� Archivos del proyecto:"
        echo "=======    10)
        echo ""
        echo "🚀 INICIANDO DEMO AVANZADO ORIGINAL..."
        echo "🔧 Abriendo simulador avanzado en segundo plano..."
        python3 simulador_riego_avanzado.py &
        SIMULATOR_PID=$!
        
        echo "⏳ Esperando 4 segundos para que cargue el historial..."
        sleep 4
        
        echo "📈 Iniciando controlador avanzado..."
        python3 controlador_riego_avanzado.py
        
        echo "🔄 Deteniendo simulador..."
        kill $SIMULATOR_PID 2>/dev/null
        echo "✅ Demo avanzado original finalizado"
        ;;
    *)========="
        echo "�🚀 SIMULADORES:"
        echo "• simulador_riego.py - Básico"
        echo "• simulador_riego_avanzado.py - Con historial"
        echo "• simulador_corregido.py - VERSION CORREGIDA ⭐"
        echo ""
        echo "🎮 CONTROLADORES:"
        echo "• controlador_riego.py - Básico"
        echo "• controlador_riego_avanzado.py - Con gráficos"
        echo "• controlador_corregido.py - VERSION CORREGIDA ⭐"
        echo ""
        echo "🔧 ARDUINO:"
        echo "• sistema_riego.ino - Código completo"
        echo ""
        echo "📄 OTROS:"
        echo "• run.sh - Este menú"
        ls -la *.py 2>/dev/null | grep -v "test\|find\|comunicacion" || echo ""
        ;;
    9)nzado (CON HISTORIAL)"
echo "3. 🎮 Controlador básico"
echo "4. 📈 Controlador avanzado (CON GRÁFICOS)"
echo "5. 🔧 Simulador CORREGIDO (RECOMENDADO)"
echo "6. 📊 Controlador CORREGIDO (RECOMENDADO)"
echo "7. 🚀 Demo CORREGIDO completo"
echo "8. 🔍 Ver archivos del proyecto"
echo "9. 📋 Mostrar instrucciones completas"
echo "10. 🏃 Demo avanzado original"
echo ""

read -p "Elige una opción (1-10): " option===================================================="
echo "🌱 SISTEMA DE RIEGO INTELIGENTE CON HISTORIAL"
echo "🚀 ARDUINO-PYTHON - VERSIÓN AVANZADA"
echo "===================================================="
echo ""

echo "¿Qué quieres hacer?"
echo "1. 🤖 Simulador básico (sin historial)"
echo "2. 🚀 Simulador avanzado (CON HISTORIAL)"
echo "3. 🎮 Controlador básico"
echo "4. 📈 Controlador avanzado (CON GRÁFICOS)"
echo "5. 🔍 Ver archivos del proyecto"
echo "6. 📋 Mostrar instrucciones completas"
echo "7. � Demo completo avanzado"
echo ""

read -p "Elige una opción (1-7): " option

case $option in
    1)
        echo ""
        echo "🤖 Iniciando simulador básico..."
        echo "💡 Para detener: presiona Ctrl+C"
        python3 simulador_riego.py
        ;;
    2)
        echo ""
        echo "🚀 Iniciando simulador avanzado con historial..."
        echo "📊 Carga 144 entradas de historial ficticio (24 horas)"
        echo "💡 Para detener: presiona Ctrl+C"
        python3 simulador_riego_avanzado.py
        ;;
    3)
        echo ""
        echo "🎮 Iniciando controlador básico..."
        python3 controlador_riego.py
        ;;
    4)
        echo ""
        echo "📈 Iniciando controlador avanzado con gráficos..."
        echo "🔍 Incluye historial, estadísticas y visualizaciones"
        python3 controlador_riego_avanzado.py
        ;;
    5)
        echo ""
        echo "🔧 Iniciando simulador CORREGIDO (RECOMENDADO)..."
        echo "📊 Version mejorada con historial robusto"
        echo "💡 Para detener: presiona Ctrl+C"
        python3 simulador_corregido.py
        ;;
    6)
        echo ""
        echo "📊 Iniciando controlador CORREGIDO (RECOMENDADO)..."
        echo "🔍 Version mejorada con parseo robusto"
        python3 controlador_corregido.py
        ;;
    7)
        echo ""
        echo "🚀 INICIANDO DEMO CORREGIDO COMPLETO..."
        echo "🔧 Abriendo simulador corregido en segundo plano..."
        python3 simulador_corregido.py &
        SIMULATOR_PID=$!
        
        echo "⏳ Esperando 4 segundos para que cargue el historial..."
        sleep 4
        
        echo "📊 Iniciando controlador corregido..."
        python3 controlador_corregido.py
        
        echo "🔄 Deteniendo simulador..."
        kill $SIMULATOR_PID 2>/dev/null
        echo "✅ Demo corregido finalizado"
        ;;
    8)
        echo ""
        echo "📁 Archivos del proyecto:"
        echo "=================================="
        echo "🚀 SIMULADORES:"
        echo "• simulador_riego.py - Básico"
        echo "• simulador_riego_avanzado.py - Con historial"
        echo ""
        echo "🎮 CONTROLADORES:"
        echo "• controlador_riego.py - Básico"
        echo "• controlador_riego_avanzado.py - Con gráficos"
        echo ""
        echo "� ARDUINO:"
        echo "• sistema_riego.ino - Código completo"
        echo ""
        echo "� OTROS:"
        echo "• run.sh - Este menú"
        ls -la *.py 2>/dev/null | grep -v "test\|find\|comunicacion" || echo ""
        ;;
    9)
        echo ""
        echo "📋 INSTRUCCIONES COMPLETAS"
        echo "======================================================="
        echo ""
        echo "🌱 SISTEMA DE RIEGO INTELIGENTE CON HISTORIAL"
        echo "• 2 Sensores de humedad del suelo"
        echo "• 2 Sensores de temperatura"
        echo "• 2 Bombas/válvulas de riego independientes"
        echo "• Historial de 24 horas (144 entradas)"
        echo "• Gráficos y estadísticas en tiempo real"
        echo "• Control automático basado en umbrales"
        echo ""
        echo "⭐ VERSIONES CORREGIDAS (RECOMENDADAS):"
        echo "• 🔧 simulador_corregido.py - Simulador mejorado"
        echo "• 📊 controlador_corregido.py - Controlador robusto"
        echo "• 🚀 Opción 7: Demo completo corregido"
        echo ""
        echo "🚀 VERSIÓN AVANZADA INCLUYE:"
        echo "• 📊 Historial de 144 entradas (24 horas simuladas)"
        echo "• 📈 Gráficos de tendencias en texto"
        echo "• 📊 Estadísticas detalladas (min, max, promedio)"
        echo "• 🔍 Análisis de tendencias"
        echo "• 💡 Recomendaciones inteligentes"
        echo "• 🎮 Dashboard interactivo mejorado"
        echo ""
        echo "🔄 PARA USAR VERSIÓN CORREGIDA (RECOMENDADO):"
        echo "1. Terminal 1: ./run.sh y elegir opción 5 (simulador corregido)"
        echo "2. Terminal 2: ./run.sh y elegir opción 6 (controlador corregido)"
        echo "3. O usar opción 7 para demo automático completo"
        echo ""
        echo "🔧 PARA USAR ARDUINO REAL:"
        echo "1. Sube el código sistema_riego.ino al Arduino"
        echo "2. Conecta sensores según esquema"
        echo "3. Modifica controlador para puerto serie"
        echo ""
        echo "⚙️ DATOS FICTICIOS INCLUIDOS:"
        echo "• Historial de 24 horas con ciclos día/noche"
        echo "• Variaciones realistas de temperatura"
        echo "• Humedad con tendencias inversas"
        echo "• Estados de bombas basados en umbrales"
        echo "• Timestamps para análisis temporal"
        echo ""
        ;;
    10)
        echo ""
        echo "🚀 INICIANDO DEMO COMPLETO AVANZADO..."
        echo "� Abriendo simulador avanzado en segundo plano..."
        python3 simulador_riego_avanzado.py &
        SIMULATOR_PID=$!
        
        echo "⏳ Esperando 4 segundos para que cargue el historial..."
        sleep 4
        
        echo "📈 Iniciando controlador avanzado..."
        python3 controlador_riego_avanzado.py
        
        echo "🔄 Deteniendo simulador..."
        kill $SIMULATOR_PID 2>/dev/null
        echo "✅ Demo avanzado finalizado"
        ;;
    *)
        echo "❌ Opción no válida"
        ;;
esac
