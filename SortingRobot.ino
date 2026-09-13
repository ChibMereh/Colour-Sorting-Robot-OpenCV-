#define motorfoward A2
#define motorreverse A3

char command = 0;  // stores last received command

void setup()
{
  pinMode(motorfoward, OUTPUT);
  pinMode(motorreverse, OUTPUT);

  Serial.begin(9600);
}

void loop()
{
  // Reset command each loop unless a new one arrives
  command = 0;

  // Read serial input if available
  if (Serial.available() > 0)
  {
    command = Serial.read();  // read one character
  }

  // Process received command
  switch (command)
  {
    case 's':  // stop
      digitalWrite(motorfoward, LOW);
      digitalWrite(motorreverse, LOW);
      break;

    case 'f':  // forward
      digitalWrite(motorfoward, HIGH);
      digitalWrite(motorreverse, LOW);
      break;

    case 'r':  // reverse
      digitalWrite(motorfoward, LOW);
      digitalWrite(motorreverse, HIGH);
      break;

    default:
      // No valid command received → do nothing
      break;
  }
}
