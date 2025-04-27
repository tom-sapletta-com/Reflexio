#!/bin/bash

# Exit on any error
set -e

# Function to print colored output
print_step() {
    echo -e "\033[1;34m[STEP]\033[0m $1"
}

# Function to print success message
print_success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

# Function to print error message
print_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

# Check if script is run with sudo or as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run this script with sudo or as root"
    exit 1
fi

# Update system packages
print_step "Updating system packages..."
dnf update -y

# Install Python and virtual environment tools
print_step "Installing Python and virtual environment tools..."
dnf install -y python3 python3-pip python3-virtualenv python3-devel

# Install system dependencies for PDF and font rendering
print_step "Installing system dependencies..."
dnf install -y \
    python3-devel \
    redhat-rpm-config \
    gcc \
    libffi-devel \
    openssl-devel \
    dejavu-sans-fonts \
    dejavu-sans-mono-fonts \
    dejavu-serif-fonts

# Create project directory if it doesn't exist
PROJECT_DIR="$HOME/Reflexio"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Create Python virtual environment
print_step "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
print_step "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies for PDF conversion
print_step "Installing Python dependencies..."
pip install \
    markdown \
    html2text \
    reportlab \
    Pillow

# sudo dnf install dejavu-sans-fonts dejavu-sans-mono-fonts dejavu-serif-fonts

# Make the script executable
chmod +x update_pdf.py

print_success "Setup complete! To convert PDF:"
echo "1. Activate virtual environment: source $PROJECT_DIR/venv/bin/activate"
echo "2. Run script: python update_pdf.py"