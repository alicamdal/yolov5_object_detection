#ifndef ESC_H
#define ESC_H
#include <Arduino.h>
#include <Servo.h>
#define DEBUG

class ESC
{
  private:
    int ESC_PIN1;
    int ESC_PIN2;
    int MIN_WIDTH;
    int MAX_WIDTH;
    int THROTTLE_PERC;
    int LEFT_THROTTLE;
    int RIGHT_THROTTLE;
    int minThrottle;
    Servo LEFT;
    Servo RIGHT;
  public:
    void escConfig(int ESC_PIN1, int ESC_PIN2, int MIN_WIDTH, int MAX_WIDTH);
    void init();
    void changeThrottlePercent(int percentage);
    void move(int region, int angle);
    void stop();
};

#endif
