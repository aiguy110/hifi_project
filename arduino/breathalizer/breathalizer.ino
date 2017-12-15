const int gasPin = A0;
const int tempPin = A1;

const int greenPin = 2;
const int yellowPin = 3;
const int redPin = 4;

int gasValueRaw = 0;     
int tempValueRaw = 0;     

void setup() {
  pinMode(gasPin, INPUT);
  pinMode(tempPin, INPUT);
  
  pinMode(greenPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(redPin, OUTPUT);
  
  Serial.begin(9600);
}

void loop() {
  // Read sensor values from on-board ADC
  gasValueRaw = analogRead(gasPin);
  tempValueRaw = analogRead(tempPin);
    
  // Print the results to the serial port
  Serial.print("gasValueRaw=");                       
  Serial.println(gasValueRaw);
  Serial.print("tempValueRaw=");      
  Serial.println(tempValueRaw);
  
  // Update LEDs
  while (Serial.available()){
    digitalWrite(greenPin, LOW);
    digitalWrite(yellowPin, LOW);
    digitalWrite(redPin, LOW);
    char color = Serial.read();
    if (color == 'g'){
      digitalWrite(greenPin, HIGH);
    }else if (color == 'y'){
      digitalWrite(yellowPin, HIGH);
    }else{
      digitalWrite(redPin, HIGH);
    }
  }

  // wait 2 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(2);                     
}
