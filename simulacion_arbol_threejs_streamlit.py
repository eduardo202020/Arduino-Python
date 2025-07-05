import streamlit as st
import streamlit.components.v1 as components
import os

def crear_simulacion_arbol_threejs():
    """
    Crea una simulación 3D de árboles realistas usando Three.js
    integrada en Streamlit como componente personalizado.
    """
    
    st.subheader("🌳 Simulación 3D de 8 Árboles Realistas")
    st.write("Visualización avanzada con Three.js - 8 árboles independientes con efectos ambientales")
    
    # Cargar el archivo HTML de Three.js
    html_file_path = "simulacion_arbol_threejs.html"
    
    # Verificar si el archivo existe
    if os.path.exists(html_file_path):
        # Leer el contenido del archivo HTML
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Mostrar el componente HTML en Streamlit
        components.html(html_content, height=800, scrolling=True)
        
        # Información adicional
        with st.expander("ℹ️ Información de la Simulación 3D de 8 Árboles"):
            st.write("""
            **🌳 Características de la Simulación (8 ÁRBOLES):**
            
            **8 Árboles Realistas Independientes:**
            - Troncos únicos con texturas realistas
            - Follaje multicapa con diferentes tonos de verde
            - Frutas y flores decorativas por árbol
            - Animación de balanceo individual por viento
            - Distribución espacial en formación rectangular
            
            **8 Sistemas de Riego Independientes:**
            - Sistema de tuberías subterráneas por árbol
            - Aspersores emergentes individuales
            - Partículas de agua con dispersión realista
            - Control de presión independiente
            
            **8 Termómetros Visuales:**
            - Termómetros realistas al lado de cada árbol
            - Lectura visual con líquido que sube/baja
            - Cambio de color según temperatura
            - Actualización en tiempo real
            
            **Controles Interactivos (24 CONTROLES INDIVIDUALES):**
            - Temperatura independiente para cada árbol (15°C - 40°C)
            - Humedad individual (0% - 100%)
            - Activación/desactivación de riego por árbol
            - Controles ambientales globales (viento, luz solar, presión)
            
            **Indicadores de Salud Avanzados:**
            - Cambio de color del follaje según condiciones de cada árbol
            - Estado visual en tiempo real para los 8 árboles
            - Información de salud detallada por árbol
            - Estados visuales: óptimo, advertencia, peligro, regando
            - Información en tiempo real del estado del sistema
            
            **Controles de Vista:**
            - Intensidad de luz solar
            - Fuerza del viento
            - Rotación libre de cámara
            """)
            
        with st.expander("🎮 Guía de Uso"):
            st.write("""
            **Cómo usar la simulación:**
            
            1. **Ajustar Parámetros:** Usa los sliders para modificar temperatura y humedad de cada árbol
            2. **Activar Riego:** Marca las casillas para ver el efecto del riego con partículas animadas
            3. **Controlar Ambiente:** Ajusta la luz solar y el viento para ver efectos ambientales
            4. **Observar Cambios:** Los árboles cambian de color según su salud
            5. **Navegar en 3D:** Arrastra para rotar, usa scroll para zoom, click derecho para desplazar
            
            **Indicadores de Estado:**
            - 🟢 Verde: Condiciones óptimas
            - 🟡 Amarillo: Advertencia (revisar parámetros)
            - 🔴 Rojo: Condiciones peligrosas
            - 🔵 Azul parpadeante: Sistema de riego activo
            """)
    
    else:
        st.error(f"❌ Error: No se encontró el archivo de simulación {html_file_path}")
        st.write("Por favor, asegúrate de que el archivo `simulacion_arbol_threejs.html` esté en el directorio del proyecto.")

def crear_vista_comparativa():
    """
    Crea una vista comparativa entre la simulación Plotly y Three.js
    """
    st.subheader("📊 Comparación de Tecnologías 3D")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🔹 Simulación Plotly (Actual)**")
        st.write("""
        - ✅ Integración nativa con Streamlit
        - ✅ Gráficos científicos y estadísticos
        - ✅ Superficies matemáticas 3D
        - ⚠️ Visualización menos realista
        - ⚠️ Limitada en animaciones complejas
        """)
    
    with col2:
        st.write("**🔹 Simulación Three.js (Nueva)**")
        st.write("""
        - ✅ Árboles 3D ultra realistas
        - ✅ Animaciones fluidas y efectos
        - ✅ Iluminación avanzada y sombras
        - ✅ Partículas y física en tiempo real
        - ✅ Navegación 3D intuitiva
        """)

if __name__ == "__main__":
    # Configuración de la página
    st.set_page_config(
        page_title="Simulación 3D Árboles - Three.js",
        page_icon="🌳",
        layout="wide"
    )
    
    st.title("🌳 Simulación 3D de Árboles - Three.js Integration")
    
    # Tabs para organizar el contenido
    tab1, tab2 = st.tabs(["🌳 Simulación Realista", "📊 Comparación"])
    
    with tab1:
        crear_simulacion_arbol_threejs()
    
    with tab2:
        crear_vista_comparativa()
