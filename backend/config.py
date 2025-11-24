"""
Configuration file for Tic-Tac-Toe Web UI
GPIO pin assignments and server settings
"""

# Server Configuration
# ====================

# Flask server settings - bind to 0.0.0.0 for LAN access
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
DEBUG = True

# GPIO Pin Assignments (BCM numbering)
# =====================================

# Button Input Pins (9 buttons for 9 grid positions)
# Buttons connect GPIO to GND when pressed (pull-up resistors enabled)
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

# Turn Indicator LED Pins
TURN_LED_PINS = {
    'X': 16,  # Red LED for Player X (GPIO16)
    'O': 20,  # Blue LED for Player O (GPIO20)
}

# Button Configuration
# ====================

# Button debounce time in seconds
BUTTON_DEBOUNCE = 0.2

# Game Configuration
# ==================

# Animation timing for LED flashing on win
WIN_LED_FLASH_COUNT = 5
WIN_LED_FLASH_DELAY = 0.2  # seconds
