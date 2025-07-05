"""
Controlador Simple con Historial - VERSION CORREGIDA
"""

import socket
import time
import os

class ControladorSimple:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.connected = False
        self.datos = {}
        self.historial = []
        self.estadisticas = {}
        
    def connect(self):
        """Conecta al simulador"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"✅ Conectado en {self.host}:{self.port}")
            
            # Cargar datos iniciales
            self.obtener_estado()
            self.obtener_historial()
            self.obtener_estadisticas()
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def send_command(self, command):
        """Envía comando"""
        if not self.connected:
            return None
        
        try:
            self.socket.send(command.encode('utf-8'))
            response = self.socket.recv(8192).decode('utf-8').strip()
            return response
        except Exception as e:
            print(f"❌ Error comunicación: {e}")
            return None
    
    def obtener_estado(self):
        """Obtiene estado actual"""
        response = self.send_command("STATUS")
        if response and response.startswith("DATOS:"):
            try:
                datos_raw = response.replace("DATOS:", "").split(",")
                # Estructura actualizada para incluir nuevos sensores
                self.datos = {
                    'humedad1': float(datos_raw[0]),
                    'humedad2': float(datos_raw[1]),
                    'temperatura1': float(datos_raw[2]),
                    'temperatura2': float(datos_raw[3]),
                    'bomba1_activa': bool(int(datos_raw[4])),
                    'bomba2_activa': bool(int(datos_raw[5]))
                }
                
                # Añadir nuevos sensores si están disponibles
                if len(datos_raw) >= 8:
                    self.datos['temp_planta'] = float(datos_raw[6])
                    self.datos['humedad_relativa'] = float(datos_raw[7])
                else:
                    # Valores por defecto si no están disponibles
                    self.datos['temp_planta'] = 0.0
                    self.datos['humedad_relativa'] = 0.0
                
                return True
            except Exception as e:
                print(f"❌ Error parseando datos: {e}")
        return False
    
    def obtener_historial(self):
        """Obtiene historial"""
        print("📊 Obteniendo historial...")
        response = self.send_command("HISTORIAL_RECIENTE")
        
        if response:
            print(f"📥 Respuesta recibida: {len(response)} chars")
            self.parsear_historial(response)
            return len(self.historial) > 0
        else:
            print("❌ No se recibió historial")
            return False
    
    def parsear_historial(self, data):
        """Parsea historial"""
        try:
            self.historial = []
            lines = data.split('\n')
            
            for line in lines:
                line = line.strip()
                if line.startswith('HR:'):
                    parts = line.split(':')[1].split(',')
                    if len(parts) >= 7:
                        entrada = {
                            'indice': int(parts[0]),
                            'humedad1': float(parts[1]),
                            'humedad2': float(parts[2]),
                            'temperatura1': float(parts[3]),
                            'temperatura2': float(parts[4]),
                            'bomba1': bool(int(parts[5])),
                            'bomba2': bool(int(parts[6]))
                        }
                        
                        # Añadir nuevos sensores si están disponibles
                        if len(parts) >= 9:
                            entrada['temp_planta'] = float(parts[7])
                            entrada['humedad_relativa'] = float(parts[8])
                        else:
                            entrada['temp_planta'] = 0.0
                            entrada['humedad_relativa'] = 0.0
                            
                        self.historial.append(entrada)
            
            print(f"✅ Historial parseado: {len(self.historial)} entradas")
            
        except Exception as e:
            print(f"❌ Error parseando: {e}")
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas"""
        response = self.send_command("ESTADISTICAS")
        if response and response.startswith("STATS:"):
            try:
                datos = response.replace("STATS:", "").split(",")
                self.estadisticas = {
                    'hum1_prom': float(datos[0]),
                    'hum2_prom': float(datos[1]),
                    'temp1_prom': float(datos[2]),
                    'temp2_prom': float(datos[3]),
                    'hum1_min': float(datos[4]),
                    'hum1_max': float(datos[5]),
                    'hum2_min': float(datos[6]),
                    'hum2_max': float(datos[7]),
                    'temp1_min': float(datos[8]),
                    'temp1_max': float(datos[9]),
                    'temp2_min': float(datos[10]),
                    'temp2_max': float(datos[11]),
                    'bomba1_tiempo': float(datos[12]),
                    'bomba2_tiempo': float(datos[13])
                }
                return True
            except Exception as e:
                print(f"❌ Error parseando estadísticas: {e}")
        return False
    
    def mostrar_dashboard(self):
        """Dashboard principal"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("=" * 80)
        print("🌱 CONTROLADOR SIMPLE CON HISTORIAL")
        print("=" * 80)
        
        if not self.datos:
            print("❌ No hay datos")
            return
        
        # Estado actual
        print("📊 ESTADO ACTUAL")
        print("-" * 40)
        print(f"🌡️ Temperaturas: Zona1={self.datos['temperatura1']:.1f}°C  Zona2={self.datos['temperatura2']:.1f}°C")
        print(f"💧 Humedad:      Zona1={self.datos['humedad1']:.1f}%   Zona2={self.datos['humedad2']:.1f}%")
        
        # Mostrar nuevos sensores si están disponibles
        if 'temp_planta' in self.datos and self.datos['temp_planta'] > 0:
            print(f"🌿 Temp. Planta:  {self.datos['temp_planta']:.1f}°C")
            
        if 'humedad_relativa' in self.datos and self.datos['humedad_relativa'] > 0:
            print(f"🌫️ Hum. Relativa: {self.datos['humedad_relativa']:.1f}%")
            
        print(f"🚿 Bombas:       Zona1={'🟢ON' if self.datos['bomba1_activa'] else '🔴OFF'}     Zona2={'🟢ON' if self.datos['bomba2_activa'] else '🔴OFF'}")
        print()
        
        # Estadísticas
        if self.estadisticas:
            print("📈 ESTADÍSTICAS (24 HORAS)")
            print("-" * 40)
            print(f"🌡️ Temp promedio:  Z1={self.estadisticas['temp1_prom']:.1f}°C  Z2={self.estadisticas['temp2_prom']:.1f}°C")
            print(f"💧 Hum promedio:   Z1={self.estadisticas['hum1_prom']:.1f}%   Z2={self.estadisticas['hum2_prom']:.1f}%")
            
            # Mostrar estadísticas de nuevos sensores si están disponibles
            if 'temp_planta_prom' in self.estadisticas:
                print(f"🌿 Temp. Planta:   Promedio={self.estadisticas['temp_planta_prom']:.1f}°C")
                print(f"🌫️ Hum. Relativa:  Promedio={self.estadisticas.get('humedad_relativa_prom', 0):.1f}%")
            
            print(f"🚿 Tiempo riego:   Z1={self.estadisticas['bomba1_tiempo']:.1f}%    Z2={self.estadisticas['bomba2_tiempo']:.1f}%")
            print(f"📊 Rangos humedad: Z1=[{self.estadisticas['hum1_min']:.1f}-{self.estadisticas['hum1_max']:.1f}%] Z2=[{self.estadisticas['hum2_min']:.1f}-{self.estadisticas['hum2_max']:.1f}%]")
            print()
        
        # Historial
        if self.historial:
            print(f"📈 HISTORIAL (ÚLTIMAS 10 DE {len(self.historial)} ENTRADAS)")
            print("-" * 95)
            
            # Verificar si hay nuevos sensores en el historial
            tiene_nuevos_sensores = any('temp_planta' in h and h['temp_planta'] > 0 for h in self.historial[-5:])
            
            if tiene_nuevos_sensores:
                print(" #  | H1(%)  H2(%)  | T1(°C) T2(°C) | 🌿TP  🌫️HR  | B1  B2")
                print("-" * 65)
                for i, h in enumerate(self.historial[-10:]):
                    b1 = "🟢" if h['bomba1'] else "🔴"
                    b2 = "🟢" if h['bomba2'] else "🔴"
                    tp = h.get('temp_planta', 0)
                    hr = h.get('humedad_relativa', 0)
                    print(f"{i+1:2d}. | {h['humedad1']:5.1f} {h['humedad2']:5.1f} | {h['temperatura1']:5.1f} {h['temperatura2']:5.1f} | {tp:4.1f} {hr:5.1f} | {b1}  {b2}")
            else:
                print(" #  | H1(%)  H2(%)  | T1(°C) T2(°C) | B1  B2")
                print("-" * 50)
                for i, h in enumerate(self.historial[-10:]):
                    b1 = "🟢" if h['bomba1'] else "🔴"
                    b2 = "🟢" if h['bomba2'] else "🔴"
                    print(f"{i+1:2d}. | {h['humedad1']:5.1f} {h['humedad2']:5.1f} | {h['temperatura1']:5.1f} {h['temperatura2']:5.1f} | {b1}  {b2}")
            print()
            
            # Gráfico simple
            self.mostrar_grafico_simple()
        
        # Menú
        print("=" * 80)
        print("🎮 OPCIONES:")
        print("1. 🔄 Actualizar     5. ⏹️ Bomba 1 OFF    9. 📈 Gráfico humedad")
        print("2. 🤖 Modo auto      6. 🚿 Bomba 2 ON    10. 🌡️ Gráfico temperatura")
        print("3. 📊 Actualizar     7. ⏹️ Bomba 2 OFF    11. 📋 Ver historial completo")
        print("4. 🚿 Bomba 1 ON     8. 📊 Estadísticas   0. 🚪 Salir")
        print("=" * 80)
    
    def mostrar_grafico_simple(self):
        """Gráfico simple de humedad"""
        if len(self.historial) < 5:
            return
        
        print("📈 GRÁFICO HUMEDAD (ÚLTIMAS 12 LECTURAS)")
        print("-" * 50)
        
        # Tomar últimas 12
        datos = self.historial[-12:] if len(self.historial) >= 12 else self.historial
        
        # Zona 1
        valores1 = [h['humedad1'] for h in datos]
        print("💧 Zona 1:")
        self.dibujar_grafico(valores1)
        
        # Zona 2
        valores2 = [h['humedad2'] for h in datos]
        print("💧 Zona 2:")
        self.dibujar_grafico(valores2)
        print()
    
    def dibujar_grafico(self, valores):
        """Dibuja gráfico simple"""
        if not valores:
            return
        
        min_val = min(valores)
        max_val = max(valores)
        rango = max_val - min_val if max_val != min_val else 1
        
        # Escala visual simple
        for valor in valores:
            # Normalizar a escala 0-20
            nivel = int(((valor - min_val) / rango) * 20) if rango > 0 else 10
            barra = "█" * nivel + "░" * (20 - nivel)
            print(f"   {valor:5.1f}% |{barra}|")
        
        print(f"   Rango: {min_val:.1f}% - {max_val:.1f}%")
    
    def mostrar_grafico_detallado(self, tipo):
        """Gráfico detallado"""
        if not self.historial:
            print("❌ No hay datos históricos")
            input("Presiona Enter...")
            return
        
        print(f"\n📈 GRÁFICO DETALLADO - {tipo.upper()}")
        print("=" * 60)
        
        if tipo == "humedad":
            datos1 = [h['humedad1'] for h in self.historial[-20:]]
            datos2 = [h['humedad2'] for h in self.historial[-20:]]
            print("💧 EVOLUCIÓN HUMEDAD (ÚLTIMAS 20 LECTURAS)")
            print("Zona 1:")
            self.dibujar_grafico_avanzado(datos1, 0, 100)
            print("Zona 2:")
            self.dibujar_grafico_avanzado(datos2, 0, 100)
        
        elif tipo == "temperatura":
            datos1 = [h['temperatura1'] for h in self.historial[-20:]]
            datos2 = [h['temperatura2'] for h in self.historial[-20:]]
            print("🌡️ EVOLUCIÓN TEMPERATURA (ÚLTIMAS 20 LECTURAS)")
            print("Zona 1:")
            self.dibujar_grafico_avanzado(datos1, 15, 40)
            print("Zona 2:")
            self.dibujar_grafico_avanzado(datos2, 15, 40)
        
        input("\nPresiona Enter...")
    
    def dibujar_grafico_avanzado(self, valores, min_escala, max_escala):
        """Gráfico avanzado con escala"""
        altura = 6
        rango = max_escala - min_escala
        
        # Crear matriz
        grafico = [[' ' for _ in range(len(valores))] for _ in range(altura)]
        
        for i, valor in enumerate(valores):
            y = altura - 1 - int(((valor - min_escala) / rango) * (altura - 1))
            y = max(0, min(altura - 1, y))
            grafico[y][i] = '●'
        
        # Mostrar
        for j, fila in enumerate(grafico):
            escala_val = max_escala - (j * rango / (altura - 1))
            print(f"{escala_val:5.1f} │{''.join(fila)}")
        
        print(f"      └{'─' * len(valores)}")
        print(f"Últimos valores: {' '.join([f'{v:4.1f}' for v in valores[-10:]])}")
    
    def ejecutar_comando_bomba(self, bomba, accion):
        """Controla bomba"""
        comando = f"BOMBA{bomba}_{accion}"
        response = self.send_command(comando)
        if response:
            estado = "activada" if accion == "ON" else "desactivada"
            print(f"✅ Bomba {bomba} {estado}")
        time.sleep(1)
    
    def disconnect(self):
        """Desconecta"""
        if self.connected:
            self.socket.close()
            self.connected = False

def main():
    print("🌱 Iniciando Controlador Simple...")
    
    controller = ControladorSimple()
    
    if not controller.connect():
        print("\n💡 Ejecuta primero: python3 simulador_corregido.py")
        return
    
    # Loop principal
    try:
        while True:
            controller.mostrar_dashboard()
            
            opcion = input("\n🔧 Opción: ").strip()
            
            if opcion == '0':
                break
            elif opcion == '1':
                controller.obtener_estado()
                controller.obtener_historial()
                print("🔄 Actualizado")
                time.sleep(1)
            elif opcion == '2':
                response = controller.send_command("AUTO")
                print("🤖 Modo automático activado")
                time.sleep(1)
            elif opcion == '3':
                controller.obtener_estadisticas()
                print("📊 Estadísticas actualizadas")
                time.sleep(1)
            elif opcion == '4':
                controller.ejecutar_comando_bomba(1, "ON")
            elif opcion == '5':
                controller.ejecutar_comando_bomba(1, "OFF")
            elif opcion == '6':
                controller.ejecutar_comando_bomba(2, "ON")
            elif opcion == '7':
                controller.ejecutar_comando_bomba(2, "OFF")
            elif opcion == '8':
                controller.obtener_estadisticas()
                input("Presiona Enter...")
            elif opcion == '9':
                controller.mostrar_grafico_detallado("humedad")
            elif opcion == '10':
                controller.mostrar_grafico_detallado("temperatura")
            elif opcion == '11':
                print(f"\n📋 HISTORIAL COMPLETO ({len(controller.historial)} entradas)")
                print("-" * 60)
                for i, h in enumerate(controller.historial):
                    if i % 10 == 0:
                        print(f"\nEntradas {i+1}-{min(i+10, len(controller.historial))}:")
                    b1 = "ON" if h['bomba1'] else "OFF"
                    b2 = "ON" if h['bomba2'] else "OFF"
                    print(f"{i+1:3d}. H1:{h['humedad1']:5.1f}% H2:{h['humedad2']:5.1f}% T1:{h['temperatura1']:4.1f}°C T2:{h['temperatura2']:4.1f}°C B1:{b1} B2:{b2}")
                input("\nPresiona Enter...")
            else:
                print("❌ Opción no válida")
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n⏹️ Saliendo...")
    finally:
        controller.disconnect()

if __name__ == "__main__":
    main()
