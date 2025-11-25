"""
WiFi Status Indicator Module
Monitors WiFi connection and controls status LED
"""

import RPi.GPIO as GPIO
import socket
import threading
import time
from config import WIFI_LED_PIN


class WiFiIndicator:
    """Manages WiFi status LED indicator"""
    
    def __init__(self):
        self.led_pin = WIFI_LED_PIN
        self.running = False
        self.thread = None
        self.check_interval = 2.0  # Check WiFi every 2 seconds
        self.blink_speed = 0.5  # Blink every 0.5 seconds when disconnected
        
        # Initialize GPIO
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.LOW)
    
    def is_connected(self):
        """
        Check if device has internet connectivity
        Returns True if connected, False otherwise
        """
        try:
            # Try to connect to Google's DNS server
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            pass
        
        # Fallback: check if we can resolve a hostname
        try:
            socket.gethostbyname("www.google.com")
            return True
        except socket.gaierror:
            return False
    
    def start(self):
        """Start the WiFi monitoring thread"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        print("WiFi indicator started")
    
    def stop(self):
        """Stop the WiFi monitoring thread"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        GPIO.output(self.led_pin, GPIO.LOW)
        print("WiFi indicator stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop (runs in background thread)"""
        last_check = 0
        blink_state = False
        last_blink = 0
        
        while self.running:
            current_time = time.time()
            
            # Check WiFi status periodically
            if current_time - last_check >= self.check_interval:
                last_check = current_time
                connected = self.is_connected()
                
                if connected:
                    # Solid green when connected
                    GPIO.output(self.led_pin, GPIO.HIGH)
                else:
                    # Blink when disconnected - handled below
                    pass
            
            # Handle blinking when disconnected
            if not self.is_connected():
                if current_time - last_blink >= self.blink_speed:
                    last_blink = current_time
                    blink_state = not blink_state
                    GPIO.output(self.led_pin, GPIO.HIGH if blink_state else GPIO.LOW)
            
            # Small sleep to prevent CPU spinning
            time.sleep(0.1)
    
    def cleanup(self):
        """Clean up GPIO resources"""
        self.stop()


# Global instance
_wifi_indicator = None


def initialize():
    """Initialize the WiFi indicator"""
    global _wifi_indicator
    if _wifi_indicator is None:
        _wifi_indicator = WiFiIndicator()
        _wifi_indicator.start()
    return _wifi_indicator


def cleanup():
    """Clean up WiFi indicator resources"""
    global _wifi_indicator
    if _wifi_indicator:
        _wifi_indicator.cleanup()
        _wifi_indicator = None
