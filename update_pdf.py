import os
import re
import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus.flowables import Flowable


class HorizontalLine(Flowable):
    """Custom horizontal line flowable"""

    def __init__(self, width=6 * inch, thickness=0.5):
        Flowable.__init__(self)
        self.width = width
        self.thickness = thickness

    def draw(self):
        """Draw the line"""
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)


def md_to_pdf(md_file, pdf_file):
    # Setup Polish fonts
    def setup_polish_fonts():
        try:
            dejavu_sans = '/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf'
            dejavu_sans_bold = '/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf'

            pdfmetrics.registerFont(TTFont('DejaVuSans', dejavu_sans))
            pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', dejavu_sans_bold))

            pdfmetrics.registerFontFamily('DejaVuSans',
                                          normal='DejaVuSans',
                                          bold='DejaVuSans-Bold',
                                          italic='DejaVuSans',
                                          boldItalic='DejaVuSans-Bold'
                                          )
        except Exception as e:
            print(f"Font registration error: {e}")
            raise

    # Setup fonts
    setup_polish_fonts()

    # Read Markdown with proper encoding
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Advanced Markdown conversion
    md_extensions = ['extra']
    html = markdown.markdown(md_content, extensions=md_extensions)

    # Create PDF
    doc = SimpleDocTemplate(pdf_file, pagesize=letter,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)

    # Prepare styles
    styles = getSampleStyleSheet()

    # Custom styles
    styles['Normal'].fontName = 'DejaVuSans'
    styles['Heading1'].fontName = 'DejaVuSans-Bold'
    styles['Heading2'].fontName = 'DejaVuSans-Bold'

    # Custom italic style
    italic_style = ParagraphStyle(
        'ItalicText',
        parent=styles['Normal'],
        fontName='DejaVuSans',
        italic=True,
        alignment=TA_LEFT
    )

    # Centered style for subtitle
    centered_style = ParagraphStyle(
        'LeftText',
        parent=styles['Normal'],
        alignment=TA_LEFT
    )

    # Prepare story
    story = []

    # Custom parsing of HTML
    import re
    from xml.sax.saxutils import unescape

    # Remove HTML tags and unescape entities
    def clean_text(html_text):
        # Remove HTML tags
        clean = re.sub('<.*?>', '', html_text)
        # Unescape HTML entities
        clean = unescape(clean)
        return clean.strip()

    # Parsing logic
    current_section = []

    # Parse HTML to create PDF elements
    for line in html.split('\n'):
        if line.startswith('<h1>') or line.startswith('<h2>'):
            # If we have a previous section, add it to the story
            if current_section:
                story.extend(current_section)
                current_section = []
                story.append(PageBreak())

            # Header 1 or 2
            header_text = clean_text(line)
            if line.startswith('<h1>'):
                current_section.append(Paragraph(header_text, styles['Heading1']))
            else:
                current_section.append(Paragraph(header_text, styles['Heading2']))
            current_section.append(Spacer(1, 12))

        elif line.startswith('<p>'):
            current_paragraph_text = clean_text(line)

            # Check for special formatting
            if current_paragraph_text.startswith('*') and current_paragraph_text.endswith('*'):
                # Italic text
                text = current_paragraph_text.strip('*')
                current_section.append(Paragraph(text, italic_style))
            elif current_paragraph_text:
                # Normal paragraph
                current_section.append(Paragraph(current_paragraph_text, centered_style))

            current_section.append(Spacer(1, 6))

        elif re.match(r'^<hr\s*/>$', line.strip()):
            # Horizontal line
            current_section.append(HorizontalLine())
            current_section.append(Spacer(1, 6))

    # Add the last section
    if current_section:
        story.extend(current_section)

    # Build PDF
    doc.build(story)


# Run the conversion
if __name__ == '__main__':
    md_to_pdf('README.md', 'Reflexio.pdf')
    print("PDF conversion completed successfully!")