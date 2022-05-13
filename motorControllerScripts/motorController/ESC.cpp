#include "ESC.h"
void ESC::escConfig(int ESC_PIN1, int ESC_PIN2, int MIN_WIDTH, int MAX_WIDTH)
{
  this -> ESC_PIN1 = ESC_PIN1;
  this -> ESC_PIN2 = ESC_PIN2;
  this -> MIN_WIDTH = MIN_WIDTH;
  this -> MAX_WIDTH = MAX_WIDTH;
  this -> THROTTLE_PERC = 0;
  this -> LEFT_THROTTLE = 90;
  this -> RIGHT_THROTTLE = 90;
  this -> minThrottle = 90;
}

void ESC::init()
{
  Servo LEFT;
  Servo RIGHT;
  this -> LEFT = LEFT;
  this -> RIGHT = RIGHT;
  LEFT.attach(ESC_PIN1, MIN_WIDTH, MAX_WIDTH);
  RIGHT.attach(ESC_PIN2, MIN_WIDTH, MAX_WIDTH);
  delay(2000);
}

void ESC::changeThrottlePercent(int percentage)
{
  THROTTLE_PERC = map(percentage, 0, 100, minThrottle, 180);;
#ifdef DEBUG
  Serial.print("THROTTLE_PERC : ");
  Serial.println(THROTTLE_PERC);
#endif
}

void ESC::move(int region, int angle)
{
  switch (region)
  {
    case 1:
      int right = map(angle, 0, 90, 90, THROTTLE_PERC);
      LEFT_THROTTLE = THROTTLE_PERC;
      RIGHT_THROTTLE = map(angle, 0, 90, minThrottle, THROTTLE_PERC);
      LEFT.write(LEFT_THROTTLE);
      RIGHT.write(RIGHT_THROTTLE);
      break;
    case 2:
      angle = 90 - (angle - 90);
      RIGHT_THROTTLE = THROTTLE_PERC;
      LEFT_THROTTLE = map(angle, 0, 90, minThrottle, THROTTLE_PERC);
      LEFT.write(LEFT_THROTTLE);
      RIGHT.write(RIGHT_THROTTLE);
      break;
    case 3:
      angle = 90 - (angle - 180);
      RIGHT_THROTTLE = THROTTLE_PERC;
      LEFT_THROTTLE = map(angle, 90, 0, minThrottle, 180 - THROTTLE_PERC);
      LEFT.write(LEFT_THROTTLE);
      RIGHT.write(RIGHT_THROTTLE);
      break;
    case 4:
      angle = 90 - (angle - 270);
      LEFT_THROTTLE = THROTTLE_PERC;
      RIGHT_THROTTLE = map(angle, 0, 90, minThrottle, 180 - THROTTLE_PERC);
      LEFT.write(LEFT_THROTTLE);
      RIGHT.write(RIGHT_THROTTLE);
      break;
  }
#ifdef DEBUG
  Serial.print("LEFT_TH : ");
  Serial.print(LEFT_THROTTLE);
  Serial.print(" - ");
  Serial.print("RIGHT_TH : ");
  Serial.println(RIGHT_THROTTLE);
#endif
}

void ESC::stop()
{
  LEFT_THROTTLE = minThrottle;
  RIGHT_THROTTLE = minThrottle;
  LEFT.write(LEFT_THROTTLE);
  RIGHT.write(RIGHT_THROTTLE);
}
