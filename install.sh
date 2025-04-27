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

# Create PDF conversion script
print_step "Creating PDF conversion script..."
cat > update_pdf.py << EOL
import os
import markdown
import html2text
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT

def find_font(font_name):
    # List of possible font paths for Fedora
    font_paths = [
        f'/usr/share/fonts/dejavu/{font_name}.ttf',
        f'/usr/share/fonts/truetype/dejavu/{font_name}.ttf',
        os.path.expanduser(f'~/.local/share/fonts/{font_name}.ttf'),
    ]

    for path in font_paths:
        if os.path.exists(path):
            return path

    raise FileNotFoundError(f"Could not find font {font_name}")

def setup_polish_fonts():
    try:
        dejavu_sans = find_font('DejaVuSans')
        dejavu_sans_bold = find_font('DejaVuSans-Bold')

        pdfmetrics.registerFont(TTFont('DejaVuSans', dejavu_sans))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', dejavu_sans_bold))
    except FileNotFoundError:
        print("Warning: DejaVu fonts not found. Using default fonts.")

def md_to_pdf(md_file, pdf_file):
    setup_polish_fonts()

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html = markdown.markdown(md_content)

    h = html2text.HTML2Text()
    h.ignore_links = False
    h.body_width = 0
    plain_text = h.handle(html)

    doc = SimpleDocTemplate(pdf_file, pagesize=letter,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)

    styles = getSampleStyleSheet()

    custom_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName='DejaVuSans',
        alignment=TA_LEFT,
        fontSize=11,
        leading=14,
        spaceAfter=6
    )

    try:
        styles['Heading1'].fontName = 'DejaVuSans-Bold'
        styles['Heading2'].fontName = 'DejaVuSans-Bold'
        styles['Heading3'].fontName = 'DejaVuSans-Bold'
        styles['Heading4'].fontName = 'DejaVuSans-Bold'
    except Exception:
        print("Warning: Could not set bold font for headings")

    story = []

    for line in plain_text.split('\n'):
        if line.strip():
            if line.startswith('#'):
                header_level = line.count('#')
                header_text = line.lstrip('#').strip()
                if header_level == 1:
                    story.append(Paragraph(header_text, styles['Heading1']))
                elif header_level == 2:
                    story.append(Paragraph(header_text, styles['Heading2']))
                elif header_level == 3:
                    story.append(Paragraph(header_text, styles['Heading3']))
                else:
                    story.append(Paragraph(header_text, styles['Heading4']))
            else:
                story.append(Paragraph(line, custom_style))

            story.append(Spacer(1, 6))

    doc.build(story)

if __name__ == '__main__':
    md_to_pdf('README.md', 'Reflexio.pdf')
    print("PDF conversion completed successfully!")
EOL

# Make the script executable
chmod +x update_pdf.py

print_success "Setup complete! To convert PDF:"
echo "1. Activate virtual environment: source $PROJECT_DIR/venv/bin/activate"
echo "2. Run script: python update_pdf.py"