#include <Arduino.h>
#include <Servo.h>

/* -------------------------------- Settings -------------------------------- */
#define SEC_PER_REV 8
#define INC			(4000 / SEC_PER_REV / 50)  // 4000 steps = 360 degrees, 50Hz update rate, INC = steps / update to achieve desired RPM

/* --------------------------------- Macros --------------------------------- */
// Servo Pins 9 and 10 (OC1A, OC1B)
#define LEFT_PIN  0b00000010
#define RIGHT_PIN 0b00000100

/* -------------------------------- Functions ------------------------------- */
// Setup
void setup() {
	Serial.begin(115200);
	// Set servo pins to OUTPUT mode
	DDRB |= LEFT_PIN | RIGHT_PIN;
	// Setup Timer 1 Control Registers
	// COM1A1:0 = COM1B1:0 = 0b10 - Non-inverting PWM Mode
	// WGM13:10 = 14 - Fast PWM Mode with TOP = ICR1
	// PWM Frequency: 50Hz
	// Prescaler = 8, TOP = 40000 - 1
	TCCR1A = _BV(COM1A1) | _BV(COM1B1) | _BV(WGM11);
	TCCR1B = (TCCR1B & 0b11000000) | _BV(WGM13) | _BV(WGM12) | _BV(CS11);
	ICR1   = 40000 - 1;
	// Enable Timer Interrupt
	TIMSK1 = (TIMSK1 & 0b11111000) | 0b001;
	// Set initial position to (700, 700)
	OCR1A = 1400;
	OCR1B = 1400;
}

void loop() {
}

ISR(TIMER1_OVF_vect) {
	if (Serial.available() > 1) {
		int left  = (Serial.read() - '1') * INC;
		int right = (Serial.read() - '1') * INC;
		OCR1A += left;
		OCR1B += right;
	}
}