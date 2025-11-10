# Tic-Tac-Toe Web UI

A web-based Tic-Tac-Toe game for Raspberry Pi Zero 2 W with physical GPIO button controls and turn indicator LEDs. The game is accessible via web browser on any device connected to the same network (LAN).

## Features

- **Physical GPIO Controls**: 9 buttons for game input
- **Web Interface**: Responsive React UI that works on desktop and mobile
- **Real-Time Sync**: WebSocket communication for instant updates
- **Turn Indicators**: Physical Red/Blue LEDs + on-screen indicators
- **Cross-Platform**: Access from any device on your local network
- **Responsive Design**: Optimized for mobile and desktop viewing
- **Animations**: Smooth CSS animations for wins and draws

## Hardware Components

### GPIO Components
- **9× Momentary Push Buttons** - Game input (one per grid position)
- **2× LEDs** - Turn indicators (Red for Player X, Blue for Player O)
- **Resistors** - For LED current limiting

### GPIO Pin Configuration (BCM Numbering)

**Button Inputs:**
```
Position 0 (Top-Left):     GPIO 17
Position 1 (Top-Center):   GPIO 27
Position 2 (Top-Right):    GPIO 22
Position 3 (Mid-Left):     GPIO 23
Position 4 (Mid-Center):   GPIO 24
Position 5 (Mid-Right):    GPIO 25
Position 6 (Bottom-Left):  GPIO 5
Position 7 (Bottom-Center): GPIO 6
Position 8 (Bottom-Right):  GPIO 13
```

**Turn Indicator LEDs:**
```
Red LED (Player X):  GPIO 16
Blue LED (Player O): GPIO 20
```

## Software Architecture

### Backend (Python Flask)
- Flask web server with SocketIO for WebSockets
- GPIO handler for button inputs and LED control
- Game controller with win/draw detection
- Serves React frontend build

### Frontend (React)
- Responsive game board UI
- Real-time WebSocket client
- Turn indicators and game status display
- Mobile and desktop optimized

## Installation

### 1. System Setup

Update your Raspberry Pi:
```bash
sudo apt update && sudo apt upgrade -y
```

Install system dependencies:
```bash
sudo apt install -y python3-pip python3-dev python3-venv nodejs npm
```

### 2. Clone Repository

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/tic-tac-toe-web-ui.git
cd tic-tac-toe-web-ui
```

### 3. Backend Setup

Navigate to backend directory:
```bash
cd backend
```

Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 4. Frontend Setup

Navigate to frontend directory:
```bash
cd ../frontend
```

Install Node dependencies:
```bash
npm install
```

Build the React app:
```bash
npm run build
```

## Running the Application

### Production Mode (Recommended)

From the backend directory with venv activated:
```bash
cd backend
source venv/bin/activate
sudo -E python3 app.py
```

The server will start on port 5000 and be accessible across your LAN.

### Development Mode

For development with hot-reload:

Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate
python3 app.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Frontend will run on port 3000 and proxy to backend on port 5000.

## Accessing the Game

### On the Raspberry Pi
```
http://localhost:5000
```

### From Other Devices (Phone, Tablet, Computer)

Find your Raspberry Pi's IP address:
```bash
hostname -I
```

Then access from any device on the same network:
```
http://192.168.1.XXX:5000
```

Replace `192.168.1.XXX` with your Pi's actual IP address.

## How to Play

1. **Start the server** on your Raspberry Pi
2. **Open the web interface** on your phone/device
3. **Press physical buttons** on the hardware to make moves
4. **Watch the screen update** in real-time
5. **Turn LEDs indicate** whose turn it is (Red=X, Blue=O)
6. **Win/Draw** animations display on screen
7. **Auto-reset** after 3 seconds

## Project Structure

```
tictactoe-web-ui/
├── backend/
│   ├── app.py              # Flask server with SocketIO
│   ├── game_controller.py  # Game logic
│   ├── gpio_handler.py     # Button and LED control
│   ├── config.py           # Configuration
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── components/     # React components
│   │   │   ├── GameBoard.jsx
│   │   │   ├── Square.jsx
│   │   │   ├── TurnIndicator.jsx
│   │   │   └── GameStatus.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## API / WebSocket Events

### Server → Client Events
- `game_state` - Full game state on connection
- `move_made` - Sent when a move is made
- `game_reset` - Sent when game is reset
- `invalid_move` - Sent when invalid move attempted

### Client → Server Events
- `reset_game` - Request to reset the game
- `request_state` - Request current game state

## Troubleshooting

### Cannot Access from Phone

1. Check both devices are on same WiFi network
2. Verify Raspberry Pi's IP address: `hostname -I`
3. Check firewall settings: `sudo ufw status`
4. Try disabling firewall temporarily: `sudo ufw disable`

### GPIO Buttons Not Working

1. Verify wiring matches pin configuration in `backend/config.py`
2. Check button connections (button should connect GPIO to GND)
3. Ensure script is run with `sudo` for GPIO access
4. Test buttons individually with a multimeter

### LEDs Not Working

1. Verify LED polarity (long leg = positive)
2. Check resistor values (typically 220Ω - 330Ω)
3. Confirm LED pins match configuration
4. Test LEDs with a simple GPIO test script

### Web Interface Not Loading

1. Check Flask server is running: `ps aux | grep python`
2. Verify frontend was built: `ls frontend/build`
3. Check server logs for errors
4. Rebuild frontend: `cd frontend && npm run build`

### WebSocket Connection Issues

1. Check browser console for errors
2. Verify SocketIO versions match between frontend and backend
3. Try different browser
4. Check if port 5000 is available: `sudo netstat -tulpn | grep 5000`

## Auto-Start on Boot (Optional)

Create a systemd service:

```bash
sudo nano /etc/systemd/system/tictactoe.service
```

Add:
```ini
[Unit]
Description=Tic-Tac-Toe Web UI
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/tic-tac-toe-web-ui/backend
ExecStart=/home/pi/tic-tac-toe-web-ui/backend/venv/bin/python /home/pi/tic-tac-toe-web-ui/backend/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable tictactoe
sudo systemctl start tictactoe
```

## Development

### Modifying Button Pins
Edit `backend/config.py` and update `BUTTON_PINS` dictionary.

### Changing Colors
Edit component CSS files in `frontend/src/components/`

### Adjusting Game Logic
Modify `backend/game_controller.py`

## Credits

A big thanks to my Dad, Mache Creeger, and to the Cascadia College Students and Teachers!

## License

This project is for educational purposes. Feel free to modify and improve!
