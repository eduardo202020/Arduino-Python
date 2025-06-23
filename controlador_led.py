"""
Cliente Python - Controla el LED del Arduino (real o simulado)
Este programa se conecta al Arduino y envía comandos para controlar el LED
"""

import socket
import time

class ArduinoController:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.connected = False
        
    def connect(self):
        """Conecta al Arduino (real o simulado)"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"✅ Conectado al Arduino en {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            print("💡 Asegúrate de que el simulador esté ejecutándose")
            return False
    
    def send_command(self, command):
        """Envía un comando al Arduino y recibe la respuesta"""
        if not self.connected:
            print("❌ No hay conexión con Arduino")
            return None
        
        try:
            # Enviar comando
            self.socket.send(command.encode('utf-8'))
            print(f"📤 Comando enviado: '{command}'")
            
            # Recibir respuesta
            response = self.socket.recv(1024).decode('utf-8').strip()
            print(f"📥 Respuesta recibida: '{response}'")
            
            return response
            
        except Exception as e:
            print(f"❌ Error en comunicación: {e}")
            return None
    
    def disconnect(self):
        """Desconecta del Arduino"""
        if self.connected:
            self.socket.close()
            self.connected = False
            print("🔌 Desconectado del Arduino")

def main():
    print("=" * 60)
    print("🎮 CONTROLADOR DE LED ARDUINO")
    print("Este programa controla el LED del Arduino")
    print("=" * 60)
    
    # Crear controlador
    controller = ArduinoController()
    
    # Intentar conectar
    if not controller.connect():
        print("\n💡 Para usar este programa:")
        print("1. Ejecuta 'python3 simulador_arduino.py' en otra terminal")
        print("2. O conecta un Arduino real con el código test.ino")
        return
    
    print("\n💡 Comandos disponibles:")
    print("  'on'   - Encender LED")
    print("  'off'  - Apagar LED")
    print("  'quit' - Salir del programa")
    print("-" * 60)
    
    try:
        while True:
            # Leer comando del usuario
            command = input("\n🔧 Ingresa comando (on/off/quit): ").strip().lower()
            
            if command == 'quit':
                break
            elif command in ['on', 'off']:
                # Enviar comando y mostrar resultado
                response = controller.send_command(command)
                
                if response:
                    if command == 'on':
                        print("💡 Estado: LED ENCENDIDO ✅")
                    else:
                        print("🔴 Estado: LED APAGADO ❌")
                else:
                    print("❌ No se recibió respuesta")
                    
                print("-" * 40)
                
            else:
                print("❌ Comando no válido. Usa: on, off, o quit")
                
    except KeyboardInterrupt:
        print("\n⏹️  Programa interrumpido")
    finally:
        controller.disconnect()
        print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()
