#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# 🤖 .agents - Easy Installer for Beginners
# ═══════════════════════════════════════════════════════════════

set -e  # Exit on any error

# Colors for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# ═══════════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════════

print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    🤖 .agents Installer                        ║"
    echo "║            WhatsApp to Social Media Automation                 ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_step() {
    echo -e "\n${MAGENTA}${BOLD}▶ $1${NC}"
}

# ═══════════════════════════════════════════════════════════════
# System Detection
# ═══════════════════════════════════════════════════════════════

detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/debian_version ]; then
            OS="debian"
            PACKAGE_MANAGER="apt"
        elif [ -f /etc/redhat-release ]; then
            OS="redhat"
            PACKAGE_MANAGER="yum"
        elif [ -f /etc/arch-release ]; then
            OS="arch"
            PACKAGE_MANAGER="pacman"
        else
            OS="linux"
            PACKAGE_MANAGER="unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        PACKAGE_MANAGER="brew"
    else
        OS="unknown"
        PACKAGE_MANAGER="unknown"
    fi
}

# ═══════════════════════════════════════════════════════════════
# Dependency Checking
# ═══════════════════════════════════════════════════════════════

check_command() {
    command -v "$1" >/dev/null 2>&1
}

check_python() {
    if check_command python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
            print_success "Python $PYTHON_VERSION detected"
            return 0
        else
            print_warning "Python $PYTHON_VERSION found, but we need Python 3.10 or higher"
            return 1
        fi
    else
        print_warning "Python 3 not found"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════
# Installation Functions
# ═══════════════════════════════════════════════════════════════

install_python() {
    print_step "Installing Python 3.10+"
    
    case $OS in
        debian)
            print_info "Installing Python using apt..."
            sudo apt update
            sudo apt install -y python3.10 python3.10-venv python3-pip
            ;;
        macos)
            if ! check_command brew; then
                print_info "Installing Homebrew first..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            print_info "Installing Python using brew..."
            brew install python@3.10
            ;;
        *)
            print_error "Automatic Python installation not supported on your OS"
            print_info "Please install Python 3.10+ manually from: https://www.python.org/downloads/"
            exit 1
            ;;
    esac
    
    if check_python; then
        print_success "Python installed successfully!"
    else
        print_error "Python installation failed"
        exit 1
    fi
}

install_poetry() {
    print_step "Installing Poetry (dependency manager)"
    
    if check_command poetry; then
        print_success "Poetry is already installed"
        return 0
    fi
    
    print_info "Downloading Poetry installer..."
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Add Poetry to PATH for this session
    export PATH="$HOME/.local/bin:$PATH"
    
    # Add Poetry to PATH permanently
    if [[ "$SHELL" == *"zsh"* ]]; then
        SHELL_RC="$HOME/.zshrc"
    else
        SHELL_RC="$HOME/.bashrc"
    fi
    
    if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_RC"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        print_info "Added Poetry to $SHELL_RC"
    fi
    
    if check_command poetry; then
        print_success "Poetry installed successfully!"
        poetry --version
    else
        print_error "Poetry installation failed"
        print_info "Try running: source $SHELL_RC"
        exit 1
    fi
}

install_dependencies() {
    print_step "Installing project dependencies"
    
    print_info "This might take 2-5 minutes... ☕"
    
    if [ "$1" = "dev" ]; then
        poetry install --with dev
    else
        poetry install --only main
    fi
    
    print_success "All dependencies installed!"
}

setup_environment() {
    print_step "Setting up environment configuration"
    
    if [ -f ".env" ]; then
        print_warning ".env file already exists"
        read -p "Do you want to overwrite it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Keeping existing .env file"
            return 0
        fi
    fi
    
    if [ -f ".env.sample" ]; then
        cp .env.sample .env
        print_success "Created .env file from template"
        print_warning "IMPORTANT: Edit .env file and set your MASTER_PASSWORD!"
        print_info "Run: nano .env"
    else
        print_warning ".env.sample not found, creating a basic .env"
        cat > .env << 'EOF'
# Master password for encryption (CHANGE THIS!)
MASTER_PASSWORD=please-change-this-to-a-very-secure-password-at-least-20-characters

# How often to check WhatsApp groups (in minutes)
CHECK_INTERVAL_MINUTES=5

# Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Storage paths
AGENTS_DIR=.agents
TMP_DIR=.agents/tmp
BUILD_DIR=.agents/build
EOF
        print_success "Created basic .env file"
        print_warning "IMPORTANT: Edit .env file and change the MASTER_PASSWORD!"
    fi
}

create_alias() {
    print_step "Creating global command '.agents'"
    
    CURRENT_DIR=$(pwd)
    
    if [[ "$SHELL" == *"zsh"* ]]; then
        SHELL_RC="$HOME/.zshrc"
    else
        SHELL_RC="$HOME/.bashrc"
    fi
    
    ALIAS_CMD="alias .agents='cd $CURRENT_DIR && poetry run python -m src.main'"
    
    if grep -q "alias .agents=" "$SHELL_RC"; then
        print_warning "Alias .agents already exists in $SHELL_RC"
        sed -i.bak "s|alias \.agents=.*|$ALIAS_CMD|" "$SHELL_RC"
        print_success "Updated existing alias"
    else
        echo "" >> "$SHELL_RC"
        echo "# .agents automation tool" >> "$SHELL_RC"
        echo "$ALIAS_CMD" >> "$SHELL_RC"
        print_success "Added alias to $SHELL_RC"
    fi
    
    print_info "You can now run '.agents' from anywhere!"
    print_warning "Restart your terminal or run: source $SHELL_RC"
}

# ═══════════════════════════════════════════════════════════════
# Main Installation Flow
# ═══════════════════════════════════════════════════════════════

main() {
    clear
    print_header
    
    # Detect OS
    detect_os
    print_info "Detected OS: $OS"
    
    # Ask installation mode
    echo -e "\n${BOLD}Choose installation mode:${NC}"
    echo "1) Developer Mode  - Full development environment with all tools"
    echo "2) User Mode       - Minimal installation for running the tool"
    echo ""
    read -p "Enter your choice (1 or 2): " -n 1 -r MODE
    echo -e "\n"
    
    case $MODE in
        1)
            INSTALL_MODE="dev"
            print_info "Installing in Developer Mode"
            ;;
        2)
            INSTALL_MODE="user"
            print_info "Installing in User Mode"
            ;;
        *)
            print_error "Invalid choice. Defaulting to User Mode"
            INSTALL_MODE="user"
            ;;
    esac
    
    # Check and install Python
    if ! check_python; then
        print_warning "Python 3.10+ is required"
        read -p "Install Python automatically? (Y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            install_python
        else
            print_error "Cannot continue without Python 3.10+"
            exit 1
        fi
    fi
    
    # Install Poetry
    if ! check_command poetry; then
        install_poetry
    else
        print_success "Poetry is already installed"
    fi
    
    # Install project dependencies
    install_dependencies $INSTALL_MODE
    
    # Setup environment
    setup_environment
    
    # Create global alias
    if [ "$INSTALL_MODE" = "user" ]; then
        read -p "Create global '.agents' command? (Y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            create_alias
        fi
    fi
    
    # Installation complete
    echo -e "\n${GREEN}${BOLD}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║              ✓ Installation Complete! 🎉                      ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    print_info "Next steps:"
    echo "  1. Edit .env file: nano .env"
    echo "  2. Set a strong MASTER_PASSWORD"
    if [ "$INSTALL_MODE" = "dev" ]; then
        echo "  3. Run the tool: poetry run python -m src.main"
    else
        echo "  3. Restart your terminal or run: source ~/.bashrc"
        echo "  4. Run the tool from anywhere: .agents"
    fi
    
    echo ""
    read -p "Do you want to run the tool now? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        print_info "Starting .agents..."
        poetry run python -m src.main
    fi
}

# Run main installation
main
