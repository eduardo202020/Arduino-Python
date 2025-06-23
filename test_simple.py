#!/usr/bin/env python3
"""
Prueba simple del sistema de riego
"""

import socket
import time
import threading

def test_comunicacion():
    """Prueba la comunicación entre simulador y controlador"""
    print("🔧 PRUEBA DE COMUNICACIÓN")
    print("=" * 50)
    
    # Iniciar simulador en hilo separado
    from simulador_corregido import SistemaRiegoSimulator
    
    print("📊 Iniciando simulador...")
    simulator = SistemaRiegoSimulator()
    
    # Iniciar servidor en hilo
    def run_server():
        try:
            simulator.start_server()
        except:
            pass
    
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Esperar a que se inicie
    time.sleep(2)
    
    # Probar conexión
    print("📱 Probando conexión...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('localhost', 9999))
        
        # Recibir estado inicial
        initial = sock.recv(1024).decode('utf-8')
        print(f"📥 Estado inicial: {initial}")
        
        # Enviar comando historial
        print("📨 Enviando comando HISTORIAL_RECIENTE...")
        sock.send(b"HISTORIAL_RECIENTE")
        
        # Recibir respuesta
        response = sock.recv(8192).decode('utf-8')
        print(f"📤 Respuesta recibida: {len(response)} caracteres")
        
        # Verificar contenido
        if "HISTORIAL_RECIENTE_INICIO" in response:
            lines = response.split('\n')
            hr_lines = [l for l in lines if l.startswith('HR:')]
            print(f"✅ Historial recibido: {len(hr_lines)} entradas")
            
            if hr_lines:
                print("📋 PRIMERAS 3 LÍNEAS:")
                for i, line in enumerate(hr_lines[:3]):
                    print(f"   {i}: {line}")
            
            return True
        else:
            print("❌ No se recibió historial válido")
            print(f"Respuesta: {response[:200]}...")
            return False
            
        sock.close()
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    finally:
        simulator.stop()

if __name__ == "__main__":
    print("🧪 PRUEBA SIMPLE DEL SISTEMA")
    print("=" * 60)
    
    if test_comunicacion():
        print("\n✅ LA COMUNICACIÓN FUNCIONA CORRECTAMENTE")
        print("\n🚀 Para usar el sistema completo:")
        print("   1. Terminal 1: python3 simulador_corregido.py")
        print("   2. Terminal 2: python3 controlador_corregido.py")
        print("   3. En el controlador, usar opción 10 para ver gráficos de temperatura")
    else:
        print("\n❌ HAY PROBLEMAS DE COMUNICACIÓN")
