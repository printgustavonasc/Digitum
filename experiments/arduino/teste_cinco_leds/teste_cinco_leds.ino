const int leds[] = {8, 9, 10, 11, 12};
const int quantidadeLeds = 5;

void setup() {
  for (int i = 0; i < quantidadeLeds; i++) {
    pinMode(leds[i], OUTPUT);
    digitalWrite(leds[i], LOW);
  }
}

void loop() {
  for (int i = 0; i < quantidadeLeds; i++) {
    digitalWrite(leds[i], HIGH);
    delay(1000);
    digitalWrite(leds[i], LOW);
    delay(300);
  }
}
