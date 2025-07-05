# 🗂️ OPTIMIZACIÓN DEL PROYECTO - PLAN DE LIMPIEZA

## ✅ ARCHIVOS ESENCIALES A MANTENER

### 🌐 Dashboard Principal

-  dashboard_streamlit.py (ESENCIAL - Dashboard principal)
-  simulacion_arbol_threejs_streamlit.py (ESENCIAL - Componente Three.js)

### 📄 Documentación

-  README.md (ESENCIAL - Documentación principal)
-  requirements.txt (ESENCIAL - Dependencias)
-  SIMULACION_ARBOLES_THREEJS.md (ESENCIAL - Doc Three.js)

### 🌳 Simulación 3D

-  simulacion_arbol_threejs.html (ESENCIAL - Simulación independiente)

### 🔧 Scripts

-  run_simplified.sh (NUEVO - Script simplificado)

### 🗂️ Configuración

-  .streamlit/ (ESENCIAL - Configuración Streamlit)
-  .gitignore (MANTENER)

## ❌ ARCHIVOS A ELIMINAR (REDUNDANTES)

### 🗑️ Scripts obsoletos

-  run.sh (OBSOLETO - Reemplazado por run_simplified.sh)
-  run_broken_backup.sh
-  run_final.sh
-  run_fixed.sh
-  run_new.sh
-  run_new_clean.sh
-  run_old.sh
-  start_3d.sh
-  start_dashboard.sh

### 🗑️ Simuladores obsoletos

-  controlador_corregido.py (REDUNDANTE)
-  controlador_led.py (REDUNDANTE)
-  controlador_riego.py (REDUNDANTE)
-  controlador_riego_avanzado.py (REDUNDANTE)
-  simulador_arduino.py (REDUNDANTE)
-  simulador_corregido.py (REDUNDANTE)
-  simulador_riego.py (REDUNDANTE)
-  simulador_riego_avanzado.py (REDUNDANTE)

### 🗑️ Simulaciones 3D obsoletas

-  simulacion_3d.py (REDUNDANTE - Integrado en Streamlit)
-  simulacion_3d_ascii.py (REDUNDANTE)
-  simulacion_3d_streamlit_demo.py (REDUNDANTE)
-  simulacion_3d_web.py (REDUNDANTE)
-  simulacion_3d_web_corregida.py (REDUNDANTE)
-  simulacion_3d_web_funcional.py (REDUNDANTE)
-  simulacion_3d_web_simple.py (REDUNDANTE)
-  simulacion_arbol_threejs_mejorada.html (REDUNDANTE - Duplicado)

### 🗑️ Tests obsoletos

-  test_3d_fix.py (REDUNDANTE)
-  test_corregido.py (REDUNDANTE)
-  test_mejoras_threejs.sh (REDUNDANTE)
-  test_nuevos_sensores.py (REDUNDANTE)
-  test_quick.sh (REDUNDANTE)
-  test_simple.py (REDUNDANTE)
-  test_threejs.sh (REDUNDANTE)
-  demo_sensores.py (REDUNDANTE)
-  diagnostico.py (REDUNDANTE)

### 🗑️ Documentación obsoleta

-  NUEVOS_SENSORES.md (REDUNDANTE)
-  SIMULACION_3D.md (REDUNDANTE)
-  SIMULACION_3D_STREAMLIT.md (REDUNDANTE)
-  SOLUCION_OPCION_7.md (REDUNDANTE)
-  MEJORAS_IMPLEMENTADAS.md (REDUNDANTE)

### 🗑️ Archivos HTML obsoletos

-  simulacion_riego_3d_funcional.html (REDUNDANTE)
-  simulacion_3d_output/ (DIRECTORIO REDUNDANTE)

## 📊 RESULTADO ESPERADO

### Antes: ~60 archivos

### Después: ~10 archivos esenciales

### 🎯 PROYECTO OPTIMIZADO:

```
📁 Arduino-Python/
├── 🌐 dashboard_streamlit.py          # Dashboard principal
├── 🌳 simulacion_arbol_threejs.html   # Simulación independiente
├── 📊 simulacion_arbol_threejs_streamlit.py # Componente Streamlit
├── 🚀 run_simplified.sh               # Script único
├── 📋 requirements.txt                # Dependencias
├── 📖 README.md                       # Documentación
├── 📄 SIMULACION_ARBOLES_THREEJS.md   # Doc específica
├── 🤖 sistema_riego.ino               # Código Arduino
├── 📁 .streamlit/                     # Configuración
└── 📁 .git/                          # Control de versiones
```

## ✨ BENEFICIOS:

-  🚀 Proyecto más limpio y mantenible
-  📦 Instalación más rápida
-  🎯 Un solo punto de entrada (Dashboard Streamlit)
-  🔧 Menos archivos que mantener
-  📖 Documentación simplificada
