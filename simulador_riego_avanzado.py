"""
Simulador de Sistema de Riego con Historial - Simula el comportamiento del archivo sistema_riego.ino
Este programa actúa como si fuera un Arduino real con sensores, actuadores e historial de datos
"""

import socket
import threading
import time
import json
import random
import math

class SistemaRiegoSimulator:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.running = True
        self.clients = []
        
        # Datos actuales de sensores
        self.datos = {
            'humedad1': 45.2,
            'humedad2': 38.7,
            'temperatura1': 24.5,
            'temperatura2': 26.1,
            'bomba1_activa': False,
            'bomba2_activa': False
        }
        
        # Historial de datos (últimas 144 entradas = 24 horas simuladas)
        self.HISTORIAL_SIZE = 144
        self.historial = {
            'humedad1': [],
            'humedad2': [],
            'temperatura1': [],
            'temperatura2': [],
            'bomba1_estados': [],
            'bomba2_estados': [],
            'timestamps': []
        }
        
        # Umbrales de riego
        self.UMBRAL_HUMEDAD_MIN = 30.0
        self.UMBRAL_HUMEDAD_MAX = 70.0
        self.UMBRAL_TEMP_MAX = 35.0
        
        # Generar historial ficticio al inicio
        self.generar_historial_ficticio()
        
        # Mostrar datos iniciales
        print("📊 DATOS INICIALES CARGADOS:")
        self.mostrar_estado_actual()
        self.mostrar_resumen_historial()
        
        # Iniciar simulación de sensores
        self.iniciar_simulacion_sensores()
    
    def generar_historial_ficticio(self):
        """Genera historial ficticio de las últimas 24 horas"""
        print("🔄 Generando historial de 24 horas...")
        
        # Valores base para generar variaciones realistas
        base_hum1 = 50.0
        base_hum2 = 45.0
        base_temp1 = 22.0
        base_temp2 = 24.0
        
        current_time = time.time()
        
        for i in range(self.HISTORIAL_SIZE):
            # Simular ciclo día/noche para temperatura (cada entrada = 10 min)
            hora_del_dia = (i * 10.0 / 60.0)  # Horas transcurridas
            factor_dia = math.sin((hora_del_dia * math.pi) / 12.0)  # Ciclo de 24h
            
            # Generar temperaturas con ciclo día/noche
            temp1 = base_temp1 + (factor_dia * 8.0) + random.uniform(-2, 2)
            temp2 = base_temp2 + (factor_dia * 6.0) + random.uniform(-2, 2)
            
            # Generar humedad con tendencia inversa a temperatura
            hum1 = base_hum1 - (factor_dia * 15.0) + random.uniform(-3, 3)
            hum2 = base_hum2 - (factor_dia * 12.0) + random.uniform(-3, 3)
            
            # Aplicar límites realistas
            temp1 = max(15.0, min(40.0, temp1))
            temp2 = max(15.0, min(40.0, temp2))
            hum1 = max(10.0, min(90.0, hum1))
            hum2 = max(10.0, min(90.0, hum2))
            
            # Determinar estados de bombas basado en humedad
            bomba1 = hum1 < self.UMBRAL_HUMEDAD_MIN
            bomba2 = hum2 < self.UMBRAL_HUMEDAD_MIN
            
            # Agregar al historial
            self.historial['temperatura1'].append(round(temp1, 1))
            self.historial['temperatura2'].append(round(temp2, 1))
            self.historial['humedad1'].append(round(hum1, 1))
            self.historial['humedad2'].append(round(hum2, 1))
            self.historial['bomba1_estados'].append(bomba1)
            self.historial['bomba2_estados'].append(bomba2)
            self.historial['timestamps'].append(current_time - (self.HISTORIAL_SIZE - i) * 600)  # 10 min atrás
        
        # Establecer datos actuales como los más recientes del historial
        self.datos['temperatura1'] = self.historial['temperatura1'][-1]
        self.datos['temperatura2'] = self.historial['temperatura2'][-1]
        self.datos['humedad1'] = self.historial['humedad1'][-1]
        self.datos['humedad2'] = self.historial['humedad2'][-1]
        self.datos['bomba1_activa'] = self.historial['bomba1_estados'][-1]
        self.datos['bomba2_activa'] = self.historial['bomba2_estados'][-1]
        
        print(f"✅ Historial generado: {len(self.historial['humedad1'])} entradas")
    
    def agregar_al_historial(self):
        """Agrega datos actuales al historial"""
        # Si el historial está lleno, remover el más antiguo
        if len(self.historial['humedad1']) >= self.HISTORIAL_SIZE:
            for key in self.historial:
                self.historial[key].pop(0)
        
        # Agregar datos actuales
        self.historial['humedad1'].append(self.datos['humedad1'])
        self.historial['humedad2'].append(self.datos['humedad2'])
        self.historial['temperatura1'].append(self.datos['temperatura1'])
        self.historial['temperatura2'].append(self.datos['temperatura2'])
        self.historial['bomba1_estados'].append(self.datos['bomba1_activa'])
        self.historial['bomba2_estados'].append(self.datos['bomba2_activa'])
        self.historial['timestamps'].append(time.time())
    
    def mostrar_resumen_historial(self):
        """Muestra resumen estadístico del historial"""
        if not self.historial['humedad1']:
            return
            
        print("\n📈 RESUMEN HISTORIAL (24 horas):")
        print("-" * 40)
        
        # Calcular estadísticas
        hum1_avg = sum(self.historial['humedad1']) / len(self.historial['humedad1'])
        hum2_avg = sum(self.historial['humedad2']) / len(self.historial['humedad2'])
        temp1_avg = sum(self.historial['temperatura1']) / len(self.historial['temperatura1'])
        temp2_avg = sum(self.historial['temperatura2']) / len(self.historial['temperatura2'])
        
        bomba1_tiempo = (sum(self.historial['bomba1_estados']) / len(self.historial['bomba1_estados'])) * 100
        bomba2_tiempo = (sum(self.historial['bomba2_estados']) / len(self.historial['bomba2_estados'])) * 100
        
        print(f"🌡️  Temp promedio: Zona1={temp1_avg:.1f}°C, Zona2={temp2_avg:.1f}°C")
        print(f"💧 Humedad promedio: Zona1={hum1_avg:.1f}%, Zona2={hum2_avg:.1f}%")
        print(f"🚿 Tiempo riego: Bomba1={bomba1_tiempo:.1f}%, Bomba2={bomba2_tiempo:.1f}%")
        print(f"📊 Entradas historial: {len(self.historial['humedad1'])}")
    
    def iniciar_simulacion_sensores(self):
        """Inicia la simulación de variación de sensores"""
        def simular_sensores():
            while self.running:
                # Simular variaciones en los sensores
                self.datos['humedad1'] += random.uniform(-2, 2)
                self.datos['humedad2'] += random.uniform(-2, 2)
                self.datos['temperatura1'] += random.uniform(-0.5, 0.5)
                self.datos['temperatura2'] += random.uniform(-0.5, 0.5)
                
                # Mantener valores en rangos realistas
                self.datos['humedad1'] = max(0, min(100, self.datos['humedad1']))
                self.datos['humedad2'] = max(0, min(100, self.datos['humedad2']))
                self.datos['temperatura1'] = max(15, min(40, self.datos['temperatura1']))
                self.datos['temperatura2'] = max(15, min(40, self.datos['temperatura2']))
                
                # Evaluar riego automático
                self.evaluar_riego_automatico()
                
                # Agregar al historial cada 30 segundos (simula 10 min)
                self.agregar_al_historial()
                
                time.sleep(3)  # Actualizar cada 3 segundos
        
        sensor_thread = threading.Thread(target=simular_sensores)
        sensor_thread.daemon = True
        sensor_thread.start()
    
    def evaluar_riego_automatico(self):
        """Evalúa si se debe activar/desactivar el riego automáticamente"""
        # Zona 1
        if self.datos['humedad1'] < self.UMBRAL_HUMEDAD_MIN and not self.datos['bomba1_activa']:
            self.datos['bomba1_activa'] = True
            self.log_evento("🚿 BOMBA 1 ACTIVADA AUTOMÁTICAMENTE", f"Humedad: {self.datos['humedad1']:.1f}%")
        elif self.datos['humedad1'] > self.UMBRAL_HUMEDAD_MAX and self.datos['bomba1_activa']:
            self.datos['bomba1_activa'] = False
            self.log_evento("⏹️ BOMBA 1 DESACTIVADA AUTOMÁTICAMENTE", f"Humedad: {self.datos['humedad1']:.1f}%")
        
        # Zona 2
        if self.datos['humedad2'] < self.UMBRAL_HUMEDAD_MIN and not self.datos['bomba2_activa']:
            self.datos['bomba2_activa'] = True
            self.log_evento("🚿 BOMBA 2 ACTIVADA AUTOMÁTICAMENTE", f"Humedad: {self.datos['humedad2']:.1f}%")
        elif self.datos['humedad2'] > self.UMBRAL_HUMEDAD_MAX and self.datos['bomba2_activa']:
            self.datos['bomba2_activa'] = False
            self.log_evento("⏹️ BOMBA 2 DESACTIVADA AUTOMÁTICAMENTE", f"Humedad: {self.datos['humedad2']:.1f}%")
    
    def log_evento(self, evento, detalle=""):
        """Registra eventos del sistema"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {evento} {detalle}")
        
    def mostrar_estado_actual(self):
        """Muestra el estado actual de todos los sensores"""
        print(f"🌡️  Temperatura 1: {self.datos['temperatura1']:.1f}°C")
        print(f"🌡️  Temperatura 2: {self.datos['temperatura2']:.1f}°C")
        print(f"💧 Humedad 1: {self.datos['humedad1']:.1f}%")
        print(f"💧 Humedad 2: {self.datos['humedad2']:.1f}%")
        print(f"🚿 Bomba 1: {'🟢 ACTIVA' if self.datos['bomba1_activa'] else '🔴 INACTIVA'}")
        print(f"🚿 Bomba 2: {'🟢 ACTIVA' if self.datos['bomba2_activa'] else '🔴 INACTIVA'}")
        
    def generar_respuesta_estado(self):
        """Genera respuesta con el estado completo del sistema"""
        return f"DATOS:{self.datos['humedad1']:.1f},{self.datos['humedad2']:.1f},{self.datos['temperatura1']:.1f},{self.datos['temperatura2']:.1f},{1 if self.datos['bomba1_activa'] else 0},{1 if self.datos['bomba2_activa'] else 0}"
      def generar_respuesta_historial(self, num_entradas=None):
        """Genera respuesta con datos históricos"""
        if num_entradas is None:
            num_entradas = len(self.historial['humedad1'])
        
        respuesta = "HISTORIAL_RECIENTE_INICIO\n"
        
        # Tomar las últimas entradas
        start_idx = max(0, len(self.historial['humedad1']) - num_entradas)
        
        for i in range(start_idx, len(self.historial['humedad1'])):
            idx_relativo = i - start_idx
            respuesta += f"HR:{idx_relativo},{self.historial['humedad1'][i]},{self.historial['humedad2'][i]},{self.historial['temperatura1'][i]},{self.historial['temperatura2'][i]},{1 if self.historial['bomba1_estados'][i] else 0},{1 if self.historial['bomba2_estados'][i] else 0}\n"
        
        respuesta += "HISTORIAL_RECIENTE_FIN"
        return respuesta
    
    def start_server(self):
        """Inicia el servidor que simula el Arduino"""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            print(f"\\n🔌 Sistema de Riego iniciado en {self.host}:{self.port}")
            print("⏳ Esperando conexiones...\\n")
            
            while self.running:
                try:
                    client, addr = self.server.accept()
                    print(f"📱 Cliente conectado desde: {addr}")
                    
                    # Crear hilo para manejar cada cliente
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(client, addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error:
                    break
                    
        except Exception as e:
            print(f"❌ Error en servidor: {e}")
        finally:
            self.server.close()
    
    def handle_client(self, client, addr):
        """Maneja la comunicación con un cliente"""
        try:
            # Enviar estado inicial al conectarse
            response = self.generar_respuesta_estado()
            client.send(response.encode('utf-8'))
            print(f"📤 Estado inicial enviado a {addr}")
            
            while self.running:
                # Recibir comandos del cliente
                data = client.recv(1024).decode('utf-8').strip()
                
                if not data:
                    break
                
                print(f"📨 Comando recibido de {addr}: '{data}'")
                response = self.procesar_comando(data)
                
                # Enviar respuesta
                client.send(response.encode('utf-8'))
                print(f"📤 Respuesta enviada a {addr}: '{response[:50]}...' ")
                print("-" * 60)
                
        except Exception as e:
            print(f"❌ Error con cliente {addr}: {e}")
        finally:
            client.close()
            print(f"🔌 Cliente {addr} desconectado")
    
    def procesar_comando(self, comando):
        """Procesa comandos recibidos del cliente"""
        comando = comando.upper().strip()
        
        if comando == "STATUS":
            return self.generar_respuesta_estado()
        elif comando == "HISTORIAL":
            return self.generar_respuesta_historial()
        elif comando == "HISTORIAL_RECIENTE":
            return self.generar_respuesta_historial(24)  # Últimas 4 horas
        elif comando == "ESTADISTICAS":
            return self.generar_estadisticas()
        elif comando == "BOMBA1_ON":
            self.datos['bomba1_activa'] = True
            self.log_evento("🚿 BOMBA 1 ACTIVADA MANUALMENTE")
            return "BOMBA1_ACTIVADA"
        elif comando == "BOMBA1_OFF":
            self.datos['bomba1_activa'] = False
            self.log_evento("⏹️ BOMBA 1 DESACTIVADA MANUALMENTE")
            return "BOMBA1_DESACTIVADA"
        elif comando == "BOMBA2_ON":
            self.datos['bomba2_activa'] = True
            self.log_evento("🚿 BOMBA 2 ACTIVADA MANUALMENTE")
            return "BOMBA2_ACTIVADA"
        elif comando == "BOMBA2_OFF":
            self.datos['bomba2_activa'] = False
            self.log_evento("⏹️ BOMBA 2 DESACTIVADA MANUALMENTE")
            return "BOMBA2_DESACTIVADA"
        elif comando == "AUTO":
            self.evaluar_riego_automatico()
            return "MODO_AUTO_ACTIVADO"
        else:
            return "COMANDO_DESCONOCIDO"
    
    def generar_estadisticas(self):
        """Genera estadísticas del historial"""
        if not self.historial['humedad1']:
            return "SIN_DATOS"
        
        # Calcular estadísticas
        hum1_avg = sum(self.historial['humedad1']) / len(self.historial['humedad1'])
        hum2_avg = sum(self.historial['humedad2']) / len(self.historial['humedad2'])
        temp1_avg = sum(self.historial['temperatura1']) / len(self.historial['temperatura1'])
        temp2_avg = sum(self.historial['temperatura2']) / len(self.historial['temperatura2'])
        
        hum1_min = min(self.historial['humedad1'])
        hum1_max = max(self.historial['humedad1'])
        hum2_min = min(self.historial['humedad2'])
        hum2_max = max(self.historial['humedad2'])
        
        temp1_min = min(self.historial['temperatura1'])
        temp1_max = max(self.historial['temperatura1'])
        temp2_min = min(self.historial['temperatura2'])
        temp2_max = max(self.historial['temperatura2'])
        
        bomba1_tiempo = (sum(self.historial['bomba1_estados']) / len(self.historial['bomba1_estados'])) * 100
        bomba2_tiempo = (sum(self.historial['bomba2_estados']) / len(self.historial['bomba2_estados'])) * 100
        
        return f"STATS:{hum1_avg:.1f},{hum2_avg:.1f},{temp1_avg:.1f},{temp2_avg:.1f},{hum1_min:.1f},{hum1_max:.1f},{hum2_min:.1f},{hum2_max:.1f},{temp1_min:.1f},{temp1_max:.1f},{temp2_min:.1f},{temp2_max:.1f},{bomba1_tiempo:.1f},{bomba2_tiempo:.1f}"
    
    def stop(self):
        """Detiene el simulador"""
        self.running = False
        if hasattr(self, 'server'):
            self.server.close()

def main():
    print("=" * 70)
    print("🌱 SIMULADOR DE SISTEMA DE RIEGO INTELIGENTE CON HISTORIAL")
    print("Este programa simula un Arduino con sensores, actuadores e historial")
    print("=" * 70)
    
    simulator = SistemaRiegoSimulator()
    
    try:
        simulator.start_server()
    except KeyboardInterrupt:
        print("\\n⏹️  Deteniendo simulador...")
        simulator.stop()
        print("✅ Simulador detenido")

if __name__ == "__main__":
    main()
