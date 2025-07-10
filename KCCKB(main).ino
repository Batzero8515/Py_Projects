#include <HID-Project.h>

const int buttons[] = {10, 16, 14, 15, 9};  // Updated button pins
bool buttonState[] = {HIGH, HIGH, HIGH, HIGH, HIGH};  // Tracks previous state

void setup() {
    for (int i = 0; i < 5; i++) {
        pinMode(buttons[i], INPUT_PULLUP);
    }
    Keyboard.begin();
}

void loop() {
    for (int i = 0; i < 5; i++) {
        bool currentState = digitalRead(buttons[i]);

        if (currentState == LOW && buttonState[i] == HIGH) {  // Detect button press
            switch (buttons[i]) {
                case 9:
                    Keyboard.write(KEY_ENTER);  // Enter key
                    break;
                case 10:
                    Keyboard.write(KEY_RIGHT_ARROW);  // Right arrow
                    break;
                case 16:
                    Keyboard.write(KEY_DOWN_ARROW);  // Down arrow
                    break;
                case 15:
                    Keyboard.write('~');  // '~' character
                    break;
                case 14:
                    Keyboard.write('~');  // '~' character (for button 9)
                    break;
            }

            delay(100);  // Debounce delay
        }

        buttonState[i] = currentState;  // Update button state
    }
}
