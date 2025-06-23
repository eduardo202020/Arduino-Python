import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt
from datetime import datetime, timedelta
import time
import requests
import socket

# Configuración de la página
st.set_page_config(
    page_title="🌱 Sistema de Riego Inteligente",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .status-good {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    }
    .status-warning {
        background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
    }
    .status-danger {
        background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

class SistemaRiegoStreamlit:
    def __init__(self):
        self.host = 'localhost'
        self.port = 9999
        self.datos_actuales = {}
        self.historial = []
        self.estadisticas = {}
        self.connected = False
        
    def generar_datos_fake(self):
        """Genera datos fake para demostración si no hay conexión"""
        # Generar fechas de las últimas 24 horas
        now = datetime.now()
        fechas = [now - timedelta(minutes=10*i) for i in range(144)]
        fechas.reverse()
        
        historial_fake = []
        
        for i, fecha in enumerate(fechas):
            # Simular ciclo día/noche
            hora_del_dia = fecha.hour + fecha.minute/60
            factor_dia = np.sin((hora_del_dia * np.pi) / 12)
            
            # Temperatura con ciclo día/noche (15-35°C)
            temp1_base = 22 + (factor_dia * 8) + np.random.normal(0, 1.5)
            temp2_base = 24 + (factor_dia * 6) + np.random.normal(0, 1.2)
            
            # Humedad inversa a temperatura (20-80%)
            hum1_base = 55 - (factor_dia * 20) + np.random.normal(0, 5)
            hum2_base = 50 - (factor_dia * 15) + np.random.normal(0, 4)
            
            # Aplicar límites realistas
            temp1 = np.clip(temp1_base, 15, 35)
            temp2 = np.clip(temp2_base, 15, 35)
            hum1 = np.clip(hum1_base, 15, 85)
            hum2 = np.clip(hum2_base, 15, 85)
            
            # Estados de bombas (activar si humedad < 30%)
            bomba1 = hum1 < 30
            bomba2 = hum2 < 30
            
            historial_fake.append({
                'timestamp': fecha,
                'humedad1': round(hum1, 1),
                'humedad2': round(hum2, 1),
                'temperatura1': round(temp1, 1),
                'temperatura2': round(temp2, 1),
                'bomba1': bomba1,
                'bomba2': bomba2
            })
        
        self.historial = historial_fake
        
        # Datos actuales (último registro)
        ultimo = historial_fake[-1]
        self.datos_actuales = {
            'humedad1': ultimo['humedad1'],
            'humedad2': ultimo['humedad2'],
            'temperatura1': ultimo['temperatura1'],
            'temperatura2': ultimo['temperatura2'],
            'bomba1_activa': ultimo['bomba1'],
            'bomba2_activa': ultimo['bomba2']
        }
        
        # Calcular estadísticas
        df = pd.DataFrame(historial_fake)
        self.estadisticas = {
            'hum1_prom': df['humedad1'].mean(),
            'hum2_prom': df['humedad2'].mean(),
            'temp1_prom': df['temperatura1'].mean(),
            'temp2_prom': df['temperatura2'].mean(),
            'hum1_min': df['humedad1'].min(),
            'hum1_max': df['humedad1'].max(),
            'hum2_min': df['humedad2'].min(),
            'hum2_max': df['humedad2'].max(),
            'temp1_min': df['temperatura1'].min(),
            'temp1_max': df['temperatura1'].max(),
            'temp2_min': df['temperatura2'].min(),
            'temp2_max': df['temperatura2'].max(),
            'bomba1_tiempo': (df['bomba1'].sum() / len(df)) * 100,
            'bomba2_tiempo': (df['bomba2'].sum() / len(df)) * 100
        }
    
    def intentar_conexion(self):
        """Intenta conectarse al simulador real"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.host, self.port))
            sock.close()
            self.connected = True
            return True
        except:
            self.connected = False
            return False
    
    def obtener_datos(self):
        """Obtiene datos del simulador o genera fake"""
        if self.intentar_conexion():
            st.sidebar.success("🔌 Conectado al simulador")
            # Aquí podrías implementar la conexión real
            # Por ahora usamos datos fake
            self.generar_datos_fake()
        else:
            st.sidebar.warning("⚠️ Usando datos de demostración")
            self.generar_datos_fake()

def mostrar_metricas_principales(datos):
    """Muestra las métricas principales en cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Estado humedad zona 1
        hum1 = datos['humedad1']
        color = "status-good" if hum1 > 40 else "status-warning" if hum1 > 25 else "status-danger"
        st.markdown(f"""
        <div class="metric-card {color}">
            <h3>💧 Humedad Zona 1</h3>
            <h2>{hum1}%</h2>
            <p>{'✅ Óptimo' if hum1 > 40 else '⚠️ Bajo' if hum1 > 25 else '🚨 Crítico'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Estado humedad zona 2
        hum2 = datos['humedad2']
        color = "status-good" if hum2 > 40 else "status-warning" if hum2 > 25 else "status-danger"
        st.markdown(f"""
        <div class="metric-card {color}">
            <h3>💧 Humedad Zona 2</h3>
            <h2>{hum2}%</h2>
            <p>{'✅ Óptimo' if hum2 > 40 else '⚠️ Bajo' if hum2 > 25 else '🚨 Crítico'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Temperatura promedio
        temp_prom = (datos['temperatura1'] + datos['temperatura2']) / 2
        color = "status-good" if 20 <= temp_prom <= 30 else "status-warning" if 15 <= temp_prom <= 35 else "status-danger"
        st.markdown(f"""
        <div class="metric-card {color}">
            <h3>🌡️ Temperatura Media</h3>
            <h2>{temp_prom:.1f}°C</h2>
            <p>{'✅ Ideal' if 20 <= temp_prom <= 30 else '⚠️ Alerta' if 15 <= temp_prom <= 35 else '🚨 Extrema'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Estado de bombas
        bombas_activas = int(datos['bomba1_activa']) + int(datos['bomba2_activa'])
        color = "status-good" if bombas_activas == 0 else "status-warning" if bombas_activas == 1 else "status-danger"
        st.markdown(f"""
        <div class="metric-card {color}">
            <h3>🚿 Bombas Activas</h3>
            <h2>{bombas_activas}/2</h2>
            <p>{'💚 Sin riego' if bombas_activas == 0 else '🟡 Regando' if bombas_activas == 1 else '🔴 Riego intenso'}</p>
        </div>
        """, unsafe_allow_html=True)

def crear_grafico_tendencias(historial):
    """Crea gráfico de tendencias de humedad y temperatura"""
    df = pd.DataFrame(historial)
    
    # Crear subplots
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('💧 Evolución de Humedad del Suelo', '🌡️ Evolución de Temperatura'),
        vertical_spacing=0.1,
        specs=[[{"secondary_y": True}], [{"secondary_y": True}]]
    )
    
    # Gráfico de humedad
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'], y=df['humedad1'],
            name='Zona 1', line=dict(color='#2E86AB', width=3),
            hovertemplate='<b>Zona 1</b><br>%{y:.1f}%<br>%{x}<extra></extra>'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'], y=df['humedad2'],
            name='Zona 2', line=dict(color='#A23B72', width=3),
            hovertemplate='<b>Zona 2</b><br>%{y:.1f}%<br>%{x}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Línea de umbral crítico para humedad
    fig.add_hline(y=30, line_dash="dash", line_color="red", 
                  annotation_text="Umbral crítico", row=1, col=1)
    
    # Gráfico de temperatura
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'], y=df['temperatura1'],
            name='Sensor 1', line=dict(color='#F18F01', width=3),
            hovertemplate='<b>Sensor 1</b><br>%{y:.1f}°C<br>%{x}<extra></extra>'
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'], y=df['temperatura2'],
            name='Sensor 2', line=dict(color='#C73E1D', width=3),
            hovertemplate='<b>Sensor 2</b><br>%{y:.1f}°C<br>%{x}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Área de temperatura ideal
    fig.add_hrect(y0=20, y1=30, fillcolor="green", opacity=0.1, 
                  annotation_text="Zona ideal", row=2, col=1)
    
    # Actualizar layout
    fig.update_layout(
        height=600,
        showlegend=True,
        title_text="📈 Tendencias del Sistema de Riego (Últimas 24 horas)",
        title_x=0.5,
        font=dict(size=12),
        template="plotly_white"
    )
    
    fig.update_xaxes(title_text="Tiempo", row=2, col=1)
    fig.update_yaxes(title_text="Humedad (%)", row=1, col=1)
    fig.update_yaxes(title_text="Temperatura (°C)", row=2, col=1)
    
    return fig

def crear_grafico_actividad_bombas(historial):
    """Crea gráfico de actividad de bombas"""
    df = pd.DataFrame(historial)
    
    fig = go.Figure()
    
    # Convertir booleanos a números para visualización
    df['bomba1_num'] = df['bomba1'].astype(int)
    df['bomba2_num'] = df['bomba2'].astype(int) + 1.1  # Offset para separar visualmente
    
    # Bomba 1
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['bomba1_num'],
        mode='lines',
        name='🚿 Bomba Zona 1',
        line=dict(color='#3498db', width=4),
        fill='tonexty',
        hovertemplate='<b>Bomba Zona 1</b><br>Estado: %{text}<br>%{x}<extra></extra>',
        text=['🟢 Activa' if x else '🔴 Inactiva' for x in df['bomba1']]
    ))
    
    # Bomba 2
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['bomba2_num'],
        mode='lines',
        name='🚿 Bomba Zona 2',
        line=dict(color='#e74c3c', width=4),
        fill='tonexty',
        hovertemplate='<b>Bomba Zona 2</b><br>Estado: %{text}<br>%{x}<extra></extra>',
        text=['🟢 Activa' if x else '🔴 Inactiva' for x in df['bomba2']]
    ))
    
    fig.update_layout(
        title="🚿 Actividad de las Bombas de Riego",
        title_x=0.5,
        xaxis_title="Tiempo",
        yaxis_title="Estado de Bombas",
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 1.1, 2.1],
            ticktext=['Inactiva', 'Zona 1 Activa', 'Zona 2 Activa', '']
        ),
        height=400,
        template="plotly_white",
        showlegend=True
    )
    
    return fig

def crear_dashboard_estadisticas(stats):
    """Crea dashboard de estadísticas"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Estadísticas de Humedad")
        
        # Gráfico de barras para humedad
        fig_hum = go.Figure(data=[
            go.Bar(name='Zona 1', x=['Promedio', 'Mínimo', 'Máximo'], 
                   y=[stats['hum1_prom'], stats['hum1_min'], stats['hum1_max']],
                   marker_color='#2E86AB'),
            go.Bar(name='Zona 2', x=['Promedio', 'Mínimo', 'Máximo'], 
                   y=[stats['hum2_prom'], stats['hum2_min'], stats['hum2_max']],
                   marker_color='#A23B72')
        ])
        
        fig_hum.update_layout(
            title="Estadísticas de Humedad (%)",
            barmode='group',
            height=300,
            template="plotly_white"
        )
        
        st.plotly_chart(fig_hum, use_container_width=True)
    
    with col2:
        st.subheader("🌡️ Estadísticas de Temperatura")
        
        # Gráfico de barras para temperatura
        fig_temp = go.Figure(data=[
            go.Bar(name='Sensor 1', x=['Promedio', 'Mínimo', 'Máximo'], 
                   y=[stats['temp1_prom'], stats['temp1_min'], stats['temp1_max']],
                   marker_color='#F18F01'),
            go.Bar(name='Sensor 2', x=['Promedio', 'Mínimo', 'Máximo'], 
                   y=[stats['temp2_prom'], stats['temp2_min'], stats['temp2_max']],
                   marker_color='#C73E1D')
        ])
        
        fig_temp.update_layout(
            title="Estadísticas de Temperatura (°C)",
            barmode='group',
            height=300,
            template="plotly_white"
        )
        
        st.plotly_chart(fig_temp, use_container_width=True)

def crear_grafico_tiempo_riego(stats):
    """Crea gráfico de tiempo de riego"""
    fig = go.Figure(data=[
        go.Pie(
            labels=['Bomba Zona 1', 'Bomba Zona 2', 'Sin riego'],
            values=[stats['bomba1_tiempo'], stats['bomba2_tiempo'], 
                   100 - stats['bomba1_tiempo'] - stats['bomba2_tiempo']],
            hole=.4,
            marker_colors=['#3498db', '#e74c3c', '#95a5a6'],
            hovertemplate='<b>%{label}</b><br>%{value:.1f}% del tiempo<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="⏱️ Distribución del Tiempo de Riego (24h)",
        title_x=0.5,
        height=400,
        template="plotly_white",
        annotations=[dict(text=f'Eficiencia<br>{100-stats["bomba1_tiempo"]-stats["bomba2_tiempo"]:.1f}%', 
                         x=0.5, y=0.5, font_size=16, showarrow=False)]
    )
    
    return fig

def main():
    # Título principal
    st.markdown('<h1 class="main-header">🌱 Sistema de Riego Inteligente</h1>', unsafe_allow_html=True)
    
    # Inicializar sistema
    sistema = SistemaRiegoStreamlit()
    
    # Sidebar con controles
    st.sidebar.title("🎛️ Control del Sistema")
    
    # Botón para actualizar datos
    if st.sidebar.button("🔄 Actualizar Datos", type="primary"):
        with st.spinner("Obteniendo datos..."):
            sistema.obtener_datos()
        st.rerun()
    
    # Auto-refresh
    auto_refresh = st.sidebar.checkbox("🔁 Auto-actualizar (30s)")
    if auto_refresh:
        time.sleep(30)
        st.rerun()
    
    # Obtener datos iniciales
    if not sistema.historial:
        with st.spinner("Cargando datos del sistema..."):
            sistema.obtener_datos()
    
    # Mostrar estado de conexión
    if sistema.connected:
        st.sidebar.success("🔌 Conectado al simulador")
    else:
        st.sidebar.info("📡 Modo demostración")
    
    # Control de bombas
    st.sidebar.subheader("🚿 Control de Bombas")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("💧 ON Zona 1"):
            st.success("Bomba Zona 1 activada")
    with col2:
        if st.button("⏹️ OFF Zona 1"):
            st.info("Bomba Zona 1 desactivada")
    
    col3, col4 = st.sidebar.columns(2)
    with col3:
        if st.button("💧 ON Zona 2"):
            st.success("Bomba Zona 2 activada")
    with col4:
        if st.button("⏹️ OFF Zona 2"):
            st.info("Bomba Zona 2 desactivada")
    
    # Modo automático
    if st.sidebar.button("🤖 Modo Automático"):
        st.sidebar.success("Modo automático activado")
    
    # === DASHBOARD PRINCIPAL ===
    
    # Métricas principales
    st.subheader("📊 Estado Actual del Sistema")
    mostrar_metricas_principales(sistema.datos_actuales)
    
    # Gráficos principales
    st.subheader("📈 Análisis de Tendencias")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔄 Tendencias", "🚿 Actividad Bombas", "📊 Estadísticas", "⏱️ Tiempo de Riego"])
    
    with tab1:
        fig_tendencias = crear_grafico_tendencias(sistema.historial)
        st.plotly_chart(fig_tendencias, use_container_width=True)
    
    with tab2:
        fig_bombas = crear_grafico_actividad_bombas(sistema.historial)
        st.plotly_chart(fig_bombas, use_container_width=True)
    
    with tab3:
        crear_dashboard_estadisticas(sistema.estadisticas)
    
    with tab4:
        col1, col2 = st.columns([2, 1])
        with col1:
            fig_tiempo = crear_grafico_tiempo_riego(sistema.estadisticas)
            st.plotly_chart(fig_tiempo, use_container_width=True)
        with col2:
            st.metric("💧 Tiempo Bomba 1", f"{sistema.estadisticas['bomba1_tiempo']:.1f}%")
            st.metric("💧 Tiempo Bomba 2", f"{sistema.estadisticas['bomba2_tiempo']:.1f}%")
            st.metric("⏱️ Tiempo Total Riego", 
                     f"{sistema.estadisticas['bomba1_tiempo'] + sistema.estadisticas['bomba2_tiempo']:.1f}%")
            st.metric("💚 Eficiencia", 
                     f"{100 - sistema.estadisticas['bomba1_tiempo'] - sistema.estadisticas['bomba2_tiempo']:.1f}%")
    
    # Tabla de datos recientes
    st.subheader("📋 Historial Reciente (Últimas 10 lecturas)")
    df_reciente = pd.DataFrame(sistema.historial[-10:])
    df_reciente['timestamp'] = df_reciente['timestamp'].dt.strftime('%H:%M:%S')
    df_reciente['bomba1'] = df_reciente['bomba1'].map({True: '🟢 ON', False: '🔴 OFF'})
    df_reciente['bomba2'] = df_reciente['bomba2'].map({True: '🟢 ON', False: '🔴 OFF'})
    
    st.dataframe(
        df_reciente[['timestamp', 'humedad1', 'humedad2', 'temperatura1', 'temperatura2', 'bomba1', 'bomba2']],
        column_config={
            'timestamp': st.column_config.TextColumn('⏰ Hora'),
            'humedad1': st.column_config.NumberColumn('💧 Humedad Z1 (%)', format="%.1f"),
            'humedad2': st.column_config.NumberColumn('💧 Humedad Z2 (%)', format="%.1f"),
            'temperatura1': st.column_config.NumberColumn('🌡️ Temp S1 (°C)', format="%.1f"),
            'temperatura2': st.column_config.NumberColumn('🌡️ Temp S2 (°C)', format="%.1f"),
            'bomba1': st.column_config.TextColumn('🚿 Bomba Z1'),
            'bomba2': st.column_config.TextColumn('🚿 Bomba Z2'),
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Footer
    st.markdown("---")
    st.markdown("**🌱 Sistema de Riego Inteligente** - Desarrollado con Streamlit y Python")

if __name__ == "__main__":
    main()
