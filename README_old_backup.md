# 🌱 Sistema de Riego Inteligente Arduino-Python

Sistema completo de riego automatizado con sensores, historial de datos y **dashboard web profesional con Streamlit**.

## 📁 Archivos del Proyecto

```
📦 Arduino-Python/
├── 🤖 sistema_riego.ino          # Código Arduino completo
├── 🔧 simulador_corregido.py     # Simulador backend (puerto 9999)
├── 📊 controlador_corregido.py   # Dashboard terminal interactivo
├── 🌐 dashboard_streamlit.py     # Dashboard web profesional
├── 🎮 simulacion_3d_web.py       # Simulación 3D interactiva (Plotly)
├── � simulacion_3d.py           # Simulación 3D científica (Matplotlib)
├── 🗺️  simulacion_3d_ascii.py    # Simulación 3D en terminal (ASCII)
├── �📋 requirements.txt           # Dependencias Python
├── 🚀 run.sh                     # Menú principal de ejecución
├── ⚡ start_dashboard.sh         # Inicio rápido dashboard web
├── 🎯 start_3d.sh               # Inicio rápido simulación 3D
└── 📖 README.md                  # Esta documentación
```

## 🚀 Ejecución Rápida

### **Dashboard Web Profesional (RECOMENDADO):**

```bash
./run.sh
# Elegir opción 3: Dashboard Web Streamlit

# O inicio directo:
./start_dashboard.sh
```

### **Simulación 3D (NUEVA):**

```bash
# Inicio rápido 3D
./start_3d.sh

# O desde el menú principal
./run.sh  # Opciones 7, 8, 9
```

### **Demo Terminal:**

```bash
./run.sh
# Elegir opción 4: Demo completo automático
```

## 🎮 Simulaciones 3D

### **🗺️ ASCII 3D (Sin dependencias)**

-  Vista superior del terreno en terminal
-  Campos de temperatura y humedad visualizados
-  Efectos de riego en tiempo real
-  Gráficos de tendencias ASCII

### **🌐 Web 3D Interactiva (Plotly)**

-  Visualización 3D en navegador
-  Campos de temperatura y humedad como superficies
-  Jets de agua animados durante riego
-  Interactividad: zoom, rotación, hover
-  Tendencias temporales integradas

### **📊 Científica 3D (Matplotlib)**

-  Visualización científica avanzada
-  Animación en tiempo real
-  Múltiples vistas simultáneas
-  Análisis detallado de campos

## 🔧 Características

### 📊 **Sensores**

-  2 Sensores de humedad del suelo
-  2 Sensores de temperatura ambiente
-  🌿 Sensor de temperatura de la planta
-  🌫️ Sensor de humedad relativa del entorno
-  Lecturas cada 2 segundos con variaciones realistas

### 💧 **Control de Riego**

-  2 Bombas/válvulas independientes
-  Control automático basado en umbrales
-  Control manual desde dashboard
-  LED indicador de estado

### 📈 **Historial y Análisis**

-  Historial de 144 entradas (24 horas simuladas)
-  Datos cada 10 minutos con ciclos día/noche
-  Estadísticas detalladas (min, max, promedio)
-  Gráficos de tendencias en texto ASCII

### 🎮 **Dashboard Interactivo**

-  Estado en tiempo real de todos los sensores
-  Visualización de historial completo
-  Gráficos de temperatura y humedad
-  Control manual de bombas
-  Análisis estadístico automático

## 📋 Opciones de Ejecución

### **Opción 1: Demo Automático (Recomendado)**

```bash
./run.sh  # Opción 3
```

Ejecuta simulador y controlador automáticamente.

### **Opción 2: Manual (2 terminales)**

```bash
# Terminal 1:
./run.sh  # Opción 1 (Simulador)

# Terminal 2:
./run.sh  # Opción 2 (Controlador)
```

### **Opción 3: Directo con Python**

```bash
# Terminal 1:
python3 simulador_corregido.py

# Terminal 2:
python3 controlador_corregido.py
```

## 🤖 Uso con Arduino Físico

1. **Subir código al Arduino:**

   ```cpp
   // Usar sistema_riego.ino
   ```

2. **Conexiones de hardware:**

   ```
   Sensores humedad: A0, A1
   Sensores temperatura: A2, A3
   Bombas: pines 2, 3
   LED estado: pin 13
   ```

3. **Modificar controlador:**
   ```python
   # En controlador_corregido.py cambiar:
   # host='localhost', port=9999
   # Por:
   # puerto_serie = '/dev/ttyUSB0'  # Linux
   # puerto_serie = 'COM3'          # Windows
   ```

## 🎯 Funciones del Dashboard

-  **Opción 1**: Actualizar datos
-  **Opción 2**: Modo automático
-  **Opción 3**: Ver estadísticas
-  **Opción 4-7**: Control manual bombas
-  **Opción 9**: Gráfico de humedad
-  **Opción 10**: Gráfico de temperatura
-  **Opción 0**: Salir

## ⚙️ Configuración de Umbrales

```cpp
float UMBRAL_HUMEDAD_MIN = 30.0;  // Activar riego
float UMBRAL_HUMEDAD_MAX = 70.0;  // Desactivar riego
float UMBRAL_TEMP_MAX = 35.0;     // Riego frecuente
```

## 📊 Formato de Datos

### Estado Actual:

```
DATOS:45.2,38.7,24.5,26.1,0,1,23.8,65.2
// humedad1,humedad2,temp1,temp2,bomba1,bomba2,temp_planta,humedad_relativa
```

### Historial:

```
HR:0,45.2,38.7,24.5,26.1,0,1,23.8,65.2
HR:1,46.1,39.2,24.8,26.3,0,0,24.1,63.5
// índice,humedad1,humedad2,temp1,temp2,bomba1,bomba2,temp_planta,humedad_relativa
```

### Estadísticas:

```
STATS:45.5,40.2,25.1,26.3,20.1,70.8,15.3,65.2,18.5,32.1,20.1,30.5,25.2,18.7
// prom_h1,prom_h2,prom_t1,prom_t2,min_h1,max_h1,min_h2,max_h2,min_t1,max_t1,min_t2,max_t2,%bomba1,%bomba2
```

## 🔌 Comunicación

-  **Puerto**: 9999 (TCP socket)
-  **Comandos**: STATUS, HISTORIAL_RECIENTE, ESTADISTICAS, BOMBA1_ON/OFF, BOMBA2_ON/OFF, AUTO
-  **Velocidad serie Arduino**: 921600 baud

## 🧪 Datos de Prueba

El simulador genera automáticamente:

-  ✅ 144 entradas de historial (24 horas)
-  ✅ Ciclos día/noche realistas
-  ✅ Variaciones de temperatura ambiente y de planta
-  ✅ Variaciones de humedad del suelo y relativa del entorno
-  ✅ Estados de bombas basados en umbrales
-  ✅ Timestamps para análisis temporal
-  ✅ Correlación entre sensores (temperatura vs humedad)

---

**Desarrollado por: Jhunior (jguevaral@uni.pe)**  
**Proyecto: Sistema de Riego Inteligente con Arduino y Python**
