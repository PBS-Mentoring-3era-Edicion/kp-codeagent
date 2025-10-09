#!/bin/bash

# KP Code Agent - Installation Script for Linux/macOS/WSL
# This script installs all dependencies and sets up KP Code Agent

set -e  # Exit on error

echo "========================================"
echo "KP Code Agent - Installation Script"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check Python
echo "[1/4] Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}[OK]${NC} $PYTHON_VERSION found"
else
    echo -e "${RED}[ERROR]${NC} Python 3 not found!"
    echo ""
    echo "Please install Python 3.10 or higher:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi
echo ""

# Step 2: Check Ollama
echo "[2/4] Checking Ollama installation..."
if curl -s http://localhost:11434 > /dev/null 2>&1; then
    echo -e "${GREEN}[OK]${NC} Ollama is running"
else
    echo -e "${YELLOW}[WARNING]${NC} Ollama is not running or not installed."
    echo ""
    read -p "Would you like to install Ollama now? (y/N): " INSTALL_OLLAMA

    if [[ "$INSTALL_OLLAMA" =~ ^[Yy]$ ]]; then
        echo "Installing Ollama..."
        curl -fsSL https://ollama.ai/install.sh | sh

        echo "Starting Ollama service..."
        if command -v systemctl &> /dev/null; then
            sudo systemctl start ollama
        else
            # For macOS or systems without systemd
            ollama serve &
            sleep 3
        fi
    else
        echo -e "${YELLOW}[WARNING]${NC} Ollama is required for KP Code Agent to work."
        echo "Please install it from: https://ollama.ai/download"
        echo "Then run this installer again."
        exit 1
    fi
fi
echo ""

# Step 3: Install KP Code Agent
echo "[3/4] Installing KP Code Agent..."
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Upgrade pip
python3 -m pip install --upgrade pip --quiet

# Install KP Code Agent
if [ -f "$SCRIPT_DIR/../requirements.txt" ]; then
    echo "Installing from requirements.txt..."
    python3 -m pip install -r "$SCRIPT_DIR/../requirements.txt" --quiet
else
    echo "Installing from package..."
    python3 -m pip install kp-codeagent --quiet
fi

echo -e "${GREEN}[OK]${NC} KP Code Agent installed successfully"
echo ""

# Step 4: Download CodeLlama model
echo "[4/4] Setting up CodeLlama model..."
echo "This will download approximately 4GB of data."
echo "It may take 5-15 minutes depending on your internet connection."
echo ""

read -p "Download CodeLlama 7B model now? (y/N): " DOWNLOAD_MODEL

if [[ "$DOWNLOAD_MODEL" =~ ^[Yy]$ ]]; then
    echo ""
    echo "Downloading CodeLlama 7B model..."
    echo "Please be patient, this will take a while..."
    echo ""

    if ollama pull codellama:7b; then
        echo -e "${GREEN}[OK]${NC} Model downloaded successfully"
    else
        echo -e "${YELLOW}[WARNING]${NC} Model download failed or was interrupted."
        echo "You can download it later by running:"
        echo "  ollama pull codellama:7b"
    fi
else
    echo ""
    echo -e "${YELLOW}[INFO]${NC} Model download skipped."
    echo "You'll need to download it before using KP Code Agent:"
    echo "  ollama pull codellama:7b"
fi
echo ""

echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "KP Code Agent is now installed."
echo ""
echo "Quick Start:"
echo "  1. Open a new terminal window"
echo "  2. Navigate to your project folder"
echo "  3. Run: kp-codeagent \"your task here\""
echo ""
echo "Examples:"
echo "  kp-codeagent \"create a Python function to calculate fibonacci\""
echo "  kp-codeagent \"add error handling to my code\""
echo ""
echo "For help: kp-codeagent --help"
echo "To check setup: kp-codeagent check"
echo ""
echo "========================================"
