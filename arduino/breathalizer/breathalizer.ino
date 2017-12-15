const int gasPin = A0;
const int tempPin = A1;

int gasValueRaw = 0;     
int tempValueRaw = 0;     

void setup() {
  pinMode(gasPin, INPUT);
  pinMode(tempPin, INPUT);
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

  // wait 2 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(2);                     
}
