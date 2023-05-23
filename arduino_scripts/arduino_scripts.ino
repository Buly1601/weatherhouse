void setup() {
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  Serial.begin(9600);
}
void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    
    if (data == "2") {
      digitalWrite(2, HIGH);
      digitalWrite(3, LOW);
  } else if (data == "3") {
      digitalWrite(3, HIGH);
      digitalWrite(2, LOW);
  } else {
      digitalWrite(2, HIGH);
      digitalWrite(3, HIGH);	
  }

 }
}
