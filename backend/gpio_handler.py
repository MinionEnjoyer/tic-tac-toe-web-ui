"""
GPIO Handler for Tic-Tac-Toe Web UI
Manages button inputs and turn indicator LEDs
"""

import RPi.GPIO as GPIO
import time
from config import BUTTON_PINS, TURN_LED_PINS, BUTTON_DEBOUNCE, WIN_LED_FLASH_COUNT, WIN_LED_FLASH_DELAY


class GPIOHandler:
    """Manages GPIO operations for buttons and LEDs."""
    
    def __init__(self, button_callback=None):
        """
        Initialize GPIO handler.
        
        Args:
            button_callback: Function to call when button is pressed (receives position)
        """
        self.button_callback = button_callback
        self.last_press_time = {}
        
        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Configure button pins as inputs with pull-up resistors
        for position, pin in BUTTON_PINS.items():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.last_press_time[position] = 0
        
        # Start polling thread for button detection
        self.button_states = {pos: GPIO.HIGH for pos in BUTTON_PINS.keys()}
        self.running = True
        import threading
        self.poll_thread = threading.Thread(target=self._poll_buttons, daemon=True)
        self.poll_thread.start()
        
        # Configure LED pins as outputs
        for player, pin in TURN_LED_PINS.items():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)  # Start with LEDs off
        
        print("GPIO handler initialized")
    
    def _poll_buttons(self):
        """Poll button states in a loop (replaces edge detection)."""
        print("Button polling started")
        while self.running:
            for position, pin in BUTTON_PINS.items():
                current_state = GPIO.input(pin)
                
                # Button pressed when state goes from HIGH to LOW (pull-up resistor)
                if self.button_states[position] == GPIO.HIGH and current_state == GPIO.LOW:
                    # Check debounce
                    current_time = time.time()
                    if current_time - self.last_press_time[position] >= BUTTON_DEBOUNCE:
                        self.last_press_time[position] = current_time
                        print(f"[DEBUG] Button pressed: Position {position} (GPIO {pin})")
                        
                        # Call the user callback
                        if self.button_callback:
                            self.button_callback(position)
                
                # Update state
                self.button_states[position] = current_state
            
            # Small delay to avoid consuming too much CPU
            time.sleep(0.01)  # Poll every 10ms
    
    def set_turn_indicator(self, player):
        """
        Set the turn indicator LED for the current player.
        
        Args:
            player: 'X' or 'O'
        """
        if player == 'X':
            # Turn on red LED, turn off blue LED
            GPIO.output(TURN_LED_PINS['X'], GPIO.HIGH)
            GPIO.output(TURN_LED_PINS['O'], GPIO.LOW)
            print("Turn indicator: Player X (Red)")
        elif player == 'O':
            # Turn on blue LED, turn off red LED
            GPIO.output(TURN_LED_PINS['X'], GPIO.LOW)
            GPIO.output(TURN_LED_PINS['O'], GPIO.HIGH)
            print("Turn indicator: Player O (Blue)")
    
    def flash_winner(self, player):
        """
        Flash the winning player's LED.
        
        Args:
            player: 'X' or 'O'
        """
        pin = TURN_LED_PINS.get(player)
        if pin is None:
            return
        
        print(f"Flashing winner LED: Player {player}")
        for _ in range(WIN_LED_FLASH_COUNT):
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(WIN_LED_FLASH_DELAY)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(WIN_LED_FLASH_DELAY)
    
    def turn_off_all_leds(self):
        """Turn off both indicator LEDs."""
        for pin in TURN_LED_PINS.values():
            GPIO.output(pin, GPIO.LOW)
        print("Turn indicators off")
    
    def cleanup(self):
        """Clean up GPIO resources."""
        print("Cleaning up GPIO handler")
        self.turn_off_all_leds()
        GPIO.cleanup()
