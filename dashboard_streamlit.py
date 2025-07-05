import streamlit as st
import streamlit.components.v1 as components
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
import os

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
            
            # Temperatura de planta (ligeramente menor que ambiente)
            temp_planta_base = temp1_base - 1.5 + np.random.normal(0, 1)
            
            # Humedad inversa a temperatura (20-80%)
            hum1_base = 55 - (factor_dia * 20) + np.random.normal(0, 5)
            hum2_base = 50 - (factor_dia * 15) + np.random.normal(0, 4)
            
            # Humedad relativa del entorno (inversa a temperatura)
            humedad_relativa_base = 85 - (temp1_base - 15) * 2 + np.random.normal(0, 8)
            
            # Aplicar límites realistas
            temp1 = np.clip(temp1_base, 15, 35)
            temp2 = np.clip(temp2_base, 15, 35)
            temp_planta = np.clip(temp_planta_base, 12, 32)
            hum1 = np.clip(hum1_base, 15, 85)
            hum2 = np.clip(hum2_base, 15, 85)
            humedad_relativa = np.clip(humedad_relativa_base, 30, 95)
            
            # Estados de bombas (activar si humedad < 30%)
            bomba1 = hum1 < 30
            bomba2 = hum2 < 30
            
            historial_fake.append({
                'timestamp': fecha,
                'humedad1': round(hum1, 1),
                'humedad2': round(hum2, 1),
                'temperatura1': round(temp1, 1),
                'temperatura2': round(temp2, 1),
                'temp_planta': round(temp_planta, 1),
                'humedad_relativa': round(humedad_relativa, 1),
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
            'temp_planta': ultimo['temp_planta'],
            'humedad_relativa': ultimo['humedad_relativa'],
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
            'temp_planta_prom': df['temp_planta'].mean(),
            'humedad_relativa_prom': df['humedad_relativa'].mean(),
            'hum1_min': df['humedad1'].min(),
            'hum1_max': df['humedad1'].max(),
            'hum2_min': df['humedad2'].min(),
            'hum2_max': df['humedad2'].max(),
            'temp1_min': df['temperatura1'].min(),
            'temp1_max': df['temperatura1'].max(),
            'temp2_min': df['temperatura2'].min(),
            'temp2_max': df['temperatura2'].max(),
            'temp_planta_min': df['temp_planta'].min(),
            'temp_planta_max': df['temp_planta'].max(),
            'humedad_relativa_min': df['humedad_relativa'].min(),
            'humedad_relativa_max': df['humedad_relativa'].max(),
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
    # Primera fila: Sensores de humedad
    col1, col2, col3 = st.columns(3)
    
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
        # Humedad relativa del entorno
        hum_rel = datos.get('humedad_relativa', 0)
        color = "status-good" if 40 <= hum_rel <= 70 else "status-warning" if 30 <= hum_rel <= 80 else "status-danger"
        st.markdown(f"""
        <div class="metric-card {color}">
            <h3>🌫️ Humedad Relativa</h3>
            <h2>{hum_rel}%</h2>
            <p>{'✅ Ideal' if 40 <= hum_rel <= 70 else '⚠️ Moderado' if 30 <= hum_rel <= 80 else '🚨 Extremo'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Segunda fila: Sensores de temperatura y estado
    col4, col5, col6 = st.columns(3)
    
    with col4:
        # Temperatura promedio ambiente
        temp_prom = (datos['temperatura1'] + datos['temperatura2']) / 2
        color = "status-good" if 20 <= temp_prom <= 30 else "status-warning" if 15 <= temp_prom <= 35 else "status-danger"
        st.markdown(f"""
        <div class="metric-card {color}">
            <h3>🌡️ Temp. Ambiente</h3>
            <h2>{temp_prom:.1f}°C</h2>
            <p>{'✅ Ideal' if 20 <= temp_prom <= 30 else '⚠️ Alerta' if 15 <= temp_prom <= 35 else '🚨 Extrema'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        # Temperatura de la planta
        temp_planta = datos.get('temp_planta', 0)
        color = "status-good" if 18 <= temp_planta <= 28 else "status-warning" if 15 <= temp_planta <= 32 else "status-danger"
        st.markdown(f"""
        <div class="metric-card {color}">
            <h3>🌿 Temp. Planta</h3>
            <h2>{temp_planta:.1f}°C</h2>
            <p>{'✅ Óptima' if 18 <= temp_planta <= 28 else '⚠️ Subóptima' if 15 <= temp_planta <= 32 else '🚨 Peligrosa'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
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
    """Crea gráfico de tendencias de humedad y temperatura con todos los sensores"""
    df = pd.DataFrame(historial)
    
    # Crear subplots con 3 filas
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=(
            '💧 Evolución de Humedad del Suelo', 
            '🌡️ Evolución de Temperatura Ambiente',
            '🌿 Sensores Especializados (Planta y Entorno)'
        ),
        vertical_spacing=0.08,
        specs=[[{"secondary_y": True}], [{"secondary_y": True}], [{"secondary_y": True}]]
    )
    
    # Gráfico de humedad del suelo
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
    
    # Gráfico de temperatura ambiente
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
    
    # Gráfico de sensores especializados
    if 'temp_planta' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'], y=df['temp_planta'],
                name='🌿 Temp. Planta', line=dict(color='#228B22', width=3),
                hovertemplate='<b>Temp. Planta</b><br>%{y:.1f}°C<br>%{x}<extra></extra>'
            ),
            row=3, col=1
        )
    
    if 'humedad_relativa' in df.columns:
        # Usar eje secundario para humedad relativa
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'], y=df['humedad_relativa'],
                name='🌫️ Hum. Relativa', line=dict(color='#4169E1', width=3, dash='dot'),
                hovertemplate='<b>Hum. Relativa</b><br>%{y:.1f}%<br>%{x}<extra></extra>',
                yaxis='y2'
            ),
            row=3, col=1
        )
        
        # Configurar eje secundario para la fila 3
        fig.update_yaxes(title_text="Humedad Relativa (%)", secondary_y=True, row=3, col=1)
    
    # Actualizar layout
    fig.update_layout(
        height=800,
        showlegend=True,
        title_text="📈 Tendencias Completas del Sistema de Riego (Últimas 24 horas)",
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

def crear_simulacion_3d_interactiva(temp1, hum1, bomba1, temp2, hum2, bomba2):
    """Crea una simulación 3D interactiva del sistema de riego"""
    
    # Configuración del terreno
    size = 15
    x_range = np.linspace(-2, 5, size)
    y_range = np.linspace(-2, 2, size)
    X, Y = np.meshgrid(x_range, y_range)
    
    # Posiciones de las plantas
    planta1_pos = (0, 0)
    planta2_pos = (3, 0)
    
    # Calcular campo de temperatura
    Z_temp = np.ones_like(X) * 20.0  # Temperatura base
    
    for planta_pos, temp, bomba in [(planta1_pos, temp1, bomba1), (planta2_pos, temp2, bomba2)]:
        px, py = planta_pos
        distancia = np.sqrt((X - px)**2 + (Y - py)**2)
        influencia = np.exp(-distancia / 1.5)
        Z_temp += influencia * (temp - 20)
        
        # Efecto de enfriamiento por riego
        if bomba:
            influencia_riego = np.exp(-distancia / 0.8)
            Z_temp -= influencia_riego * 3
    
    # Calcular campo de humedad
    Z_humedad = np.ones_like(X) * 30.0  # Humedad base
    
    for planta_pos, hum, bomba in [(planta1_pos, hum1, bomba1), (planta2_pos, hum2, bomba2)]:
        px, py = planta_pos
        distancia = np.sqrt((X - px)**2 + (Y - py)**2)
        influencia = np.exp(-distancia / 1.2)
        Z_humedad += influencia * (hum - 30)
        
        # Efecto de aumento de humedad por riego
        if bomba:
            influencia_riego = np.exp(-distancia / 1.0)
            Z_humedad += influencia_riego * 35
    
    Z_humedad = np.clip(Z_humedad, 0, 100)
    
    # Crear subplots
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "surface"}, {"type": "surface"}],
               [{"type": "scatter3d"}, {"type": "scatter"}]],
        subplot_titles=[
            '🌡️ Campo de Temperatura (°C)', 
            '💧 Campo de Humedad (%)', 
            '🌱 Vista Combinada 3D', 
            '📊 Estado Actual'
        ],
        vertical_spacing=0.12
    )
    
    # 1. Superficie de temperatura
    fig.add_trace(
        go.Surface(
            x=X, y=Y, z=Z_temp,
            colorscale='RdYlBu_r',
            showscale=True,
            colorbar=dict(title="°C", x=0.45, len=0.8),
            name="Temperatura"
        ),
        row=1, col=1
    )
    
    # Plantas en superficie de temperatura
    plantas_x = [planta1_pos[0], planta2_pos[0]]
    plantas_y = [planta1_pos[1], planta2_pos[1]]
    plantas_z_temp = [temp1 + 1, temp2 + 1]
    plantas_color_temp = ['red' if bomba1 else 'green', 'red' if bomba2 else 'green']
    plantas_text = ['P1', 'P2']
    
    fig.add_trace(
        go.Scatter3d(
            x=plantas_x, y=plantas_y, z=plantas_z_temp,
            mode='markers+text',
            marker=dict(size=20, color=plantas_color_temp),
            text=plantas_text,
            textposition="middle center",
            showlegend=False,
            name="Plantas"
        ),
        row=1, col=1
    )
    
    # 2. Superficie de humedad
    fig.add_trace(
        go.Surface(
            x=X, y=Y, z=Z_humedad,
            colorscale='Blues',
            showscale=True,
            colorbar=dict(title="%", x=1.02, len=0.8),
            name="Humedad"
        ),
        row=1, col=2
    )
    
    # Plantas en superficie de humedad
    plantas_z_hum = [hum1 + 3, hum2 + 3]
    plantas_color_hum = ['blue' if bomba1 else 'brown', 'blue' if bomba2 else 'brown']
    
    fig.add_trace(
        go.Scatter3d(
            x=plantas_x, y=plantas_y, z=plantas_z_hum,
            mode='markers+text',
            marker=dict(size=20, color=plantas_color_hum),
            text=plantas_text,
            textposition="middle center",
            showlegend=False,
            name="Plantas Humedad"
        ),
        row=1, col=2
    )
    
    # 3. Vista combinada
    # Plantas principales
    fig.add_trace(
        go.Scatter3d(
            x=plantas_x, y=plantas_y, z=[temp1, temp2],
            mode='markers+text',
            marker=dict(
                size=30,
                color=[hum1, hum2],
                colorscale='Viridis',
                colorbar=dict(title="Humedad %", x=0.45, y=0.2, len=0.3)
            ),
            text=['🌱P1', '🌱P2'],
            textposition="middle center",
            showlegend=False,
            name="Plantas Combinado"
        ),
        row=2, col=1
    )
    
    # Jets de riego
    for i, (planta_pos, temp, bomba) in enumerate([(planta1_pos, temp1, bomba1), (planta2_pos, temp2, bomba2)]):
        if bomba:
            px, py = planta_pos
            jet_z = [temp + j*1.5 for j in range(1, 5)]
            fig.add_trace(
                go.Scatter3d(
                    x=[px] * 4, y=[py] * 4, z=jet_z,
                    mode='markers',
                    marker=dict(size=8, color='cyan', opacity=0.7),
                    showlegend=False,
                    name=f"Riego P{i+1}"
                ),
                row=2, col=1
            )
    
    # 4. Gráfico de barras de estado actual
    fig.add_trace(
        go.Bar(
            x=['🌿 Planta 1', '🌿 Planta 2'],
            y=[temp1, temp2],
            name='Temperatura (°C)',
            marker_color=plantas_color_temp,
            text=[f"{temp1:.1f}°C {'🚿' if bomba1 else '🌱'}", 
                  f"{temp2:.1f}°C {'🚿' if bomba2 else '🌱'}"],
            textposition='auto'
        ),
        row=2, col=2
    )
    
    # Humedad como barras secundarias
    fig.add_trace(
        go.Bar(
            x=['💧 Planta 1', '💧 Planta 2'],
            y=[hum1, hum2],
            name='Humedad (%)',
            marker_color=plantas_color_hum,
            text=[f"{hum1:.1f}% {'🚿' if bomba1 else '💧'}", 
                  f"{hum2:.1f}% {'🚿' if bomba2 else '💧'}"],
            textposition='auto',
            yaxis='y2'
        ),
        row=2, col=2
    )
    
    # Configurar layout
    timestamp = datetime.now().strftime("%H:%M:%S")
    fig.update_layout(
        title=dict(
            text=f"🌱 Simulación 3D Interactiva - Sistema de Riego<br>" +
                 f"<sub>Actualizado: {timestamp} | " +
                 f"P1: {'Regando 🚿' if bomba1 else 'Normal 🌱'} | " +
                 f"P2: {'Regando 🚿' if bomba2 else 'Normal 🌱'}</sub>",
            x=0.5
        ),
        height=800,
        showlegend=False
    )
    
    # Configurar escenas 3D
    scene_config = dict(
        xaxis_title="X (metros)",
        yaxis_title="Y (metros)",
        zaxis_title="Valor",
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
    )
    
    fig.update_layout(
        scene=scene_config,
        scene2=scene_config,
        scene3=scene_config
    )
    
    # Configurar eje Y secundario para el gráfico de barras
    fig.update_layout(
        xaxis4=dict(title="Estado de Plantas"),
        yaxis4=dict(title="Temperatura (°C)", side="left"),
        yaxis5=dict(title="Humedad (%)", side="right", overlaying="y4")
    )
    
    return fig

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
        with st.expander("ℹ️ Información de la Simulación 3D"):
            st.write("""
            **🌳 Características de la Simulación:**
            
            **Árboles Realistas:**
            - Troncos con textura realista
            - Follaje multicapa con diferentes tonos de verde
            - Frutas y flores decorativas
            - Animación de balanceo por viento
            
            **Efectos Ambientales:**
            - Sistema de riego con partículas de agua animadas
            - Iluminación solar ajustable
            - Efectos de viento en tiempo real
            - Sombras dinámicas
            
            **Interactividad:**
            - Controles independientes para cada árbol
            - Temperatura y humedad ajustables
            - Activación/desactivación de riego
            - Cámara con controles de órbita (arrastrar para rotar, scroll para zoom)
            
            **Indicadores de Salud:**
            - Cambio de color del follaje según condiciones
            - Estados visuales: óptimo, advertencia, peligro, regando
            - Información en tiempo real del estado del sistema
            
            **Controles de Vista:**
            - Intensidad de luz solar
            - Fuerza del viento
            - Rotación libre de cámara
            """)
            
        with st.expander("🎮 Guía de Uso"):
            st.write("""
            **Cómo usar la simulación:
            
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
        
        # Botón para crear el archivo si no existe
        if st.button("🔧 Crear archivo de simulación"):
            try:
                # Aquí se podría crear el archivo automáticamente
                st.info("💡 Para crear el archivo de simulación, ejecuta el script `simulacion_arbol_threejs_streamlit.py` por separado.")
            except Exception as e:
                st.error(f"Error al crear el archivo: {str(e)}")

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
    
    # Estadísticas detalladas
    st.sidebar.subheader("📊 Estadísticas 24h")
    
    # Estadísticas de humedad
    st.sidebar.markdown("**💧 Humedad del Suelo:**")
    st.sidebar.text(f"Zona 1: {sistema.estadisticas.get('hum1_prom', 0):.1f}% (promedio)")
    st.sidebar.text(f"Zona 2: {sistema.estadisticas.get('hum2_prom', 0):.1f}% (promedio)")
    
    # Estadísticas de temperatura
    st.sidebar.markdown("**🌡️ Temperatura Ambiente:**")
    st.sidebar.text(f"Sensor 1: {sistema.estadisticas.get('temp1_prom', 0):.1f}°C")
    st.sidebar.text(f"Sensor 2: {sistema.estadisticas.get('temp2_prom', 0):.1f}°C")
    
    # Nuevas estadísticas
    if 'temp_planta_prom' in sistema.estadisticas:
        st.sidebar.markdown("**🌿 Sensores Especializados:**")
        st.sidebar.text(f"Temp. Planta: {sistema.estadisticas['temp_planta_prom']:.1f}°C")
        st.sidebar.text(f"Hum. Relativa: {sistema.estadisticas.get('humedad_relativa_prom', 0):.1f}%")
    
    # Estadísticas de bombas
    st.sidebar.markdown("**🚿 Actividad de Riego:**")
    st.sidebar.text(f"Bomba 1: {sistema.estadisticas.get('bomba1_tiempo', 0):.1f}% tiempo")
    st.sidebar.text(f"Bomba 2: {sistema.estadisticas.get('bomba2_tiempo', 0):.1f}% tiempo")
    
    # === DASHBOARD PRINCIPAL ===
    
    # Métricas principales
    st.subheader("📊 Estado Actual del Sistema")
    mostrar_metricas_principales(sistema.datos_actuales)
    
    # Gráficos principales
    st.subheader("📈 Análisis de Tendencias")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🔄 Tendencias", "🚿 Actividad Bombas", "📊 Estadísticas", "⏱️ Tiempo de Riego", "🎮 Simulación 3D", "🌳 Árboles 3D"])
    
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
    
    with tab5:
        st.markdown("### 🌱 Simulación 3D del Sistema de Riego")
        st.markdown("**Controla las plantas y observa los efectos en tiempo real**")
        
        # Controles interactivos para las plantas
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌿 Planta 1")
            temp1_manual = st.slider("🌡️ Temperatura Planta 1", 15.0, 40.0, 
                                    sistema.datos_actuales.get('temperatura1', 25.0), 0.5)
            hum1_manual = st.slider("💧 Humedad Planta 1", 0.0, 100.0, 
                                  sistema.datos_actuales.get('humedad1', 45.0), 1.0)
            bomba1_manual = st.checkbox("🚿 Activar Riego Planta 1", 
                                      sistema.datos_actuales.get('bomba1_activa', False))
        
        with col2:
            st.markdown("#### 🌿 Planta 2")
            temp2_manual = st.slider("🌡️ Temperatura Planta 2", 15.0, 40.0, 
                                    sistema.datos_actuales.get('temperatura2', 26.0), 0.5)
            hum2_manual = st.slider("💧 Humedad Planta 2", 0.0, 100.0, 
                                  sistema.datos_actuales.get('humedad2', 40.0), 1.0)
            bomba2_manual = st.checkbox("🚿 Activar Riego Planta 2", 
                                      sistema.datos_actuales.get('bomba2_activa', False))
        
        # Generar simulación 3D con valores actuales/manuales
        fig_3d = crear_simulacion_3d_interactiva(
            temp1_manual, hum1_manual, bomba1_manual,
            temp2_manual, hum2_manual, bomba2_manual
        )
        st.plotly_chart(fig_3d, use_container_width=True)
        
        # Información adicional
        st.info("🎮 **Cómo usar la simulación 3D:**\n"
                "• Ajusta los controles deslizantes para cambiar temperatura y humedad\n"
                "• Activa/desactiva el riego con los checkboxes\n"
                "• Observa cómo cambian los campos de temperatura y humedad en 3D\n"
                "• Los jets de agua azules aparecen cuando el riego está activo")
    
    with tab6:
        crear_simulacion_arbol_threejs()
    
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
