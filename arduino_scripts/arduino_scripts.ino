String data;
void setup() {

  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  Serial.begin(9600);

}


void loop() {
  
  data = Serial.readStringUntil('\n');
  
  if (data.length() > 2) {;
    data = "";
  } else {
    Serial.println("no entro");
    delay(100);
  }
  if (data == "2") {
    digitalWrite(2, HIGH);
  } else {
    digitalWrite(2, LOW);
  }
  /*
  switch(data) {
    case "2":
      digitalWrite(2, HIGH);
      digitalWrite(3, LOW);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      break;
    
    case "3":
      digitalWrite(3, HIGH);
      digitalWrite(2, LOW);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      break;

    case "4":
      digitalWrite(4, HIGH);
      digitalWrite(3, LOW);
      digitalWrite(2, LOW);
      digitalWrite(5, LOW);
      break;

    case "5":
      digitalWrite(5, HIGH);
      digitalWrite(3, LOW);
      digitalWrite(4, LOW);
      digitalWrite(2, LOW);
      break;
  }*/
}
