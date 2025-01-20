

void setup(){
    Serial.begin(921600);
    /*Esta linea va al inicio*/
    Serial.SetTimeout(1);
}

void void loop(){
    while(Serial.avaible){
        String data = Serial.readString();
        Serial.println(data);
    }
}