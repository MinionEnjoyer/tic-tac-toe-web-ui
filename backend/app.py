#!/usr/bin/env python3
"""
Flask Server for Tic-Tac-Toe Web UI
Provides WebSocket API and serves React frontend
"""

from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
import time
from threading import Thread

from game_controller import GameController
from gpio_handler import GPIOHandler
from config import SERVER_HOST, SERVER_PORT, DEBUG

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app)  # Enable CORS for development
app.config['SECRET_KEY'] = 'tic-tac-toe-secret-key'

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize game components
game = GameController()

# Initialize GPIO handler immediately (not waiting for client connection)
gpio = None
try:
    print("Initializing GPIO handler...")
    gpio = GPIOHandler(button_callback=lambda pos: on_button_press(pos))
    gpio.set_turn_indicator('X')
    print("GPIO handler initialized successfully!")
except Exception as e:
    print(f"Warning: Could not initialize GPIO: {e}")
    print("GPIO buttons will not work, but web interface will still function")
    # Create a dummy GPIO handler for testing
    gpio = type('DummyGPIO', (), {
        'set_turn_indicator': lambda self, p: print(f"LED: {p}"),
        'flash_winner': lambda self, p: print(f"Flash: {p}"),
        'turn_off_all_leds': lambda self: print("LEDs off"),
        'cleanup': lambda self: None
    })()


def on_button_press(position):
    """
    Callback for physical button press.
    
    Args:
        position: Board position (0-8) that was pressed
    """
    print(f"Physical button pressed at position {position}")
    
    # Make the move
    result = game.make_move(position)
    
    if result is None:
        # Invalid move
        socketio.emit('invalid_move', {'position': position}, broadcast=True)
        return
    
    # Update turn indicator LED
    if result['game_over']:
        if result['winner']:
            # Flash winner's LED in a separate thread
            def flash_led():
                time.sleep(0.5)  # Small delay before flashing
                gpio.flash_winner(result['winner'])
            Thread(target=flash_led, daemon=True).start()
        else:
            # Draw - turn off both LEDs
            gpio.turn_off_all_leds()
    else:
        # Set LED for next player
        gpio.set_turn_indicator(result['next_player'])
    
    # Broadcast move to all connected clients
    socketio.emit('move_made', result, broadcast=True)
    
    # Auto-reset after game over
    if result['game_over']:
        def reset_game():
            time.sleep(3)  # Wait 3 seconds before reset
            game.reset_game()
            gpio.set_turn_indicator('X')
            socketio.emit('game_reset', game.get_game_state(), broadcast=True)
        Thread(target=reset_game, daemon=True).start()


@app.route('/')
def serve_frontend():
    """Serve the React frontend."""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from React build."""
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    global gpio
    
    print('Client connected')
    
    # Initialize GPIO handler on first connection
    if gpio is None:
        try:
            gpio = GPIOHandler(button_callback=on_button_press)
            gpio.set_turn_indicator('X')
        except Exception as e:
            print(f"Warning: Could not initialize GPIO (not on Raspberry Pi?): {e}")
            # Create a dummy GPIO handler for testing
            gpio = type('DummyGPIO', (), {
                'set_turn_indicator': lambda self, p: print(f"LED: {p}"),
                'flash_winner': lambda self, p: print(f"Flash: {p}"),
                'turn_off_all_leds': lambda self: print("LEDs off"),
                'cleanup': lambda self: None
            })()
    
    # Send current game state to the newly connected client
    emit('game_state', game.get_game_state())


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print('Client disconnected')


@socketio.on('reset_game')
def handle_reset():
    """Handle game reset request from client."""
    print('Game reset requested')
    game.reset_game()
    if gpio:
        gpio.set_turn_indicator('X')
    emit('game_reset', game.get_game_state(), broadcast=True)


@socketio.on('request_state')
def handle_state_request():
    """Handle request for current game state."""
    emit('game_state', game.get_game_state())


def cleanup():
    """Cleanup resources on shutdown."""
    if gpio:
        gpio.cleanup()


if __name__ == '__main__':
    try:
        print("=" * 60)
        print("Tic-Tac-Toe Web Server Starting...")
        print(f"Server: http://{SERVER_HOST}:{SERVER_PORT}")
        print(f"Access from other devices: http://<raspberry-pi-ip>:{SERVER_PORT}")
        print("=" * 60)
        
        # Run the server
        socketio.run(
            app,
            host=SERVER_HOST,
            port=SERVER_PORT,
            debug=DEBUG,
            allow_unsafe_werkzeug=True
        )
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        cleanup()
