#include "ESC.h"
#define ESC1 3
#define ESC2 5
#define MIN_WIDTH 1000
#define MAX_WIDTH 2000
ESC ESCs;

bool trigger = false;
String msg = "";
String oldMsg = "";

void setup() {
  Serial.begin(115200);

#ifdef DEBUG
  Serial.println("---------------- Initializing ESCs -------------------");
#endif
  ESCs.escConfig(ESC1, ESC2, MIN_WIDTH, MAX_WIDTH);
#ifdef DEBUG
  Serial.println("Config Done");
#endif

  ESCs.init();

#ifdef DEBUG
  Serial.println("Initializing Done");
#endif
}

void loop() {
  if (trigger) {
#ifdef DEBUG
    Serial.println(msg);
#endif
    if (msg.compareTo(oldMsg) != 0) {
      if (msg.charAt(0) == 't') {
        int th = msg.substring(1).toInt();
        ESCs.changeThrottlePercent(th);
      } else {
        String region = msg.substring(0, 1);
        String angle = msg.substring(msg.indexOf(',') + 1);
        if (angle.compareTo("-1\n") == 0)
        {
          ESCs.stop();
        }
        else
        {
          ESCs.move(region.toInt(), angle.toInt());
        }
      }
      oldMsg = msg;
    }
    msg = "";
    trigger = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    msg += inChar;
    if (inChar == '\n') {
      trigger = true;
    }
  }
}
