#!/bin/bash
# Setup script for Tic-Tac-Toe Web UI
# Run with: bash setup.sh

echo "=========================================="
echo "Tic-Tac-Toe Web UI - Setup Script"
echo "=========================================="
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo "Warning: This doesn't appear to be a Raspberry Pi"
    echo "GPIO functionality will not work, but you can still test the web interface"
    echo ""
fi

echo "Step 1: Updating system packages..."
sudo apt update

echo ""
echo "Step 2: Installing system dependencies..."
sudo apt install -y python3-pip python3-dev python3-venv nodejs npm

echo ""
echo "Step 3: Setting up Python backend..."
cd backend

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Step 4: Setting up React frontend..."
cd ../frontend

echo "Installing Node dependencies..."
npm install

echo "Building React app..."
npm run build

cd ..

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start the server:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  sudo -E python3 app.py"
echo ""
echo "Then access from any device on your network:"
echo "  http://<raspberry-pi-ip>:5000"
echo ""
echo "Find your Pi's IP with: hostname -I"
echo ""
echo "See README.md for complete documentation."
echo "=========================================="
