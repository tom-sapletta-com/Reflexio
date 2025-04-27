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
    # List of possible font paths
    font_paths = [
        f'/usr/share/fonts/truetype/dejavu/{font_name}.ttf',  # Linux standard
        f'/usr/local/share/fonts/{font_name}.ttf',
        f'/Library/Fonts/{font_name}.ttf',  # macOS
        os.path.expanduser(f'~/.local/share/fonts/{font_name}.ttf'),
        os.path.expanduser(f'~/Library/Fonts/{font_name}.ttf')
    ]

    for path in font_paths:
        if os.path.exists(path):
            return path

    raise FileNotFoundError(f"Could not find font {font_name}")


def setup_polish_fonts():
    # Find and register Polish-friendly fonts
    try:
        dejavu_sans = find_font('DejaVuSans')
        dejavu_sans_bold = find_font('DejaVuSans-Bold')

        pdfmetrics.registerFont(TTFont('DejaVuSans', dejavu_sans))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', dejavu_sans_bold))
    except FileNotFoundError:
        # Fallback to a default font if DejaVu is not found
        print("Warning: DejaVu fonts not found. Using default fonts.")


def md_to_pdf(md_file, pdf_file):
    # Setup Polish fonts
    setup_polish_fonts()

    # Read Markdown with proper encoding
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert Markdown to HTML
    html = markdown.markdown(md_content)

    # Convert HTML to plain text
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.body_width = 0  # Disable line wrapping
    plain_text = h.handle(html)

    # Create PDF
    doc = SimpleDocTemplate(pdf_file, pagesize=letter,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)

    # Prepare styles
    styles = getSampleStyleSheet()

    # Custom style for better Markdown rendering with Polish characters
    custom_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName='DejaVuSans',
        alignment=TA_LEFT,
        fontSize=11,
        leading=14,
        spaceAfter=6
    )

    # Modify heading styles to use DejaVuSans
    try:
        styles['Heading1'].fontName = 'DejaVuSans-Bold'
        styles['Heading2'].fontName = 'DejaVuSans-Bold'
        styles['Heading3'].fontName = 'DejaVuSans-Bold'
        styles['Heading4'].fontName = 'DejaVuSans-Bold'
    except Exception:
        print("Warning: Could not set bold font for headings")

    # Prepare story
    story = []

    # Split text into lines and create paragraphs
    for line in plain_text.split('\n'):
        # Skip empty lines
        if line.strip():
            # Handle headers
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
                # Regular paragraph
                story.append(Paragraph(line, custom_style))

            # Add some space between paragraphs
            story.append(Spacer(1, 6))

    # Build PDF
    doc.build(story)


# Run the conversion
if __name__ == '__main__':
    md_to_pdf('README.md', 'Reflexio.pdf')
    print("PDF conversion completed successfully!")