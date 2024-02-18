int right1 = 8;
int right2 = 9;

int left1 = 10;
int left2 = 11;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(right1, OUTPUT);
  pinMode(right2, OUTPUT);
  pinMode(left1, OUTPUT);
  pinMode(left2, OUTPUT);

}

void loop() {
  String input = " ";
  if (Serial.available() > 0) {
    input = Serial.readString();  // Read the incoming data
    input.trim(); // Trim any whitespace
    controlMotors(input); // Parse and execute the command
  }

}

void controlMotors(String input) {
  int firstSpace = input.indexOf(' ');
  int secondSpace = input.indexOf(' ', firstSpace + 1);
  
  if (firstSpace != -1 && secondSpace != -1) {
    String direction = input.substring(0, firstSpace);
    String durationStr = input.substring(firstSpace + 1, secondSpace);    
    double duration = durationStr.toDouble();
    
    if (direction == "forward") {
      forward();
    } else if (direction == "backward") {
      backward();
    } else if (direction == "right") {
      right();
    } else if (direction == "left") {
      left();
    } else {
      stop(); // Stop if direction is unknown
    }
    
    delay(duration * 1000); // Convert duration to milliseconds and delay
    stop(); // Stop the motors after the duration
  }
}


void forward(){
  digitalWrite(right1, HIGH);
  digitalWrite(right2, LOW);
  digitalWrite(left1, HIGH);
  digitalWrite(left2, LOW);
}

void backward(){
  digitalWrite(right1, LOW);
  digitalWrite(right2, HIGH);
  digitalWrite(left1, LOW);
  digitalWrite(left2, HIGH);
}

void right(){
  digitalWrite(right1, HIGH);
  digitalWrite(right2, LOW);
  digitalWrite(left1, LOW);
  digitalWrite(left2, HIGH);
}

void left(){
  digitalWrite(right1, LOW);
  digitalWrite(right2, HIGH);
  digitalWrite(left1, HIGH);
  digitalWrite(left2, LOW);
  
}

void stop(){
  digitalWrite(right1, LOW);
  digitalWrite(right2, LOW);
  digitalWrite(left1, LOW);
  digitalWrite(left2, LOW);
}