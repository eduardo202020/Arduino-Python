#!/usr/bin/env python3
"""
Script de prueba para verificar que las versiones corregidas funcionen
"""

import time
import subprocess
import sys
import socket

def test_simulador():
    """Prueba que el simulador corregido funcione"""
    print("🔧 Probando simulador corregido...")
    
    # Iniciar simulador en segundo plano
    try:
        proc = subprocess.Popen([sys.executable, "simulador_corregido.py"], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
        
        # Esperar que se inicie
        time.sleep(3)
        
        # Probar conexión
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        
        try:
            sock.connect(('localhost', 9999))
            
            # Enviar comando HISTORIAL_RECIENTE
            sock.send(b"HISTORIAL_RECIENTE")
            response = sock.recv(8192).decode('utf-8')
            
            sock.close()
            
            # Verificar respuesta
            if "HISTORIAL_RECIENTE_INICIO" in response and "HR:" in response:
                print("✅ Simulador corregido funciona correctamente")
                print(f"📊 Respuesta tiene {len(response)} caracteres")
                print(f"📈 Líneas de historial: {response.count('HR:')}")
                return True
            else:
                print("❌ Simulador no envía historial correctamente")
                print(f"Respuesta: {response[:200]}...")
                return False
                
        except Exception as e:
            print(f"❌ Error conectando al simulador: {e}")
            return False
        finally:
            proc.terminate()
            proc.wait()
            
    except Exception as e:
        print(f"❌ Error iniciando simulador: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 PRUEBA DE VERSIONES CORREGIDAS")
    print("=" * 60)
    
    if test_simulador():
        print("\n✅ LAS VERSIONES CORREGIDAS FUNCIONAN CORRECTAMENTE")
        print("\n📋 Para usar las versiones corregidas:")
        print("1. ./run.sh -> Opción 5 (Simulador corregido)")
        print("2. ./run.sh -> Opción 6 (Controlador corregido)")
        print("3. ./run.sh -> Opción 7 (Demo completo corregido)")
    else:
        print("\n❌ HAY PROBLEMAS CON LAS VERSIONES CORREGIDAS")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
