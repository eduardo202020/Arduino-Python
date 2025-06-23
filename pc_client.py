import serial, time, json, pandas as pd

PORT = input("Pega puerto virtual: ").strip()
ser  = serial.Serial(PORT, 9600, timeout=2)

def ask(cmd):
    ser.write((cmd+"\n").encode())
    return ser.readline().decode().strip()

# --- 1) Obtener historial inicial ----
hist_json = ask("HIST")
print("DEBUG-RAW:", repr(hist_json)) 
history = json.loads(hist_json)
print(f"Historial recibido: {len(history)} registros")

# Opcional: mostrar en tabla
df = pd.DataFrame(history)
print(df.tail())   # últimas filas

# --- 2) Lecturas “en vivo” cada 10 s ----
try:
    while True:
        line = ask("READ")
        print("READ →", line)
        time.sleep(10)
except KeyboardInterrupt:
    ser.close()
