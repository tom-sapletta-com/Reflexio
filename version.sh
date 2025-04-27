#!/bin/bash
./flatedit
cp README.md Reflexio.md
# Usuń 3 pierwsze linijki i zapisz do pliku tymczasowego
# Utwórz tymczasowy plik
temp_file=$(mktemp)
# Usuń 3 pierwsze linijki i zapisz do pliku tymczasowego
tail -n +4 "Reflexio.md" > "$temp_file"
# Zastąp oryginalny plik plikiem tymczasowym
mv "$temp_file" "Reflexio.md"
#md2pdf Reflexio.md Reflexio.pdf
source venv/bin/activate
md2pdf README.md Reflexio.pdf
# --css-file=md2pdf/style.css --mermaid-options='{"theme":"neutral","securityLevel":"loose"}'
python changelog.py
bash git.sh
