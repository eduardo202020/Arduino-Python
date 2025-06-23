import os, pty, threading, time, random, json
from datetime import datetime, timedelta

INTERVAL = 10          # segundos entre lecturas “en vivo”
HIST_MINUTOS = 15      # cuánto historial falso generar

class ArduinoSimulator:
    def __init__(self):
        # -- Puerto serie virtual --
        self.master, self.slave = pty.openpty()
        self.slave_name = os.ttyname(self.slave)

        # -- Estado interno --
        self.temp, self.humi = 22.0, 60.0
        self.led_state = False
        self.irrigation = False
        self.running = True

        # -- Historial previo --
        self.history = []
        self._generate_initial_history()

        print(f"Puerto virtual: {self.slave_name}")
        print(f"(Historial simulado de {len(self.history)} medidas)")

    # ------------------------------------------------------------------    
    def _generate_initial_history(self):
        """Crea lecturas falsas hacia atrás en el tiempo."""
        t = datetime.now() - timedelta(minutes=HIST_MINUTOS)
        for _ in range(int(HIST_MINUTOS*60/INTERVAL)):
            self._random_walk()               # variar temp/humi
            self.history.append(
                {"ts": t.isoformat(timespec='seconds'),
                 "temp": round(self.temp,1),
                 "hum":  round(self.humi,1)}
            )
            t += timedelta(seconds=INTERVAL)

    def _random_walk(self):
        self.temp = max(15, min(self.temp + random.uniform(-0.3, 0.3), 35))
        self.humi = max(30, min(self.humi + random.uniform(-0.6, 0.6), 90))

    # ------------------------------------------------------------------
    def simulate_arduino(self):
        t0 = time.time()
        while self.running:
            # ① Generar nueva lectura cada INTERVAL
            if time.time() - t0 >= INTERVAL:
                t0 = time.time()
                self._random_walk()
                self.history.append({
                    "ts": datetime.now().isoformat(timespec='seconds'),
                    "temp": round(self.temp,1),
                    "hum":  round(self.humi,1)
                })

            # ② Escuchar comandos
            try:
                data = os.read(self.master, 128)
                if data:
                    self._process_cmd(data.decode().strip().upper())
            except OSError:
                break
            except Exception as e:
                print("ERROR:", e)

            time.sleep(0.05)

    # ------------------------------------------------------------------
    def _process_cmd(self, msg):
        print("📨 RX:", msg)

        if msg in ("ON", "OFF"):
            self.led_state = (msg == "ON")
            os.write(self.master, f"LED:{msg}\n".encode())

        elif msg in ("IRR_ON", "IRR_OFF"):
            self.irrigation = (msg == "IRR_ON")
            estado = "ON" if self.irrigation else "OFF"
            os.write(self.master, f"IRRIGACION:{estado}\n".encode())

        elif msg == "READ":
            ultimo = self.history[-1]
            os.write(self.master,
                     f"T:{ultimo['temp']} H:{ultimo['hum']}\n".encode())

        elif msg == "HIST":
            blob = json.dumps(self.history) + "\n"
            os.write(self.master, blob.encode())

        else:
            os.write(self.master, b"ERR\n")

    # ------------------------------------------------------------------
    def start(self):
        threading.Thread(target=self.simulate_arduino,
                         daemon=True).start()
        return self.slave_name

    def stop(self):
        self.running = False
        os.close(self.master); os.close(self.slave)

# ----------------------------------------------------------------------
if __name__ == "__main__":
    sim = ArduinoSimulator()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        sim.stop()
