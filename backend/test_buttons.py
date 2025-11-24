#!/usr/bin/env python3
"""
Simple button test script for Raspberry Pi GPIO
Tests all 9 button inputs and prints when pressed
"""

import RPi.GPIO as GPIO
import time

# Button pins (BCM numbering)
BUTTON_PINS = {
    0: 17,  # Top-Left
    1: 27,  # Top-Center
    2: 4,   # Top-Right (changed from 22 - more reliable)
    3: 23,  # Mid-Left
    4: 24,  # Mid-Center
    5: 25,  # Mid-Right
    6: 12,  # Bottom-Left (changed from 5 - more reliable)
    7: 6,   # Bottom-Center
    8: 13,  # Bottom-Right
}

def main():
    # Setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Configure all button pins
    for position, pin in BUTTON_PINS.items():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    print("=" * 60)
    print("GPIO Button Test - Press buttons to test")
    print("=" * 60)
    print("\nButton Layout:")
    print("  [0] [1] [2]    GPIO: [17] [27] [4]")
    print("  [3] [4] [5]    GPIO: [23] [24] [25]")
    print("  [6] [7] [8]    GPIO: [12] [6]  [13]")
    print("\nPress Ctrl+C to exit\n")
    
    # Track previous states
    button_states = {pos: GPIO.HIGH for pos in BUTTON_PINS.keys()}
    last_press_time = {pos: 0 for pos in BUTTON_PINS.keys()}
    
    try:
        while True:
            for position, pin in BUTTON_PINS.items():
                current_state = GPIO.input(pin)
                
                # Detect button press (HIGH to LOW transition)
                if button_states[position] == GPIO.HIGH and current_state == GPIO.LOW:
                    current_time = time.time()
                    # Debounce: only register if 200ms has passed
                    if current_time - last_press_time[position] >= 0.2:
                        last_press_time[position] = current_time
                        print(f"✓ Button {position} pressed (GPIO {pin})")
                
                button_states[position] = current_state
            
            time.sleep(0.01)  # Poll every 10ms
            
    except KeyboardInterrupt:
        print("\n\nCleaning up...")
        GPIO.cleanup()
        print("Done!")

if __name__ == "__main__":
    main()
