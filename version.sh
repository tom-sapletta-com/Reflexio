#!/bin/bash
./flatedit
cp README.md Reflexio.md
# Usuń 3 pierwsze linijki i zapisz do pliku tymczasowego

#python -m venv venv
source venv/bin/activate
#md2pdf README.md Reflexio.pdf
#pandoc README.md -o Reflexio.pdf
python update_pdf.py
# --css-file=md2pdf/style.css --mermaid-options='{"theme":"neutral","securityLevel":"loose"}'
python changelog.py
bash git.sh
