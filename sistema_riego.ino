/*
Sistema de Riego Inteligente - Arduino
- 2 Sensores de humedad del suelo
- 2 Sensores de temperatura 
- 2 Controladores de riego (bombas/válvulas)
- Comunicación serie con Python
*/

// Pines de sensores (simulados)
#define SENSOR_HUMEDAD_1 A0
#define SENSOR_HUMEDAD_2 A1
#define SENSOR_TEMP_1 A2
#define SENSOR_TEMP_2 A3

// Pines de controladores de riego
#define BOMBA_1 2
#define BOMBA_2 3
#define LED_STATUS 13

// Variables de estado
struct SensorData {
    float humedad1;
    float humedad2;
    float temperatura1;
    float temperatura2;
    bool bomba1_activa;
    bool bomba2_activa;
};

SensorData datos;

// Historial de datos (últimas 24 horas simuladas)
#define HISTORIAL_SIZE 144  // 24 horas * 6 lecturas por hora (cada 10 min)
struct HistorialData {
    float humedad1[HISTORIAL_SIZE];
    float humedad2[HISTORIAL_SIZE];
    float temperatura1[HISTORIAL_SIZE];
    float temperatura2[HISTORIAL_SIZE];
    bool bomba1_estados[HISTORIAL_SIZE];
    bool bomba2_estados[HISTORIAL_SIZE];
    int indice_actual;
    bool historial_completo;
};

HistorialData historial;

// Umbrales de riego
float UMBRAL_HUMEDAD_MIN = 30.0;  // Si humedad < 30%, activar riego
float UMBRAL_HUMEDAD_MAX = 70.0;  // Si humedad > 70%, desactivar riego
float UMBRAL_TEMP_MAX = 35.0;     // Si temp > 35°C, riego más frecuente

void setup() {
    Serial.begin(921600);
    Serial.setTimeout(1);
    
    // Configurar pines
    pinMode(BOMBA_1, OUTPUT);
    pinMode(BOMBA_2, OUTPUT);
    pinMode(LED_STATUS, OUTPUT);
    
    // Estado inicial
    digitalWrite(BOMBA_1, LOW);
    digitalWrite(BOMBA_2, LOW);
    digitalWrite(LED_STATUS, LOW);
    
    datos.bomba1_activa = false;
    datos.bomba2_activa = false;
    
    // Cargar datos ficticios iniciales
    cargarDatosIniciales();
    
    Serial.println("Sistema de Riego Iniciado");
    enviarEstadoCompleto();
}

void loop() {
    // Leer sensores cada 2 segundos
    static unsigned long lastRead = 0;
    if (millis() - lastRead > 2000) {
        leerSensores();
        evaluarRiego();
        lastRead = millis();
    }
    
    // Agregar al historial cada 10 minutos (simulado: cada 30 segundos)
    static unsigned long lastHistorial = 0;
    if (millis() - lastHistorial > 30000) {
        agregarAlHistorial();
        lastHistorial = millis();
    }
    
    // Procesar comandos serie
    while (Serial.available()) {
        String comando = Serial.readString();
        comando.trim();
        procesarComando(comando);
    }
    
    delay(100);
}

void cargarDatosIniciales() {
    // Simular datos como si hubiera leído sensores anteriormente
    datos.humedad1 = 45.2;
    datos.humedad2 = 38.7;
    datos.temperatura1 = 24.5;
    datos.temperatura2 = 26.1;
    
    // Inicializar historial
    historial.indice_actual = 0;
    historial.historial_completo = false;
    
    // Generar historial ficticio de las últimas 24 horas
    generarHistorialFicticio();
}

void generarHistorialFicticio() {
    Serial.println("Generando historial de 24 horas...");
    
    // Valores base para generar variaciones realistas
    float base_hum1 = 50.0;
    float base_hum2 = 45.0;
    float base_temp1 = 22.0;
    float base_temp2 = 24.0;
    
    for (int i = 0; i < HISTORIAL_SIZE; i++) {
        // Simular ciclo día/noche para temperatura
        float hora_del_dia = (i * 10.0 / 60.0); // Cada entrada = 10 min
        float factor_dia = sin((hora_del_dia * PI) / 12.0); // Ciclo de 24h
        
        // Generar temperaturas con ciclo día/noche
        historial.temperatura1[i] = base_temp1 + (factor_dia * 8.0) + random(-20, 20) / 10.0;
        historial.temperatura2[i] = base_temp2 + (factor_dia * 6.0) + random(-20, 20) / 10.0;
        
        // Generar humedad con tendencia inversa a temperatura
        historial.humedad1[i] = base_hum1 - (factor_dia * 15.0) + random(-30, 30) / 10.0;
        historial.humedad2[i] = base_hum2 - (factor_dia * 12.0) + random(-30, 30) / 10.0;
        
        // Aplicar límites realistas
        historial.temperatura1[i] = constrain(historial.temperatura1[i], 15.0, 40.0);
        historial.temperatura2[i] = constrain(historial.temperatura2[i], 15.0, 40.0);
        historial.humedad1[i] = constrain(historial.humedad1[i], 10.0, 90.0);
        historial.humedad2[i] = constrain(historial.humedad2[i], 10.0, 90.0);
        
        // Determinar estados de bombas basado en humedad
        historial.bomba1_estados[i] = historial.humedad1[i] < UMBRAL_HUMEDAD_MIN;
        historial.bomba2_estados[i] = historial.humedad2[i] < UMBRAL_HUMEDAD_MIN;
    }
    
    // Marcar como completo y establecer índice actual
    historial.historial_completo = true;
    historial.indice_actual = HISTORIAL_SIZE - 1;
    
    Serial.println("Historial generado completamente");
    Serial.print("Entradas en historial: ");
    Serial.println(HISTORIAL_SIZE);
}

void agregarAlHistorial() {
    // Agregar datos actuales al historial
    historial.indice_actual = (historial.indice_actual + 1) % HISTORIAL_SIZE;
    
    historial.humedad1[historial.indice_actual] = datos.humedad1;
    historial.humedad2[historial.indice_actual] = datos.humedad2;
    historial.temperatura1[historial.indice_actual] = datos.temperatura1;
    historial.temperatura2[historial.indice_actual] = datos.temperatura2;
    historial.bomba1_estados[historial.indice_actual] = datos.bomba1_activa;
    historial.bomba2_estados[historial.indice_actual] = datos.bomba2_activa;
    
    if (!historial.historial_completo && historial.indice_actual == HISTORIAL_SIZE - 1) {
        historial.historial_completo = true;
    }
}

void leerSensores() {
    // Simular lecturas con variaciones realistas
    datos.humedad1 += random(-20, 20) / 10.0;
    datos.humedad2 += random(-20, 20) / 10.0;
    datos.temperatura1 += random(-10, 10) / 10.0;
    datos.temperatura2 += random(-10, 10) / 10.0;
    
    // Mantener valores en rangos realistas
    datos.humedad1 = constrain(datos.humedad1, 0, 100);
    datos.humedad2 = constrain(datos.humedad2, 0, 100);
    datos.temperatura1 = constrain(datos.temperatura1, 15, 40);
    datos.temperatura2 = constrain(datos.temperatura2, 15, 40);
}

void evaluarRiego() {
    // Zona 1
    if (datos.humedad1 < UMBRAL_HUMEDAD_MIN && !datos.bomba1_activa) {
        activarBomba(1, true);
    } else if (datos.humedad1 > UMBRAL_HUMEDAD_MAX && datos.bomba1_activa) {
        activarBomba(1, false);
    }
    
    // Zona 2
    if (datos.humedad2 < UMBRAL_HUMEDAD_MIN && !datos.bomba2_activa) {
        activarBomba(2, true);
    } else if (datos.humedad2 > UMBRAL_HUMEDAD_MAX && datos.bomba2_activa) {
        activarBomba(2, false);
    }
}

void activarBomba(int bomba, bool estado) {
    if (bomba == 1) {
        digitalWrite(BOMBA_1, estado ? HIGH : LOW);
        datos.bomba1_activa = estado;
    } else if (bomba == 2) {
        digitalWrite(BOMBA_2, estado ? HIGH : LOW);
        datos.bomba2_activa = estado;
    }
    
    // LED indicador: encendido si alguna bomba está activa
    digitalWrite(LED_STATUS, (datos.bomba1_activa || datos.bomba2_activa) ? HIGH : LOW);
}

void procesarComando(String comando) {
    if (comando == "STATUS") {
        enviarEstadoCompleto();
    } else if (comando == "HISTORIAL") {
        enviarHistorialCompleto();
    } else if (comando == "HISTORIAL_RECIENTE") {
        enviarHistorialReciente(24); // Últimas 24 entradas (4 horas)
    } else if (comando == "ESTADISTICAS") {
        enviarEstadisticas();
    } else if (comando == "BOMBA1_ON") {
        activarBomba(1, true);
        Serial.println("BOMBA1_ACTIVADA");
    } else if (comando == "BOMBA1_OFF") {
        activarBomba(1, false);
        Serial.println("BOMBA1_DESACTIVADA");
    } else if (comando == "BOMBA2_ON") {
        activarBomba(2, true);
        Serial.println("BOMBA2_ACTIVADA");
    } else if (comando == "BOMBA2_OFF") {
        activarBomba(2, false);
        Serial.println("BOMBA2_DESACTIVADA");
    } else if (comando == "AUTO") {
        evaluarRiego();
        Serial.println("MODO_AUTO_ACTIVADO");
    } else {
        Serial.println("COMANDO_DESCONOCIDO");
    }
}

void enviarEstadoCompleto() {
    Serial.print("DATOS:");
    Serial.print(datos.humedad1); Serial.print(",");
    Serial.print(datos.humedad2); Serial.print(",");
    Serial.print(datos.temperatura1); Serial.print(",");
    Serial.print(datos.temperatura2); Serial.print(",");
    Serial.print(datos.bomba1_activa ? "1" : "0"); Serial.print(",");
    Serial.print(datos.bomba2_activa ? "1" : "0");
    Serial.println();
}
