#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# 🤖 .agents - Quick Run Script
# ═══════════════════════════════════════════════════════════════
# This script checks if the project is installed, and if not,
# runs the installer in dev mode, then launches the program.
# ═══════════════════════════════════════════════════════════════

set -e  # Exit on any error

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🤖 .agents - Quick Run${NC}\n"

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo -e "${YELLOW}Poetry not found. Running installer...${NC}\n"
    chmod +x install.sh
    ./install.sh
    exit 0
fi

# Check if dependencies are installed
if ! poetry env info &> /dev/null || ! poetry run python -c "import rich" &> /dev/null 2>&1; then
    echo -e "${YELLOW}Dependencies not installed. Running installer...${NC}\n"
    chmod +x install.sh
    ./install.sh
    exit 0
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found!${NC}"
    if [ -f ".env.sample" ]; then
        echo "Creating .env from .env.sample..."
        cp .env.sample .env
        echo -e "${YELLOW}IMPORTANT: Edit .env and set your MASTER_PASSWORD!${NC}"
        echo "Run: nano .env"
        echo ""
        read -p "Press Enter after editing .env to continue..."
    else
        echo -e "${YELLOW}Please create a .env file with your configuration${NC}"
        exit 1
    fi
fi

# Run the program
echo -e "${GREEN}Starting .agents...${NC}\n"
poetry run python -m src.main
