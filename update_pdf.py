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
from reportlab.lib.fonts import ps2tt, addMapping


def find_font(font_name):
    # List of possible font paths for Fedora and other systems
    font_paths = [
        f'/usr/share/fonts/dejavu-sans-fonts/{font_name}.ttf',
        f'/usr/share/fonts/dejavu-sans-fonts/{font_name}*.ttf',
        f'/usr/share/fonts/truetype/dejavu/{font_name}.ttf',
        f'/usr/share/fonts/{font_name}.ttf',
        os.path.expanduser(f'~/.local/share/fonts/{font_name}.ttf'),
    ]

    for path_pattern in font_paths:
        matching_fonts = [f for f in glob.glob(path_pattern) if os.path.exists(f)]
        if matching_fonts:
            return matching_fonts[0]

    raise FileNotFoundError(f"Could not find font {font_name}")


def setup_polish_fonts():
    import glob

    try:
        # Explicitly use the full paths we found earlier
        dejavu_sans = '/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf'
        dejavu_sans_bold = '/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf'

        # Register fonts with ReportLab
        pdfmetrics.registerFont(TTFont('DejaVuSans', dejavu_sans))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', dejavu_sans_bold))

        # Explicit font mappings
        pdfmetrics.registerFontFamily('DejaVuSans',
                                      normal='DejaVuSans',
                                      bold='DejaVuSans-Bold',
                                      italic='DejaVuSans',
                                      boldItalic='DejaVuSans-Bold'
                                      )
    except Exception as e:
        print(f"Font registration error: {e}")
        raise


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

    # Custom font settings for styles
    styles['Normal'].fontName = 'DejaVuSans'
    styles['Heading1'].fontName = 'DejaVuSans-Bold'
    styles['Heading2'].fontName = 'DejaVuSans-Bold'
    styles['Heading3'].fontName = 'DejaVuSans-Bold'
    styles['Heading4'].fontName = 'DejaVuSans-Bold'

    # Custom style for body text
    custom_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName='DejaVuSans',
        alignment=TA_LEFT,
        fontSize=11,
        leading=14,
        spaceAfter=6
    )

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