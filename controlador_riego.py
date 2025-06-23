"""
Controlador de Sistema de Riego Inteligente
- Monitoreo de sensores de humedad y temperatura
- Control manual y automático de bombas de riego
- Interfaz de usuario intuitiva
"""

import socket
import time
import threading
import os
from datetime import datetime

class ControladorRiego:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.connected = False
        self.datos = {}
        self.log_eventos = []
        
    def connect(self):
        """Conecta al sistema de riego"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"✅ Conectado al Sistema de Riego en {self.host}:{self.port}")
            
            # Recibir estado inicial
            self.obtener_estado()
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
            response = self.socket.recv(1024).decode('utf-8').strip()
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
    
    def mostrar_dashboard(self):
        """Muestra el dashboard principal"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("=" * 80)
        print("🌱 SISTEMA DE RIEGO INTELIGENTE - DASHBOARD")
        print("=" * 80)
        
        if not self.datos:
            print("❌ No hay datos disponibles")
            return
        
        # Estado de sensores
        print(f"📊 ESTADO DE SENSORES ({self.datos['timestamp']})")
        print("-" * 50)
        print(f"🌡️  Zona 1 - Temperatura: {self.datos['temperatura1']:.1f}°C")
        print(f"💧 Zona 1 - Humedad:     {self.datos['humedad1']:.1f}% {self.get_estado_humedad(self.datos['humedad1'])}")
        print(f"🚿 Zona 1 - Bomba:       {self.get_estado_bomba(self.datos['bomba1_activa'])}")
        print()
        print(f"🌡️  Zona 2 - Temperatura: {self.datos['temperatura2']:.1f}°C")
        print(f"💧 Zona 2 - Humedad:     {self.datos['humedad2']:.1f}% {self.get_estado_humedad(self.datos['humedad2'])}")
        print(f"🚿 Zona 2 - Bomba:       {self.get_estado_bomba(self.datos['bomba2_activa'])}")
        print()
        
        # Recomendaciones
        self.mostrar_recomendaciones()
        
        # Menú de opciones
        print("=" * 80)
        print("🎮 OPCIONES DE CONTROL:")
        print("1. 🔄 Actualizar datos        6. 🚿 Bomba 2 ON")
        print("2. 🤖 Modo automático         7. ⏹️  Bomba 2 OFF")
        print("3. 📊 Mostrar historial       8. 🔧 Configuración")
        print("4. 🚿 Bomba 1 ON             9. 📋 Ayuda")
        print("5. ⏹️  Bomba 1 OFF            0. 🚪 Salir")
        print("=" * 80)
    
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
        
        print()
    
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
    
    def mostrar_historial(self):
        """Muestra el historial de eventos"""
        print("\n📋 HISTORIAL DE EVENTOS:")
        print("-" * 50)
        
        if not self.log_eventos:
            print("No hay eventos registrados")
        else:
            for evento in self.log_eventos[-10:]:  # Últimos 10 eventos
                print(evento)
        
        input("\nPresiona Enter para continuar...")
    
    def mostrar_ayuda(self):
        """Muestra información de ayuda"""
        print("\n❓ AYUDA DEL SISTEMA:")
        print("-" * 50)
        print("🌱 Sistema de Riego Inteligente")
        print("• Monitorea humedad y temperatura de 2 zonas")
        print("• Controla 2 bombas de riego independientes")
        print("• Modo automático: riega cuando humedad < 30%")
        print("• Detiene riego cuando humedad > 70%")
        print("\n🎮 Comandos:")
        print("• Actualizar: obtiene datos actuales de sensores")
        print("• Modo automático: activa riego inteligente")
        print("• Control manual: activa/desactiva bombas manualmente")
        
        input("\nPresiona Enter para continuar...")
    
    def disconnect(self):
        """Desconecta del sistema"""
        if self.connected:
            self.socket.close()
            self.connected = False
            print("🔌 Desconectado del sistema")

def main():
    print("🌱 Iniciando Controlador de Riego Inteligente...")
    
    # Crear controlador
    controller = ControladorRiego()
    
    # Intentar conectar
    if not controller.connect():
        print("\n💡 Para usar este programa:")
        print("1. Ejecuta 'python3 simulador_riego.py' en otra terminal")
        print("2. O conecta un Arduino real con el código sistema_riego.ino")
        return
    
    # Loop principal
    try:
        while True:
            controller.mostrar_dashboard()
            
            opcion = input("\n🔧 Selecciona una opción: ").strip()
            
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
                controller.mostrar_historial()
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
                print("🔧 Configuración no implementada aún")
                time.sleep(1)
            elif opcion == '9':
                controller.mostrar_ayuda()
            else:
                print("❌ Opción no válida")
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n⏹️  Programa interrumpido")
    finally:
        controller.disconnect()
        print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()
