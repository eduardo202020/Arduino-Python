# 🌱 Sistema de Riego Inteligente Arduino-Python - Versión Profesional

Sistema completo de riego automatizado con **Dashboard Web Streamlit** que integra todas las funcionalidades: monitoreo en tiempo real, simulaciones 3D interactivas, y control avanzado de riego.

## 📁 Estructura del Proyecto (Optimizada)

```
📦 Arduino-Python/
├── 🌐 dashboard_streamlit.py              # Dashboard principal con todas las funcionalidades
├── 🌳 simulacion_arbol_threejs.html       # Simulación 3D independiente
├── 📊 simulacion_arbol_threejs_streamlit.py # Componente Three.js para Streamlit
├── 🤖 sistema_riego.ino                   # Código Arduino completo
├── 🔧 simulador_corregido.py              # Backend de datos (opcional)
├── 📊 controlador_corregido.py            # Controlador de respaldo (opcional)
├── 📋 requirements.txt                    # Dependencias Python
├── 🚀 run.sh                              # Script único de ejecución
├── 📖 README.md                           # Esta documentación
├── 📄 SIMULACION_ARBOLES_THREEJS.md       # Documentación específica Three.js
├── 🗂️ .streamlit/                        # Configuración Streamlit
└── 🗃️ .git/                              # Control de versiones
```

## ⚡ Ejecución Simplificada

### **🌐 Dashboard Web Profesional (ÚNICO PUNTO DE ENTRADA):**

```bash
./run.sh
```

**El Dashboard incluye TODO:**

-  📊 **Métricas en tiempo real** con gráficos interactivos
-  🎮 **Simulación 3D con Plotly** integrada
-  🌳 **Simulación 3D de Árboles con Three.js** ultra-realista
-  🌡️ **Termómetros visuales** en cada árbol
-  🔧 **Sistema de tuberías subterráneas** con dispersión de agua
-  🎛️ **Controles completos** de temperatura, humedad y riego
-  📈 **Análisis automático** de salud de plantas

### **📱 Acceso:**

-  **URL:** http://localhost:8501
-  **Pestañas disponibles:**
   -  📊 **Dashboard Principal** - Métricas y gráficos
   -  🎮 **Simulación 3D** - Visualización Plotly
   -  🌳 **Árboles 3D** - Simulación Three.js realista

## 🎯 Características Principales

### 🌳 Simulación 3D Ultra-Realista

-  **Árboles detallados** con troncos, follaje multicapa y frutas
-  **Termómetros realistas** al lado de cada árbol
-  **Sistema de tuberías subterráneas** individuales
-  **Dispersión de agua** desde aspersores emergentes
-  **Efectos ambientales** (viento, luz solar, sombras)
-  **Navegación 3D completa** (rotar, zoom, desplazar)

### 📊 Dashboard Integrado

-  **Gráficos interactivos** en tiempo real con Plotly
-  **Métricas de sensores** (temperatura, humedad del suelo)
-  **Control de riego** automático y manual
-  **Historial de datos** con análisis temporal
-  **Indicadores de salud** de las plantas

### 🎛️ Control Avanzado

-  **Ajustes independientes** por árbol
-  **Control de presión** del agua (0.5x - 2.0x)
-  **Monitoreo visual** de temperatura con termómetros
-  **Estados visuales** con códigos de color
-  **Alertas automáticas** de condiciones críticas

## 🔧 Instalación y Configuración

### Prerequisitos

```bash
# Python 3.7 o superior
python3 --version

# Git (para clonar el repositorio)
git --version
```

### Instalación Automática

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/Arduino-Python.git
cd Arduino-Python

# Ejecutar (instala dependencias automáticamente)
./run.sh
```

### Instalación Manual

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar dashboard
streamlit run dashboard_streamlit.py
```

## 🤖 Configuración Arduino (Opcional)

### Hardware Requerido

-  **Arduino Uno/Nano** (o compatible)
-  **2x Sensores de humedad del suelo** (YL-69 o similar)
-  **2x Sensores de temperatura** (DS18B20 o DHT22)
-  **2x Relés o válvulas** para control de riego
-  **Bomba de agua** (5V o 12V)
-  **Protoboard y cables** de conexión

### Carga del Código

```bash
# 1. Abrir Arduino IDE
# 2. Cargar archivo: sistema_riego.ino
# 3. Seleccionar puerto serie
# 4. Subir al Arduino
```

### Conexiones

```
Arduino Uno:
├── A0 → Sensor humedad suelo 1
├── A1 → Sensor humedad suelo 2
├── D2 → Sensor temperatura 1
├── D3 → Sensor temperatura 2
├── D7 → Relé bomba 1
├── D8 → Relé bomba 2
└── GND/5V → Alimentación sensores
```

## 🎮 Guía de Uso

### 1. Iniciar el Sistema

```bash
cd Arduino-Python
./run.sh
```

### 2. Acceder al Dashboard

-  Abre automáticamente: http://localhost:8501
-  O manualmente en cualquier navegador

### 3. Navegar por las Pestañas

#### 📊 Dashboard Principal

-  **Métricas actuales** de temperatura y humedad
-  **Gráficos históricos** de los últimos datos
-  **Controles de riego** manual
-  **Estados de salud** de las plantas

#### 🎮 Simulación 3D (Plotly)

-  **Vista 3D interactiva** del campo de riego
-  **Campos de temperatura** visualizados como superficies
-  **Efectos de riego** en tiempo real
-  **Navegación libre** en 3D

#### 🌳 Árboles 3D (Three.js)

-  **Árboles ultra-realistas** con detalles
-  **Termómetros funcionales** al lado de cada árbol
-  **Tuberías subterráneas** con aspersores
-  **Control individual** de cada árbol
-  **Efectos ambientales** avanzados

### 4. Controles Disponibles

#### Por Árbol:

-  🌡️ **Temperatura:** 15°C - 40°C
-  💧 **Humedad:** 0% - 100%
-  🚿 **Riego:** Activar/Desactivar

#### Ambientales:

-  ☀️ **Luz Solar:** Intensidad 0% - 100%
-  🌪️ **Viento:** Velocidad 0 - 10
-  💦 **Presión Agua:** 0.5x - 2.0x

## 📈 Análisis y Métricas

### Indicadores de Salud

| Color       | Estado      | Acción Recomendada   |
| ----------- | ----------- | -------------------- |
| 🟢 Verde    | Óptimo      | Mantener condiciones |
| 🟡 Amarillo | Advertencia | Revisar parámetros   |
| 🔴 Rojo     | Crítico     | Acción inmediata     |
| 🔵 Azul     | Regando     | Sistema activo       |

### Parámetros Óptimos

-  **Temperatura:** 18°C - 28°C
-  **Humedad del suelo:** 40% - 70%
-  **Frecuencia de riego:** Según sensor
-  **Duración de riego:** 5-15 segundos

## 🔧 Solución de Problemas

### Error: "Module not found"

```bash
pip install -r requirements.txt
```

### Puerto ocupado (8501)

```bash
# Cambiar puerto manualmente
streamlit run dashboard_streamlit.py --server.port 8502
```

### Simulación 3D no carga

```bash
# Verificar navegador (Chrome recomendado)
# Verificar conexión a internet (Three.js CDN)
```

### Arduino no conecta

```bash
# Verificar puerto serie
# Comprobar drivers USB
# Reiniciar Arduino IDE
```

## 🚀 Próximas Mejoras

### 🌟 Funcionalidades Planificadas

-  **App móvil** con notificaciones push
-  **Machine Learning** para predicción de riego
-  **Integración IoT** con sensores inalámbricos
-  **Análisis de imágenes** para detección de plagas
-  **Sistema multi-zona** para grandes cultivos

### 🔌 Integraciones

-  **Home Assistant** para domótica
-  **Google Assistant / Alexa** para control por voz
-  **Telegram Bot** para notificaciones
-  **Base de datos en la nube** para históricos

## 📞 Soporte y Contribución

### 🐛 Reportar Problemas

-  Crear issue en GitHub con detalles del error
-  Incluir logs de terminal y navegador
-  Especificar sistema operativo y versión Python

### 🤝 Contribuir

-  Fork del repositorio
-  Crear rama para nueva funcionalidad
-  Enviar Pull Request con descripción detallada

### 📧 Contacto

-  **GitHub:** [Tu usuario]
-  **Email:** [tu-email@ejemplo.com]

---

**🌱 Sistema de Riego Inteligente - Versión Profesional**  
_Dashboard Web completo con simulaciones 3D ultra-realistas_
