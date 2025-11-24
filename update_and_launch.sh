#!/bin/bash
#
# Auto-Update and Launch Script for Tic-Tac-Toe Web UI
# This script checks for updates from GitHub and launches the Flask server
#

set -e  # Exit on error

# Configuration
PROJECT_DIR="/home/pi/tic-tac-toe-web-ui"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
LOG_FILE="/var/log/tictactoe-update.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log "${BLUE}============================================================${NC}"
log "${BLUE}  Tic-Tac-Toe Web UI - Auto-Update & Launch${NC}"
log "${BLUE}============================================================${NC}"

# Change to project directory
cd "$PROJECT_DIR" || exit 1

# Get current version
CURRENT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
log "${GREEN}📍 Current Version: ${CURRENT_COMMIT}${NC}"

# Fetch latest from GitHub
log "${YELLOW}🔍 Checking for updates from GitHub...${NC}"
git fetch origin main 2>&1 | tee -a "$LOG_FILE"

# Get remote version
REMOTE_COMMIT=$(git rev-parse --short origin/main 2>/dev/null || echo "unknown")
log "${GREEN}📡 Remote Version:  ${REMOTE_COMMIT}${NC}"

# Check if update is needed
if [ "$CURRENT_COMMIT" != "$REMOTE_COMMIT" ]; then
    log "${YELLOW}🔄 UPDATE AVAILABLE - Updating...${NC}"
    
    # Reset any local changes and pull latest
    git reset --hard HEAD 2>&1 | tee -a "$LOG_FILE"
    git clean -fd 2>&1 | tee -a "$LOG_FILE"
    git pull origin main 2>&1 | tee -a "$LOG_FILE"
    
    # Check if requirements.txt changed
    if git diff --name-only "$CURRENT_COMMIT" "$REMOTE_COMMIT" | grep -q "backend/requirements.txt"; then
        log "${YELLOW}📦 Requirements changed - Updating Python dependencies...${NC}"
        cd "$BACKEND_DIR"
        source venv/bin/activate
        pip install -r requirements.txt 2>&1 | tee -a "$LOG_FILE"
        deactivate
        cd "$PROJECT_DIR"
    fi
    
    # Check if frontend files changed
    if git diff --name-only "$CURRENT_COMMIT" "$REMOTE_COMMIT" | grep -q "frontend/"; then
        log "${YELLOW}🎨 Frontend changed - Rebuilding React app...${NC}"
        cd "$FRONTEND_DIR"
        npm install 2>&1 | tee -a "$LOG_FILE"
        npm run build 2>&1 | tee -a "$LOG_FILE"
        cd "$PROJECT_DIR"
    fi
    
    NEW_COMMIT=$(git rev-parse --short HEAD)
    log "${GREEN}✅ UPDATE COMPLETE - New version: ${NEW_COMMIT}${NC}"
else
    log "${GREEN}✅ Already up to date${NC}"
fi

# Launch the application
log "${BLUE}🚀 LAUNCHING Flask Server...${NC}"
log "${BLUE}   Server will be available at: http://192.168.19.120:5000${NC}"
log "${BLUE}============================================================${NC}"

# Start the Flask server
cd "$BACKEND_DIR"
exec ./venv/bin/python3 app.py 2>&1 | tee -a "$LOG_FILE"
