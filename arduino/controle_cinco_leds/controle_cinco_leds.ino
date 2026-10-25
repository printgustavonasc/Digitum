
const int leds[] = {2, 3, 4, 5, 6};
const int totalLeds = 5;

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < totalLeds; i++) {
    pinMode(leds[i], OUTPUT);
    digitalWrite(leds[i], LOW);
  }
}

void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();

    if (comando >= '0' && comando <= '5') {
      int quantidade = comando - '0';

      for (int i = 0; i < totalLeds; i++) {
        if (i < quantidade) {
          digitalWrite(leds[i], HIGH);
        } else {
          digitalWrite(leds[i], LOW);
        }
      }
    }
  }
}
