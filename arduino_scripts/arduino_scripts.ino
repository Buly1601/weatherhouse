String data;
void setup() {
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  Serial.begin(9600);
}
void loop() {
  data = Serial.readStringUntil('\n');
  if (data.length() > 2) {
    Serial.println("entro");
    data = "";
} else {
    Serial.println("no entro");
    delay(100);
}
 Serial.println(data);
}
