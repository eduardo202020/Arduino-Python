

void setup(){
    Serial.begin(921600);
    /*Esta linea va al inicio*/
    Serial.SetTimeout(1);
    pinMode(LED_BUILTIN,OUTPUT);
    digitalWrite(LED_BUILTIN,LOW);
}

void void loop(){
   
    while(Serial.avaible){
        String data = Serial.readString();
        if(data=='on'){
            digitalWrite(LED_BUILTIN,HIGH);
            Serial.print(data);
        }else{
            digitalWrite(LED_BUILTIN,LOW);
            Serial.print(data);
        }
    }
}