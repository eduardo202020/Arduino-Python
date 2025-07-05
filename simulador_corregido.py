"""
Simulador de Sistema de Riego con Historial - VERSION CORREGIDA
"""

import socket
import threading
import time
import random
import math

class SistemaRiegoSimulator:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.running = True
        
        # Datos actuales
        self.datos = {
            'humedad1': 45.2,              # Humedad suelo zona 1
            'humedad2': 38.7,              # Humedad suelo zona 2
            'temperatura1': 24.5,          # Temperatura ambiente zona 1
            'temperatura2': 26.1,          # Temperatura ambiente zona 2
            'temp_planta': 23.8,           # Temperatura de la planta (nueva)
            'humedad_relativa': 65.2,      # Humedad relativa del entorno (nueva)
            'bomba1_activa': False,
            'bomba2_activa': False
        }
        
        # Historial - listas simples
        self.historial = {
            'humedad1': [],
            'humedad2': [],
            'temperatura1': [],
            'temperatura2': [],
            'temp_planta': [],             # Nueva: temperatura planta
            'humedad_relativa': [],        # Nueva: humedad relativa
            'bomba1_estados': [],
            'bomba2_estados': []
        }
        
        # Umbrales
        self.UMBRAL_HUMEDAD_MIN = 30.0
        self.UMBRAL_HUMEDAD_MAX = 70.0
        
        # Generar historial
        self.generar_historial_ficticio()
        print("📊 SIMULADOR CON HISTORIAL LISTO")
        print(f"📈 Historial generado: {len(self.historial['humedad1'])} entradas")
        
        # Iniciar simulación
        self.iniciar_simulacion_sensores()
    
    def generar_historial_ficticio(self):
        """Genera 144 entradas de historial (24 horas)"""
        print("🔄 Generando historial...")
        
        for i in range(144):  # 144 entradas = 24 horas
            # Ciclo día/noche
            hora = (i * 10.0 / 60.0)  # Cada entrada = 10 min
            factor_dia = math.sin((hora * math.pi) / 12.0)
            
            # Temperatura ambiente con ciclo día/noche
            temp1 = 22.0 + (factor_dia * 8.0) + random.uniform(-2, 2)
            temp2 = 24.0 + (factor_dia * 6.0) + random.uniform(-2, 2)
            
            # Temperatura de planta (ligeramente más baja que ambiente)
            temp_planta = (temp1 + temp2) / 2 - 1.5 + random.uniform(-1, 1)
            
            # Humedad del suelo (inversa a temperatura)
            hum1 = 50.0 - (factor_dia * 15.0) + random.uniform(-5, 5)
            hum2 = 45.0 - (factor_dia * 12.0) + random.uniform(-5, 5)
            
            # Humedad relativa del entorno (mayor en la noche, menor en el día)
            hum_relativa = 70.0 - (factor_dia * 25.0) + random.uniform(-8, 8)
            
            # Aplicar límites realistas
            temp1 = max(15.0, min(40.0, temp1))
            temp2 = max(15.0, min(40.0, temp2))
            temp_planta = max(12.0, min(35.0, temp_planta))
            hum1 = max(10.0, min(90.0, hum1))
            hum2 = max(10.0, min(90.0, hum2))
            hum_relativa = max(30.0, min(95.0, hum_relativa))
            
            # Estados de bombas
            bomba1 = hum1 < self.UMBRAL_HUMEDAD_MIN
            bomba2 = hum2 < self.UMBRAL_HUMEDAD_MIN
            
            # Agregar al historial
            self.historial['temperatura1'].append(round(temp1, 1))
            self.historial['temperatura2'].append(round(temp2, 1))
            self.historial['temp_planta'].append(round(temp_planta, 1))
            self.historial['humedad1'].append(round(hum1, 1))
            self.historial['humedad2'].append(round(hum2, 1))
            self.historial['humedad_relativa'].append(round(hum_relativa, 1))
            self.historial['bomba1_estados'].append(bomba1)
            self.historial['bomba2_estados'].append(bomba2)
        
        # Establecer datos actuales como los más recientes
        self.datos['temperatura1'] = self.historial['temperatura1'][-1]
        self.datos['temperatura2'] = self.historial['temperatura2'][-1]
        self.datos['temp_planta'] = self.historial['temp_planta'][-1]
        self.datos['humedad1'] = self.historial['humedad1'][-1]
        self.datos['humedad2'] = self.historial['humedad2'][-1]
        self.datos['humedad_relativa'] = self.historial['humedad_relativa'][-1]
        self.datos['bomba1_activa'] = self.historial['bomba1_estados'][-1]
        self.datos['bomba2_activa'] = self.historial['bomba2_estados'][-1]
    
    def iniciar_simulacion_sensores(self):
        """Simula variaciones de sensores"""
        def simular():
            while self.running:
                # Pequeñas variaciones
                self.datos['humedad1'] += random.uniform(-1, 1)
                self.datos['humedad2'] += random.uniform(-1, 1)
                self.datos['temperatura1'] += random.uniform(-0.3, 0.3)
                self.datos['temperatura2'] += random.uniform(-0.3, 0.3)
                self.datos['temp_planta'] += random.uniform(-0.2, 0.2)
                self.datos['humedad_relativa'] += random.uniform(-2, 2)
                
                # Límites
                self.datos['humedad1'] = max(0, min(100, self.datos['humedad1']))
                self.datos['humedad2'] = max(0, min(100, self.datos['humedad2']))
                self.datos['temperatura1'] = max(15, min(40, self.datos['temperatura1']))
                self.datos['temperatura2'] = max(15, min(40, self.datos['temperatura2']))
                self.datos['temp_planta'] = max(12, min(35, self.datos['temp_planta']))
                self.datos['humedad_relativa'] = max(30, min(95, self.datos['humedad_relativa']))
                
                # Redondear
                for key in self.datos:
                    if isinstance(self.datos[key], (int, float)) and not isinstance(self.datos[key], bool):
                        self.datos[key] = round(self.datos[key], 1)
                
                # Evaluar riego automático
                self.evaluar_riego_automatico()
                
                # Agregar al historial (mantener solo las últimas 144)
                if len(self.historial['humedad1']) >= 144:
                    for key in self.historial:
                        self.historial[key].pop(0)
                
                for key in ['humedad1', 'humedad2', 'temperatura1', 'temperatura2', 'temp_planta', 'humedad_relativa']:
                    self.historial[key].append(self.datos[key])
                self.historial['bomba1_estados'].append(self.datos['bomba1_activa'])
                self.historial['bomba2_estados'].append(self.datos['bomba2_activa'])
                
                time.sleep(3)
        
        thread = threading.Thread(target=simular)
        thread.daemon = True
        thread.start()
    
    def evaluar_riego_automatico(self):
        """Evalúa riego automático"""
        # Zona 1
        if self.datos['humedad1'] < self.UMBRAL_HUMEDAD_MIN and not self.datos['bomba1_activa']:
            self.datos['bomba1_activa'] = True
            print(f"[{time.strftime('%H:%M:%S')}] 🚿 BOMBA 1 ON - Humedad: {self.datos['humedad1']:.1f}%")
        elif self.datos['humedad1'] > self.UMBRAL_HUMEDAD_MAX and self.datos['bomba1_activa']:
            self.datos['bomba1_activa'] = False
            print(f"[{time.strftime('%H:%M:%S')}] ⏹️ BOMBA 1 OFF - Humedad: {self.datos['humedad1']:.1f}%")
        
        # Zona 2
        if self.datos['humedad2'] < self.UMBRAL_HUMEDAD_MIN and not self.datos['bomba2_activa']:
            self.datos['bomba2_activa'] = True
            print(f"[{time.strftime('%H:%M:%S')}] 🚿 BOMBA 2 ON - Humedad: {self.datos['humedad2']:.1f}%")
        elif self.datos['humedad2'] > self.UMBRAL_HUMEDAD_MAX and self.datos['bomba2_activa']:
            self.datos['bomba2_activa'] = False
            print(f"[{time.strftime('%H:%M:%S')}] ⏹️ BOMBA 2 OFF - Humedad: {self.datos['humedad2']:.1f}%")
    
    def start_server(self):
        """Inicia el servidor"""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            print(f"\n🔌 Servidor iniciado en {self.host}:{self.port}")
            print("⏳ Esperando conexiones...\n")
            
            while self.running:
                try:
                    client, addr = self.server.accept()
                    print(f"📱 Cliente conectado: {addr}")
                    
                    thread = threading.Thread(target=self.handle_client, args=(client, addr))
                    thread.daemon = True
                    thread.start()
                    
                except socket.error:
                    break
                    
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.server.close()
    
    def handle_client(self, client, addr):
        """Maneja cliente"""
        try:
            # Enviar estado inicial
            response = self.generar_respuesta_estado()
            client.send(response.encode('utf-8'))
            
            while self.running:
                data = client.recv(1024).decode('utf-8').strip()
                if not data:
                    break
                
                print(f"📨 Comando: {data}")
                response = self.procesar_comando(data)
                client.send(response.encode('utf-8'))
                print(f"📤 Respuesta enviada ({len(response)} chars)")
                
        except Exception as e:
            print(f"❌ Error con cliente: {e}")
        finally:
            client.close()
            print(f"🔌 Cliente {addr} desconectado")
    
    def procesar_comando(self, comando):
        """Procesa comandos"""
        cmd = comando.upper().strip()
        
        if cmd == "STATUS":
            return self.generar_respuesta_estado()
        elif cmd == "HISTORIAL_RECIENTE":
            return self.generar_respuesta_historial(24)
        elif cmd == "ESTADISTICAS":
            return self.generar_estadisticas()
        elif cmd == "BOMBA1_ON":
            self.datos['bomba1_activa'] = True
            print("🚿 BOMBA 1 ACTIVADA MANUALMENTE")
            return "BOMBA1_ACTIVADA"
        elif cmd == "BOMBA1_OFF":
            self.datos['bomba1_activa'] = False
            print("⏹️ BOMBA 1 DESACTIVADA MANUALMENTE")
            return "BOMBA1_DESACTIVADA"
        elif cmd == "BOMBA2_ON":
            self.datos['bomba2_activa'] = True
            print("🚿 BOMBA 2 ACTIVADA MANUALMENTE")
            return "BOMBA2_ACTIVADA"
        elif cmd == "BOMBA2_OFF":
            self.datos['bomba2_activa'] = False
            print("⏹️ BOMBA 2 DESACTIVADA MANUALMENTE")
            return "BOMBA2_DESACTIVADA"
        elif cmd == "AUTO":
            self.evaluar_riego_automatico()
            return "MODO_AUTO_ACTIVADO"
        else:
            return "COMANDO_DESCONOCIDO"
    
    def generar_respuesta_estado(self):
        """Genera respuesta de estado"""
        return f"DATOS:{self.datos['humedad1']},{self.datos['humedad2']},{self.datos['temperatura1']},{self.datos['temperatura2']},{1 if self.datos['bomba1_activa'] else 0},{1 if self.datos['bomba2_activa'] else 0},{self.datos['temp_planta']},{self.datos['humedad_relativa']}"
    
    def generar_respuesta_historial(self, num_entradas=24):
        """Genera respuesta con historial"""
        if not self.historial['humedad1']:
            return "SIN_HISTORIAL"
        
        # Tomar las últimas entradas
        start_idx = max(0, len(self.historial['humedad1']) - num_entradas)
        
        respuesta = "HISTORIAL_RECIENTE_INICIO\n"
        
        for i in range(start_idx, len(self.historial['humedad1'])):
            idx = i - start_idx
            respuesta += f"HR:{idx},{self.historial['humedad1'][i]},{self.historial['humedad2'][i]},{self.historial['temperatura1'][i]},{self.historial['temperatura2'][i]},{1 if self.historial['bomba1_estados'][i] else 0},{1 if self.historial['bomba2_estados'][i] else 0},{self.historial['temp_planta'][i]},{self.historial['humedad_relativa'][i]}\n"
        
        respuesta += "HISTORIAL_RECIENTE_FIN"
        return respuesta
    
    def generar_estadisticas(self):
        """Genera estadísticas"""
        if not self.historial['humedad1']:
            return "SIN_DATOS"
        
        h1 = self.historial['humedad1']
        h2 = self.historial['humedad2']
        t1 = self.historial['temperatura1']
        t2 = self.historial['temperatura2']
        b1 = self.historial['bomba1_estados']
        b2 = self.historial['bomba2_estados']
        
        stats = f"STATS:{sum(h1)/len(h1):.1f},{sum(h2)/len(h2):.1f},{sum(t1)/len(t1):.1f},{sum(t2)/len(t2):.1f},{min(h1):.1f},{max(h1):.1f},{min(h2):.1f},{max(h2):.1f},{min(t1):.1f},{max(t1):.1f},{min(t2):.1f},{max(t2):.1f},{(sum(b1)/len(b1)*100):.1f},{(sum(b2)/len(b2)*100):.1f}"
        return stats
    
    def stop(self):
        """Detiene el simulador"""
        self.running = False
        if hasattr(self, 'server'):
            self.server.close()

def main():
    print("=" * 70)
    print("🌱 SIMULADOR DE RIEGO CON HISTORIAL - VERSION CORREGIDA")
    print("=" * 70)
    
    simulator = SistemaRiegoSimulator()
    
    try:
        simulator.start_server()
    except KeyboardInterrupt:
        print("\n⏹️ Deteniendo...")
        simulator.stop()

if __name__ == "__main__":
    main()
