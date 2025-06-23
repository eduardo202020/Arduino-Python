"""
Controlador Avanzado de Sistema de Riego con Historial y Gráficos
- Visualización de datos históricos
- Gráficos de tendencias
- Estadísticas detalladas
- Control inteligente
"""

import socket
import time
import threading
import os
from datetime import datetime, timedelta
import json

class ControladorRiegoAvanzado:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.connected = False
        self.datos = {}
        self.historial = []
        self.estadisticas = {}
        self.log_eventos = []
        
    def connect(self):
        """Conecta al sistema de riego"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"✅ Conectado al Sistema de Riego en {self.host}:{self.port}")
            
            # Cargar datos iniciales
            self.obtener_estado()
            self.obtener_estadisticas()
            return True
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            print("💡 Asegúrate de que el simulador esté ejecutándose")
            return False
    
    def send_command(self, command):
        """Envía un comando al sistema y recibe la respuesta"""
        if not self.connected:
            print("❌ No hay conexión con el sistema")
            return None
        
        try:
            self.socket.send(command.encode('utf-8'))
            response = self.socket.recv(4096).decode('utf-8').strip()  # Buffer más grande para historial
            return response
        except Exception as e:
            print(f"❌ Error en comunicación: {e}")
            return None
    
    def obtener_estado(self):
        """Obtiene el estado actual del sistema"""
        response = self.send_command("STATUS")
        if response and response.startswith("DATOS:"):
            self.parsear_datos(response)
            return True
        return False
      def obtener_historial_reciente(self):
        """Obtiene historial reciente (últimas 4 horas)"""
        print("📊 Solicitando historial...")
        response = self.send_command("HISTORIAL_RECIENTE")
        if response:
            print(f"📥 Respuesta historial recibida: {len(response)} caracteres")
            if "HISTORIAL_RECIENTE_INICIO" in response:
                self.parsear_historial(response)
                return True
            else:
                print(f"⚠️ Respuesta inesperada: {response[:100]}...")
        else:
            print("❌ No se recibió respuesta del historial")
        return False
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas del sistema"""
        response = self.send_command("ESTADISTICAS")
        if response and response.startswith("STATS:"):
            self.parsear_estadisticas(response)
            return True
        return False
    
    def parsear_datos(self, data_string):
        """Parsea la cadena de datos recibida"""
        try:
            # Formato: DATOS:humedad1,humedad2,temp1,temp2,bomba1,bomba2
            datos_raw = data_string.replace("DATOS:", "").split(",")
            
            self.datos = {
                'humedad1': float(datos_raw[0]),
                'humedad2': float(datos_raw[1]),
                'temperatura1': float(datos_raw[2]),
                'temperatura2': float(datos_raw[3]),
                'bomba1_activa': bool(int(datos_raw[4])),
                'bomba2_activa': bool(int(datos_raw[5])),
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
        except Exception as e:
            print(f"❌ Error parseando datos: {e}")
      def parsear_historial(self, historial_string):
        """Parsea el historial recibido"""
        try:
            print(f"📊 DEBUG: Recibido historial ({len(historial_string)} chars)")
            
            lines = historial_string.split('\n')
            self.historial = []
            
            for line in lines:
                line = line.strip()
                if line.startswith('HR:') or line.startswith('H:'):
                    # Formato: HR:indice,hum1,hum2,temp1,temp2,bomba1,bomba2
                    try:
                        parts = line.split(':')[1].split(',')
                        if len(parts) >= 7:
                            self.historial.append({
                                'indice': int(parts[0]),
                                'humedad1': float(parts[1]),
                                'humedad2': float(parts[2]),
                                'temperatura1': float(parts[3]),
                                'temperatura2': float(parts[4]),
                                'bomba1': bool(int(parts[5])),
                                'bomba2': bool(int(parts[6]))
                            })
                    except (ValueError, IndexError) as e:
                        print(f"⚠️ Error parseando línea: {line} - {e}")
                        continue
            
            print(f"✅ Historial parseado: {len(self.historial)} entradas")
            
        except Exception as e:
            print(f"❌ Error parseando historial: {e}")
            print(f"DEBUG: Contenido recibido: {historial_string[:200]}...")
    
    def parsear_estadisticas(self, stats_string):
        """Parsea las estadísticas recibidas"""
        try:
            # Formato: STATS:hum1_avg,hum2_avg,temp1_avg,temp2_avg,hum1_min,hum1_max,hum2_min,hum2_max,temp1_min,temp1_max,temp2_min,temp2_max,bomba1_%,bomba2_%
            datos_raw = stats_string.replace("STATS:", "").split(",")
            
            self.estadisticas = {
                'hum1_promedio': float(datos_raw[0]),
                'hum2_promedio': float(datos_raw[1]),
                'temp1_promedio': float(datos_raw[2]),
                'temp2_promedio': float(datos_raw[3]),
                'hum1_min': float(datos_raw[4]),
                'hum1_max': float(datos_raw[5]),
                'hum2_min': float(datos_raw[6]),
                'hum2_max': float(datos_raw[7]),
                'temp1_min': float(datos_raw[8]),
                'temp1_max': float(datos_raw[9]),
                'temp2_min': float(datos_raw[10]),
                'temp2_max': float(datos_raw[11]),
                'bomba1_tiempo': float(datos_raw[12]),
                'bomba2_tiempo': float(datos_raw[13])
            }
        except Exception as e:
            print(f"❌ Error parseando estadísticas: {e}")
    
    def mostrar_dashboard(self):
        """Muestra el dashboard principal con historial"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("=" * 90)
        print("🌱 SISTEMA DE RIEGO INTELIGENTE - DASHBOARD CON HISTORIAL")
        print("=" * 90)
        
        if not self.datos:
            print("❌ No hay datos disponibles")
            return
        
        # Estado actual
        print(f"📊 ESTADO ACTUAL ({self.datos['timestamp']})")
        print("-" * 60)
        print(f"🌡️  Zona 1 - Temperatura: {self.datos['temperatura1']:.1f}°C")
        print(f"💧 Zona 1 - Humedad:     {self.datos['humedad1']:.1f}% {self.get_estado_humedad(self.datos['humedad1'])}")
        print(f"🚿 Zona 1 - Bomba:       {self.get_estado_bomba(self.datos['bomba1_activa'])}")
        print()
        print(f"🌡️  Zona 2 - Temperatura: {self.datos['temperatura2']:.1f}°C")
        print(f"💧 Zona 2 - Humedad:     {self.datos['humedad2']:.1f}% {self.get_estado_humedad(self.datos['humedad2'])}")
        print(f"🚿 Zona 2 - Bomba:       {self.get_estado_bomba(self.datos['bomba2_activa'])}")
        print()
        
        # Estadísticas
        if self.estadisticas:
            self.mostrar_estadisticas_resumen()
        
        # Gráfico simple en texto
        if self.historial:
            self.mostrar_grafico_simple()
        
        # Recomendaciones
        self.mostrar_recomendaciones()
        
        # Menú de opciones
        print("=" * 90)
        print("🎮 OPCIONES DE CONTROL:")
        print("1. 🔄 Actualizar datos        7. ⏹️  Bomba 2 OFF        13. 📈 Ver historial completo")
        print("2. 🤖 Modo automático         8. 📊 Actualizar estadísticas 14. 🔍 Análisis detallado")
        print("3. 📋 Mostrar historial       9. 📈 Gráfico de humedad    15. 💾 Exportar datos")
        print("4. 🚿 Bomba 1 ON             10. 🌡️  Gráfico temperatura   16. ⚙️  Configuración")
        print("5. ⏹️  Bomba 1 OFF            11. 🚿 Gráfico de riego      17. 📋 Ayuda")
        print("6. 🚿 Bomba 2 ON             12. 📊 Tendencias             0. 🚪 Salir")
        print("=" * 90)
    
    def mostrar_estadisticas_resumen(self):
        """Muestra resumen de estadísticas"""
        print("📈 ESTADÍSTICAS (24 HORAS)")
        print("-" * 60)
        print(f"🌡️  Temperatura promedio: Zona1={self.estadisticas['temp1_promedio']:.1f}°C, Zona2={self.estadisticas['temp2_promedio']:.1f}°C")
        print(f"💧 Humedad promedio:      Zona1={self.estadisticas['hum1_promedio']:.1f}%, Zona2={self.estadisticas['hum2_promedio']:.1f}%")
        print(f"🚿 Tiempo de riego:       Bomba1={self.estadisticas['bomba1_tiempo']:.1f}%, Bomba2={self.estadisticas['bomba2_tiempo']:.1f}%")
        print(f"📊 Rangos humedad:        Zona1=[{self.estadisticas['hum1_min']:.1f}%-{self.estadisticas['hum1_max']:.1f}%], Zona2=[{self.estadisticas['hum2_min']:.1f}%-{self.estadisticas['hum2_max']:.1f}%]")
        print()
    
    def mostrar_grafico_simple(self):
        """Muestra un gráfico simple en texto de las últimas lecturas"""
        print("📈 TENDENCIA HUMEDAD (ÚLTIMAS 12 LECTURAS)")
        print("-" * 60)
        
        # Tomar las últimas 12 entradas
        ultimas = self.historial[-12:] if len(self.historial) >= 12 else self.historial
        
        if not ultimas:
            print("No hay datos históricos")
            return
        
        # Zona 1
        print("💧 Zona 1:")
        self.dibujar_grafico_linea([h['humedad1'] for h in ultimas], "Hum1")
        
        # Zona 2  
        print("💧 Zona 2:")
        self.dibujar_grafico_linea([h['humedad2'] for h in ultimas], "Hum2")
        print()
    
    def dibujar_grafico_linea(self, valores, label):
        """Dibuja un gráfico de línea simple en texto"""
        if not valores:
            return
        
        min_val = min(valores)
        max_val = max(valores)
        rango = max_val - min_val if max_val != min_val else 1
        
        # Normalizar valores a una escala de 0-20 caracteres
        altura = 5
        width = len(valores)
        
        # Crear matriz para el gráfico
        grafico = [[' ' for _ in range(width)] for _ in range(altura)]
        
        for i, valor in enumerate(valores):
            # Calcular posición Y (invertida para mostrar correctamente)
            y = altura - 1 - int(((valor - min_val) / rango) * (altura - 1))
            grafico[y][i] = '●'
        
        # Imprimir gráfico
        for fila in grafico:
            print(f"   {''.join(fila)}")
        
        # Mostrar valores numéricos
        valores_str = " ".join([f"{v:4.1f}" for v in valores])
        print(f"   {valores_str}")
        print(f"   Rango: {min_val:.1f}% - {max_val:.1f}%")
    
    def mostrar_grafico_detallado(self, tipo):
        """Muestra gráficos más detallados según el tipo"""
        if not self.historial:
            print("❌ No hay datos históricos disponibles")
            input("Presiona Enter para continuar...")
            return
        
        print(f"\\n📈 GRÁFICO DETALLADO - {tipo.upper()}")
        print("=" * 80)
        
        if tipo == "humedad":
            print("💧 EVOLUCIÓN DE HUMEDAD (ÚLTIMAS 24 ENTRADAS)")
            print("-" * 60)
            hum1_vals = [h['humedad1'] for h in self.historial[-24:]]
            hum2_vals = [h['humedad2'] for h in self.historial[-24:]]
            
            print("Zona 1 (●):")
            self.dibujar_grafico_avanzado(hum1_vals, 0, 100)
            print("\\nZona 2 (○):")
            self.dibujar_grafico_avanzado(hum2_vals, 0, 100)
            
        elif tipo == "temperatura":
            print("🌡️  EVOLUCIÓN DE TEMPERATURA (ÚLTIMAS 24 ENTRADAS)")
            print("-" * 60)
            temp1_vals = [h['temperatura1'] for h in self.historial[-24:]]
            temp2_vals = [h['temperatura2'] for h in self.historial[-24:]]
            
            print("Zona 1 (●):")
            self.dibujar_grafico_avanzado(temp1_vals, 15, 40)
            print("\\nZona 2 (○):")
            self.dibujar_grafico_avanzado(temp2_vals, 15, 40)
            
        elif tipo == "riego":
            print("🚿 ACTIVIDAD DE RIEGO (ÚLTIMAS 24 ENTRADAS)")
            print("-" * 60)
            bomba1_vals = [1 if h['bomba1'] else 0 for h in self.historial[-24:]]
            bomba2_vals = [1 if h['bomba2'] else 0 for h in self.historial[-24:]]
            
            print("Bomba 1 (█ = ACTIVA, ░ = INACTIVA):")
            self.dibujar_grafico_barras(bomba1_vals)
            print("\\nBomba 2 (█ = ACTIVA, ░ = INACTIVA):")
            self.dibujar_grafico_barras(bomba2_vals)
        
        input("\\nPresiona Enter para continuar...")
    
    def dibujar_grafico_avanzado(self, valores, min_escala, max_escala):
        """Dibuja un gráfico más avanzado con escala fija"""
        if not valores:
            return
        
        altura = 8
        rango = max_escala - min_escala
        
        # Crear matriz para el gráfico
        grafico = [[' ' for _ in range(len(valores))] for _ in range(altura)]
        
        for i, valor in enumerate(valores):
            # Calcular posición Y
            y = altura - 1 - int(((valor - min_escala) / rango) * (altura - 1))
            y = max(0, min(altura - 1, y))  # Asegurar que esté en rango
            grafico[y][i] = '●'
        
        # Imprimir gráfico con escala
        for j, fila in enumerate(grafico):
            escala_val = max_escala - (j * rango / (altura - 1))
            print(f"{escala_val:5.1f} │{''.join(fila)}")
        
        # Línea inferior
        print(f"      └{'─' * len(valores)}")
        
        # Mostrar algunos valores
        print("Valores:", " ".join([f"{v:4.1f}" for v in valores[-10:]]))  # Últimos 10
    
    def dibujar_grafico_barras(self, valores):
        """Dibuja un gráfico de barras para estados on/off"""
        simbolos = ['░', '█']
        grafico = ''.join([simbolos[val] for val in valores])
        print(f"   {grafico}")
        
        # Estadísticas
        total_activo = sum(valores)
        porcentaje = (total_activo / len(valores)) * 100 if valores else 0
        print(f"   Tiempo activo: {total_activo}/{len(valores)} ({porcentaje:.1f}%)")
    
    def get_estado_humedad(self, humedad):
        """Retorna indicador visual del estado de humedad"""
        if humedad < 30:
            return "🔴 BAJA"
        elif humedad > 70:
            return "🔵 ALTA"
        else:
            return "🟢 NORMAL"
    
    def get_estado_bomba(self, activa):
        """Retorna indicador visual del estado de la bomba"""
        return "🟢 ACTIVA" if activa else "🔴 INACTIVA"
    
    def mostrar_recomendaciones(self):
        """Muestra recomendaciones basadas en los datos"""
        print("💡 RECOMENDACIONES:")
        print("-" * 30)
        
        # Zona 1
        if self.datos['humedad1'] < 30:
            print("🚨 Zona 1: Humedad baja - Se recomienda riego")
        elif self.datos['humedad1'] > 70:
            print("⚠️  Zona 1: Humedad alta - Detener riego")
        
        # Zona 2
        if self.datos['humedad2'] < 30:
            print("🚨 Zona 2: Humedad baja - Se recomienda riego")
        elif self.datos['humedad2'] > 70:
            print("⚠️  Zona 2: Humedad alta - Detener riego")
        
        # Temperatura
        if self.datos['temperatura1'] > 35 or self.datos['temperatura2'] > 35:
            print("🌡️  Temperatura alta - Considerar riego adicional")
        
        # Análisis de tendencias
        if self.historial and len(self.historial) > 5:
            hum1_tendencia = self.calcular_tendencia([h['humedad1'] for h in self.historial[-5:]])
            hum2_tendencia = self.calcular_tendencia([h['humedad2'] for h in self.historial[-5:]])
            
            if hum1_tendencia < -2:
                print("📉 Zona 1: Humedad descendiendo rápidamente")
            if hum2_tendencia < -2:
                print("📉 Zona 2: Humedad descendiendo rápidamente")
        
        print()
    
    def calcular_tendencia(self, valores):
        """Calcula la tendencia de una serie de valores"""
        if len(valores) < 2:
            return 0
        
        # Calcular pendiente simple
        return valores[-1] - valores[0]
    
    def ejecutar_comando_bomba(self, bomba, accion):
        """Ejecuta comando de bomba"""
        comando = f"BOMBA{bomba}_{accion}"
        response = self.send_command(comando)
        
        if response:
            estado = "activada" if accion == "ON" else "desactivada"
            print(f"✅ Bomba {bomba} {estado} exitosamente")
            self.log_evento(f"Bomba {bomba} {estado} manualmente")
        else:
            print(f"❌ Error al controlar bomba {bomba}")
    
    def modo_automatico(self):
        """Activa el modo automático"""
        response = self.send_command("AUTO")
        if response:
            print("🤖 Modo automático activado")
            print("💡 El sistema evaluará automáticamente cuando regar")
            self.log_evento("Modo automático activado")
        else:
            print("❌ Error al activar modo automático")
    
    def log_evento(self, evento):
        """Registra un evento en el log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_eventos.append(f"[{timestamp}] {evento}")
        
        # Mantener solo los últimos 20 eventos
        if len(self.log_eventos) > 20:
            self.log_eventos.pop(0)
    
    def mostrar_historial_completo(self):
        """Muestra el historial completo de eventos"""
        print("\\n📋 HISTORIAL COMPLETO:")
        print("-" * 80)
        
        if not self.historial:
            print("No hay datos históricos")
        else:
            print(f"Total de entradas: {len(self.historial)}")
            print("\\nÚltimas 10 entradas:")
            for i, entrada in enumerate(self.historial[-10:]):
                print(f"{i+1:2d}. H1:{entrada['humedad1']:5.1f}% H2:{entrada['humedad2']:5.1f}% "
                      f"T1:{entrada['temperatura1']:4.1f}°C T2:{entrada['temperatura2']:4.1f}°C "
                      f"B1:{'ON' if entrada['bomba1'] else 'OFF'} B2:{'ON' if entrada['bomba2'] else 'OFF'}")
        
        if self.log_eventos:
            print("\\nEventos recientes:")
            for evento in self.log_eventos[-10:]:
                print(evento)
        
        input("\\nPresiona Enter para continuar...")
    
    def mostrar_ayuda(self):
        """Muestra información de ayuda"""
        print("\\n❓ AYUDA DEL SISTEMA AVANZADO:")
        print("-" * 80)
        print("🌱 Sistema de Riego Inteligente con Historial")
        print("• Monitorea humedad y temperatura de 2 zonas")
        print("• Mantiene historial de 24 horas (144 entradas)")
        print("• Controla 2 bombas de riego independientes")
        print("• Modo automático: riega cuando humedad < 30%")
        print("• Detiene riego cuando humedad > 70%")
        print("• Análisis de tendencias y estadísticas")
        print("\\n🎮 Comandos adicionales:")
        print("• Gráficos: visualiza tendencias de sensores")
        print("• Estadísticas: promedios, mínimos, máximos")
        print("• Historial: datos completos de 24 horas")
        print("• Análisis: tendencias y recomendaciones")
        print("\\n📈 Interpretación de gráficos:")
        print("• ● = Punto de datos")
        print("• █ = Bomba activa, ░ = Bomba inactiva")
        print("• Escala lateral muestra valores reales")
        
        input("\\nPresiona Enter para continuar...")
    
    def disconnect(self):
        """Desconecta del sistema"""
        if self.connected:
            self.socket.close()
            self.connected = False
            print("🔌 Desconectado del sistema")

def main():
    print("🌱 Iniciando Controlador Avanzado de Riego...")
    
    # Crear controlador
    controller = ControladorRiegoAvanzado()
    
    # Intentar conectar
    if not controller.connect():
        print("\\n💡 Para usar este programa:")
        print("1. Ejecuta 'python3 simulador_riego_avanzado.py' en otra terminal")
        print("2. O conecta un Arduino real con el código sistema_riego.ino")
        return
    
    # Cargar historial inicial
    print("📊 Cargando historial...")
    controller.obtener_historial_reciente()
    time.sleep(1)
    
    # Loop principal
    try:
        while True:
            controller.mostrar_dashboard()
            
            opcion = input("\\n🔧 Selecciona una opción: ").strip()
            
            if opcion == '0':
                break
            elif opcion == '1':
                controller.obtener_estado()
                print("🔄 Datos actualizados")
                time.sleep(1)
            elif opcion == '2':
                controller.modo_automatico()
                time.sleep(2)
            elif opcion == '3':
                controller.obtener_historial_reciente()
                print("📊 Historial actualizado")
                time.sleep(1)
            elif opcion == '4':
                controller.ejecutar_comando_bomba(1, "ON")
                time.sleep(1)
            elif opcion == '5':
                controller.ejecutar_comando_bomba(1, "OFF")
                time.sleep(1)
            elif opcion == '6':
                controller.ejecutar_comando_bomba(2, "ON")
                time.sleep(1)
            elif opcion == '7':
                controller.ejecutar_comando_bomba(2, "OFF")
                time.sleep(1)
            elif opcion == '8':
                controller.obtener_estadisticas()
                print("📊 Estadísticas actualizadas")
                time.sleep(1)
            elif opcion == '9':
                controller.mostrar_grafico_detallado("humedad")
            elif opcion == '10':
                controller.mostrar_grafico_detallado("temperatura")
            elif opcion == '11':
                controller.mostrar_grafico_detallado("riego")
            elif opcion == '12':
                print("📊 Análisis de tendencias no implementado aún")
                time.sleep(1)
            elif opcion == '13':
                controller.mostrar_historial_completo()
            elif opcion == '14':
                print("🔍 Análisis detallado no implementado aún")
                time.sleep(1)
            elif opcion == '15':
                print("💾 Exportar datos no implementado aún")
                time.sleep(1)
            elif opcion == '16':
                print("⚙️  Configuración no implementada aún")
                time.sleep(1)
            elif opcion == '17':
                controller.mostrar_ayuda()
            else:
                print("❌ Opción no válida")
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\\n⏹️  Programa interrumpido")
    finally:
        controller.disconnect()
        print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()
