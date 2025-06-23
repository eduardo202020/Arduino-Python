"""
Simulador de Sistema de Riego - Simula el comportamiento del archivo sistema_riego.ino
Este programa actúa como si fuera un Arduino real con sensores y actuadores
"""

import socket
import threading
import time
import json
import random
import math

class SistemaRiegoSimulator:    def __init__(self, host='localhost', port=9999):
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
        
        # Iniciar simulación de sensores
        self.iniciar_simulacion_sensores()
    
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
        
    def start_server(self):
        """Inicia el servidor que simula el Arduino"""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            print(f"🔌 Sistema de Riego iniciado en {self.host}:{self.port}")
            print("⏳ Esperando conexiones...\n")
            
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
                print(f"📤 Respuesta enviada a {addr}: '{response}'")
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
    
    def stop(self):
        """Detiene el simulador"""
        self.running = False
        if hasattr(self, 'server'):
            self.server.close()

def main():
    print("=" * 70)
    print("🌱 SIMULADOR DE SISTEMA DE RIEGO INTELIGENTE")
    print("Este programa simula un Arduino con sensores y actuadores de riego")
    print("=" * 70)
    
    simulator = SistemaRiegoSimulator()
    
    try:
        simulator.start_server()
    except KeyboardInterrupt:
        print("\n⏹️  Deteniendo simulador...")
        simulator.stop()
        print("✅ Simulador detenido")

if __name__ == "__main__":
    main()
