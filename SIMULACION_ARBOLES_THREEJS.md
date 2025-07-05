# 🌳 Simulación 3D de 8 Árboles con Three.js - Sistema de Riego Inteligente

## 📖 Descripción

Esta funcionalidad integra una **simulación 3D ultra-realista de 8 árboles** utilizando Three.js en el sistema de riego inteligente. Cada árbol cuenta con su propio termómetro y sistema de riego independiente, proporcionando un ambiente de simulación completo y realista.

## 🌟 Características Principales

### 🌳 8 Árboles Realistas Independientes

-  **8 árboles únicos** con variaciones naturales en tamaño y forma
-  **Troncos detallados** con textura y forma natural
-  **Follaje multicapa** con diferentes tonos de verde
-  **Frutas y flores decorativas** para mayor realismo
-  **Animación de balanceo** influenciada por el viento
-  **Posicionamiento en formación rectangular** para mejor visualización

### 🌡️ Sistema de Sensores (8 TERMÓMETROS)

-  **8 termómetros realistas** ubicados al costado de cada árbol
-  **Lectura visual de temperatura** con líquido que sube/baja
-  **Cambio de color** del termómetro según la temperatura:
   -  🔵 Azul: Temperatura baja (< 20°C)
   -  🟠 Naranja: Temperatura normal (20-30°C)
   -  🔴 Rojo: Temperatura alta (> 35°C)
-  **Actualización en tiempo real** con los controles de temperatura

### 🔧 Sistema de Riego Subterráneo (8 SISTEMAS INDEPENDIENTES)

-  **8 tuberías independientes** para cada árbol que van por el suelo
-  **Red de distribución** con tubería principal y conexiones individuales
-  **8 aspersores emergentes** que salen del suelo cerca de cada árbol
-  **Dispersión realista** del agua en forma de spray desde las tuberías
-  **Control de presión** del agua para ajustar la intensidad del riego

### 🌍 Efectos Ambientales

-  **Sistema de riego con partículas** animadas desde tuberías subterráneas
-  **Iluminación solar ajustable** con sombras dinámicas
-  **Efectos de viento** que afectan el movimiento de los árboles
-  **Cambios de color** del follaje según la salud de la planta

### 🎮 Interactividad Avanzada

-  **Controles independientes** para cada uno de los 8 árboles
-  **Navegación 3D intuitiva** (rotar, zoom, desplazar)
-  **Indicadores de estado visual** en tiempo real para todos los árboles
-  **Ajustes ambientales** (luz solar, viento, presión del agua)
-  **Monitoreo de temperatura visual** con 8 termómetros independientes

## 🚀 Acceso a la Simulación

### **🌐 Dashboard Streamlit Integrado (ÚNICO ACCESO):**

```bash
./run.sh
```

Luego navegar a la pestaña **"🌳 Árboles 3D"** en el dashboard.

**El dashboard incluye:**

-  Integrado en el dashboard profesional
-  Pestaña dedicada "🌳 Árboles 3D"
-  Combina datos del sistema con visualización 3D
-  Acceso a todas las funcionalidades
-  URL: http://localhost:8501

### **📄 Simulación Independiente (Opcional):**

Abrir directamente: `simulacion_arbol_threejs.html` en el navegador

**Características:**

-  Archivo HTML autónomo
-  No requiere servidor web
-  Ideal para pruebas rápidas

## 🎛️ Controles y Funcionalidades

### 🌿 Controles por Árbol (8 ÁRBOLES)

Cada uno de los 8 árboles tiene controles independientes:

| Control            | Función     | Efecto Visual      |
| ------------------ | ----------- | ------------------ |
| 🌡️ **Temperatura** | 15°C - 40°C | Color del follaje  |
| 💧 **Humedad**     | 0% - 100%   | Salud general      |
| 🚿 **Riego**       | ON/OFF      | Partículas de agua |

**Árboles disponibles:** Árbol 1 a Árbol 8, cada uno con parámetros independientes.

### 🌍 Controles Ambientales

| Control          | Función   | Efecto Visual             |
| ---------------- | --------- | ------------------------- |
| ☀️ **Luz Solar** | 0.3 - 2.0 | Intensidad de iluminación |
| 🌊 **Viento**    | 0 - 2.0   | Balanceo de árboles       |

### 📊 Indicadores de Estado

| Color           | Estado      | Descripción          |
| --------------- | ----------- | -------------------- |
| 🟢 **Verde**    | Óptimo      | Condiciones ideales  |
| 🟡 **Amarillo** | Advertencia | Revisar parámetros   |
| 🔴 **Rojo**     | Peligro     | Condiciones críticas |
| 🔵 **Azul**     | Regando     | Sistema activo       |

## 🛠️ Implementación Técnica

### Archivos Principales

```
📁 Arduino-Python/
├── 🌳 simulacion_arbol_threejs.html           # Simulación independiente
├── 📊 simulacion_arbol_threejs_streamlit.py   # Componente Streamlit
├── 🌐 dashboard_streamlit.py                  # Dashboard integrado
└── 🚀 run.sh                                  # Script de ejecución
```

### Tecnologías Utilizadas

-  **Three.js** - Motor 3D JavaScript
-  **Streamlit Components** - Integración web
-  **OrbitControls** - Navegación 3D
-  **WebGL** - Renderizado acelerado por GPU

### Estructura del Código Three.js

```javascript
// Principales componentes
- Scene: Escena 3D principal
- Camera: Cámara con controles de órbita
- Renderer: Renderizador WebGL
- Lighting: Sistema de iluminación
- Trees: Grupos de objetos 3D (troncos + follaje)
- Particles: Sistema de partículas de agua
- Controls: Interfaz de usuario
```

## 🎮 Guía de Uso

### 1. Navegación 3D

-  **Rotar**: Arrastra con botón izquierdo
-  **Zoom**: Rueda del ratón
-  **Desplazar**: Arrastra con botón derecho

### 2. Ajuste de Parámetros

1. Modifica **temperatura** y **humedad** con los sliders
2. Activa **riego** para ver partículas de agua
3. Ajusta **luz solar** y **viento** para efectos ambientales

### 3. Observación de Efectos

-  **Salud del árbol**: Color del follaje cambia según condiciones
-  **Riego activo**: Partículas azules caen del cielo
-  **Viento**: Árboles se balancean suavemente
-  **Temperatura extrema**: Follaje amarillento o rojizo

## 📈 Beneficios vs. Simulación Anterior

| Aspecto            | Simulación Plotly       | Simulación Three.js         |
| ------------------ | ----------------------- | --------------------------- |
| **Realismo**       | Superficies matemáticas | Árboles 3D realistas        |
| **Animación**      | Estática                | Dinámica con efectos        |
| **Interactividad** | Básica                  | Avanzada con navegación     |
| **Efectos**        | Limitados               | Partículas, sombras, viento |
| **Inmersión**      | Moderada                | Alta                        |

## 🔧 Solución de Problemas

### ❌ Error: Archivo no encontrado

```bash
# El archivo HTML no existe
python3 simulacion_arbol_threejs_streamlit.py
```

### 🌐 Navegador no abre automáticamente

```bash
# Abrir manualmente
# Windows: start simulacion_arbol_threejs.html
# macOS: open simulacion_arbol_threejs.html
# Linux: xdg-open simulacion_arbol_threejs.html
```

### 📊 Problemas con Streamlit

```bash
# Verificar instalación
pip install streamlit
streamlit run dashboard_streamlit.py
```

## 🆕 Últimas Mejoras Implementadas

### 🌡️ Termómetros Avanzados

-  **Ubicación**: Posicionados al costado derecho de cada árbol
-  **Componentes realistas**:
   -  Poste de soporte metálico
   -  Caja del termómetro con escala graduada
   -  Tubo de mercurio/líquido variable
   -  Bulbo rojo en la base
   -  Etiqueta digital de lectura
-  **Funcionalidad**:
   -  El líquido sube y baja según la temperatura configurada
   -  Cambio de color automático por rangos de temperatura
   -  Actualización visual en tiempo real
   -  Sombras y efectos de iluminación

### 🔧 Sistema de Tuberías Subterráneas

-  **Arquitectura del sistema**:
   -  Tubería principal horizontal subterránea (profundidad -1.5m)
   -  Conexiones individuales para cada árbol
   -  Tuberías secundarias específicas por árbol (-1.2m de profundidad)
   -  Conexiones verticales que emergen cerca de los árboles
-  **Aspersores emergentes**:
   -  Base cilíndrica que sale del suelo
   -  Cabezal esférico con múltiples boquillas direccionales
   -  8 boquillas de aspersión orientadas en círculo
   -  Inclinación optimizada para cobertura máxima

### 💧 Dispersión de Agua Mejorada

-  **Características del spray**:
   -  Partículas generadas desde cada boquilla del aspersor
   -  Trayectorias realistas con física de gravedad
   -  Velocidad y dirección influenciadas por la presión del agua
   -  Efectos de transparencia y degradado
-  **Control de presión**:
   -  Slider para ajustar la intensidad del riego (0.5x - 2.0x)
   -  Afecta la velocidad y alcance de las partículas
   -  Cambio visual inmediato al ajustar el control

### 🎮 Controles Mejorados

-  **Nuevos controles agregados**:
   -  💦 **Presión del Agua**: Control deslizante para intensidad de riego
   -  🌡️ **Monitoreo Visual**: Los termómetros reflejan cambios instantáneos
   -  📊 **Estado Ambiental**: Información de viento y luz solar
-  **Interactividad mejorada**:
   -  Respuesta visual inmediata a todos los cambios
   -  Sincronización entre controles y efectos visuales
   -  Indicadores de estado más precisos

## 🆕 Actualización: Expansión a 8 Árboles ✨

### 🎯 Resumen de la Mejora

La simulación ha sido **completamente expandida** para soportar **8 árboles independientes**, cada uno con su propio sistema completo:

#### ✅ Características Implementadas:

-  **8 árboles 3D únicos** con variaciones naturales
-  **8 termómetros independientes** con lectura visual en tiempo real
-  **8 sistemas de riego subterráneo** con tuberías individuales
-  **8 aspersores emergentes** con dispersión realista de agua
-  **Controles independientes** para cada árbol (temperatura, humedad, riego)
-  **Indicadores de estado visual** para monitoreo en tiempo real
-  **Distribución espacial optimizada** en formación rectangular

#### 🔧 Mejoras Técnicas:

-  **Arrays dinámicos** para manejar múltiples árboles eficientemente
-  **Sistema de partículas escalable** para efectos de agua
-  **Lógica de eventos optimizada** para 8 conjuntos de controles
-  **Interfaz responsive** que se adapta a múltiples elementos
-  **Código modular** fácil de mantener y expandir

#### 🎮 Controles Actualizados:

-  **24 controles individuales** (3 por árbol: temperatura, humedad, riego)
-  **8 indicadores de estado** con código de colores
-  **3 controles ambientales** globales (viento, luz solar, presión)
-  **Información de salud** en tiempo real para todos los árboles

---

## 🚀 Futuras Mejoras

### 🌟 Características Planificadas

-  **Múltiples tipos de plantas** (cactus, flores, verduras)
-  **Estaciones del año** con cambios visuales
-  **Efectos climáticos** (lluvia, sol, nubosidad)
-  **Análisis predictivo** con IA
-  **Realidad aumentada** para móviles

### 🔌 Integración con Hardware

-  **Sensores IoT** para datos en tiempo real
-  **Control remoto** de sistemas de riego
-  **Alertas push** en dispositivos móviles
-  **Análisis de imágenes** para salud de plantas

## 📞 Soporte

Para problemas o sugerencias:

1. Verificar que todos los archivos estén presentes
2. Comprobar instalación de dependencias
3. Revisar logs de error en terminal
4. Probar diferentes navegadores (Chrome recomendado)

---

**🌱 Sistema de Riego Inteligente - Simulación 3D con Three.js**  
_Desarrollado para visualización realista y control avanzado_
