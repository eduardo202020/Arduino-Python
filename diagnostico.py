#!/usr/bin/env python3
"""
Script de diagnóstico para el sistema de riego
"""

import sys
import os
import socket
import time

def test_simulador_directo():
    """Prueba el simulador directamente"""
    print("🔧 PRUEBA DIRECTA DEL SIMULADOR")
    print("=" * 50)
    
    try:
        # Importar el simulador
        sys.path.append('.')
        from simulador_corregido import SistemaRiegoSimulator
        
        # Crear instancia
        print("📊 Creando simulador...")
        simulator = SistemaRiegoSimulator()
        
        # Verificar historial
        print(f"📈 Historial generado:")
        print(f"   - Humedad 1: {len(simulator.historial['humedad1'])} entradas")
        print(f"   - Humedad 2: {len(simulator.historial['humedad2'])} entradas")
        print(f"   - Temperatura 1: {len(simulator.historial['temperatura1'])} entradas")
        print(f"   - Temperatura 2: {len(simulator.historial['temperatura2'])} entradas")
        
        if len(simulator.historial['humedad1']) > 0:
            print("✅ Historial generado correctamente")
            
            # Mostrar primeras 5 entradas
            print("\n📋 PRIMERAS 5 ENTRADAS:")
            for i in range(min(5, len(simulator.historial['humedad1']))):
                print(f"   {i}: H1={simulator.historial['humedad1'][i]:.1f}%, "
                      f"H2={simulator.historial['humedad2'][i]:.1f}%, "
                      f"T1={simulator.historial['temperatura1'][i]:.1f}°C, "
                      f"T2={simulator.historial['temperatura2'][i]:.1f}°C")
            
            # Probar comando HISTORIAL_RECIENTE
            print("\n🔧 PROBANDO COMANDO HISTORIAL_RECIENTE:")
            response = simulator.generar_respuesta_historial(10)
            if "HR:" in response:
                print(f"✅ Comando funciona - Respuesta: {len(response)} chars")
                lines = response.split('\n')
                hr_lines = [l for l in lines if l.startswith('HR:')]
                print(f"📊 Líneas HR encontradas: {len(hr_lines)}")
                
                if hr_lines:
                    print("📋 PRIMERA LÍNEA HR:")
                    print(f"   {hr_lines[0]}")
            else:
                print("❌ Comando no devuelve historial")
                print(f"Respuesta: {response[:200]}")
        else:
            print("❌ No se generó historial")
            
        return len(simulator.historial['humedad1']) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_controlador_directo():
    """Prueba el controlador directamente"""
    print("\n🎮 PRUEBA DIRECTA DEL CONTROLADOR")
    print("=" * 50)
      try:
        from controlador_corregido import ControladorSimple
        
        print("📊 Creando controlador...")
        controller = ControladorSimple()
        
        # Simular parseo de historial
        test_data = """HISTORIAL_RECIENTE_INICIO
HR:0,45.2,38.7,24.5,26.1,0,1
HR:1,46.1,39.2,24.8,26.3,0,0
HR:2,44.8,37.9,25.1,26.5,1,0
HISTORIAL_RECIENTE_FIN"""
        
        print("🔧 Probando parseo de historial...")
        controller.parsear_historial(test_data)
        
        if len(controller.historial) > 0:
            print(f"✅ Parseo exitoso - {len(controller.historial)} entradas")
            print("📋 PRIMERA ENTRADA:")
            print(f"   {controller.historial[0]}")
            return True
        else:
            print("❌ No se parseó el historial")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🧪 DIAGNÓSTICO DEL SISTEMA DE RIEGO")
    print("=" * 60)
    
    # Cambiar al directorio correcto
    os.chdir('/mnt/d/Home/Desktop/Arduino-Python')
    
    # Probar simulador
    sim_ok = test_simulador_directo()
    
    # Probar controlador
    ctrl_ok = test_controlador_directo()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN:")
    print(f"   Simulador: {'✅ OK' if sim_ok else '❌ FALLA'}")
    print(f"   Controlador: {'✅ OK' if ctrl_ok else '❌ FALLA'}")
    
    if sim_ok and ctrl_ok:
        print("\n🚀 TODO FUNCIONA - El problema puede ser de comunicación")
        print("💡 Intenta ejecutar:")
        print("   1. Terminal 1: python3 simulador_corregido.py")
        print("   2. Terminal 2: python3 controlador_corregido.py")
    else:
        print("\n❌ HAY PROBLEMAS EN EL CÓDIGO")

if __name__ == "__main__":
    main()
