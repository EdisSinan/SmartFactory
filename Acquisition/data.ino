// Pin assignments
const int ir1Pin = 2;   // IR1 input pin
const int ir2Pin = 3;   // IR2 input pin
const int ir3Pin = 4;   // IR3 input pin
const int ultrasonicPin = 5;  // Ultrasonic sensor input pin
const int motorR = 6;   // IR1 input pin
const int motorL = 7;   // IR2 input pin
const int servoMotor = 8;   // IR3 input pin

unsigned long startTime = 0;

void setup() {
  Serial.begin(9600);
  pinMode(ir1Pin, INPUT);
  pinMode(ir2Pin, INPUT);
  pinMode(ir3Pin, INPUT);
  pinMode(ultrasonicPin, INPUT);
  pinMode(motorR, INPUT);
  pinMode(motorL, INPUT);
  pinMode(servoMotor, INPUT);
  
  startTime = millis(); // Record the start time
}

void loop() {
  unsigned long currentTime = millis();
  float elapsedTime = (currentTime - startTime) / 1000.0; // Convert to seconds

  // Read state of IR sensors
  int ir1State = digitalRead(ir1Pin);
  int ir2State = digitalRead(ir2Pin);
  int ir3State = digitalRead(ir3Pin);
  int motorRState = digitalRead(motorR);
  int motorLState = digitalRead(motorL);
  int servoMotorState = digitalRead(servoMotor);
  
  // Read state of Ultrasonic sensor
  int ultrasonicState = digitalRead(ultrasonicPin);

  // Print the current state of each sensor with timestamp
  Serial.print(elapsedTime, 1); // Print time with 1 decimal place
  Serial.print(",");
  Serial.print(ir1State);
  Serial.print(",");
  Serial.print(ir2State);
  Serial.print(",");
  Serial.print(ir3State);
  Serial.print(",");
  Serial.print(ultrasonicState);
  Serial.print(",");
  Serial.print(motorRState);
  Serial.print(",");
  Serial.print(motorLState);
  Serial.print(",");
  Serial.println(servoMotorState);
  delay (500);
}
