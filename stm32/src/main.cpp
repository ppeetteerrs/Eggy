#include <Arduino.h>
#include <Servo.h>

Servo	 servo1;
Servo	 servo2;
char	 letter;
String	 serialString = "";
String	 serial2;
uint16_t cnt1  = 500;
uint16_t cnt2  = 500;
int		 i	   = 0;
bool	 ready = false;

void setup() {
	Serial.begin(115200);
	servo1.attach(9);
	servo2.attach(10);
	servo1.writeMicroseconds(cnt1);
	servo2.writeMicroseconds(cnt2);
}

void loop() {
	if (ready) {
		// Update servos
		servo2.writeMicroseconds(cnt2);
		servo1.writeMicroseconds(cnt1);
		Serial.print(cnt1);
		Serial.print(" ");
		Serial.println(cnt2);
		serialString = "";
		i			 = 0;
		ready		 = false;
	} else {
		if (i < 10) {
			if (Serial.available() > 0) {
				// Read Serial
				letter = (char)Serial.read();

				if (letter == 'x') {
					serialString = "";
					i			 = 0;
					ready		 = false;
					Serial.println("Reset");
				} else {
					serialString += letter;
					i++;
				}
			}
		} else {
			// Parse counts;
			cnt1  = (uint16_t)serialString.substring(0, 5).toInt();
			cnt2  = (uint16_t)serialString.substring(5, 10).toInt();
			ready = true;
		}
	}
}