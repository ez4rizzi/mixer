void setup() {
    Serial.begin(9600);  // Inicializa a comunicação serial
}

void loop() {
    // Lê os valores dos potenciômetros (0 a 1023)
    int volumeMaster = analogRead(A0);
    int volumeApp1 = analogRead(A1);
    int volumeApp2 = analogRead(A2);
    int volumeApp3 = analogRead(A3);

    // Envia os dados formatados corretamente: <VAL1,VAL2,VAL3,VAL4>
    Serial.print("<");
    Serial.print(volumeMaster);
    Serial.print(",");
    Serial.print(volumeApp1);
    Serial.print(",");
    Serial.print(volumeApp2);
    Serial.print(",");
    Serial.print(volumeApp3);
    Serial.println(">");  // Fecha o pacote de dados

    delay(50);  // Evita sobrecarga na porta serial
}
