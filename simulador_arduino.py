"""
Simulador de Sistema de Riego - Simula el comportamiento del archivo sistema_riego.ino
Este programa actúa como si fuera un Arduino real con sensores y actuadores
"""

import socket
import threading
import time
import json
import random

class SistemaRiegoSimulator:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.running = True
        self.clients = []
        
        # Datos de sensores (cargados como ficticios al inicio)
        self.datos = {
            'humedad1': 45.2,
            'humedad2': 38.7,
            'temperatura1': 24.5,
            'temperatura2': 26.1,
            'bomba1_activa': False,
            'bomba2_activa': False
        }
        
        # Umbrales de riego
        self.UMBRAL_HUMEDAD_MIN = 30.0
        self.UMBRAL_HUMEDAD_MAX = 70.0
        self.UMBRAL_TEMP_MAX = 35.0
        
        # Iniciar simulación de sensores
        self.iniciar_simulacion_sensores()    def iniciar_simulacion_sensores(self):
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
                
                time.sleep(2)  # Actualizar cada 2 segundos
        
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
        
    def generar_respuesta_estado(self):
        """Genera respuesta con el estado completo del sistema"""
        return f"DATOS:{self.datos['humedad1']:.1f},{self.datos['humedad2']:.1f},{self.datos['temperatura1']:.1f},{self.datos['temperatura2']:.1f},{1 if self.datos['bomba1_activa'] else 0},{1 if self.datos['bomba2_activa'] else 0}"
        """Inicia el servidor que simula el Arduino"""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            print(f"🔌 Simulador Arduino iniciado en {self.host}:{self.port}")
            print("💡 LED inicial: APAGADO")
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
        """Maneja la comunicación con un cliente (simula el comportamiento de test.ino)"""
        try:
            while self.running:
                # Recibir datos del cliente (equivale a Serial.available() y Serial.readString())
                data = client.recv(1024).decode('utf-8').strip()
                
                if not data:
                    break
                
                print(f"📨 Recibido de {addr}: '{data}'")
                
                # Procesar comando (simula la lógica del Arduino)
                if data == "on":
                    self.led_state = True
                    response = data  # Simula Serial.print(data)
                    print("💡 LED: ENCENDIDO ✅")
                else:
                    self.led_state = False
                    response = data  # Simula Serial.print(data)
                    print("🔴 LED: APAGADO ❌")
                
                # Enviar respuesta (simula Serial.print())
                client.send(response.encode('utf-8'))
                print(f"📤 Enviado a {addr}: '{response}'")
                print("-" * 50)
                
        except Exception as e:
            print(f"❌ Error con cliente {addr}: {e}")
        finally:
            client.close()
            print(f"🔌 Cliente {addr} desconectado")
    
    def stop(self):
        """Detiene el simulador"""
        self.running = False
        if hasattr(self, 'server'):
            self.server.close()

def main():
    print("=" * 60)
    print("🤖 SIMULADOR DE ARDUINO")
    print("Este programa simula el comportamiento de test.ino")
    print("=" * 60)
    
    simulator = ArduinoSimulator()
    
    try:
        simulator.start_server()
    except KeyboardInterrupt:
        print("\n⏹️  Deteniendo simulador...")
        simulator.stop()
        print("✅ Simulador detenido")

if __name__ == "__main__":
    main()
