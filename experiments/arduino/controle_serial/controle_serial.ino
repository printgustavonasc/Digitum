const int LED = 8;

void setup() {
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();

    if (comando == '1') {
      digitalWrite(LED, HIGH);
    }

    if (comando == '0') {
      digitalWrite(LED, LOW);
    }
  }
}
