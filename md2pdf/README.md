### Metoda 1: Osadzanie CSS bezpośrednio w pliku Markdown

1. Na początku pliku Markdown umieść blok CSS wewnątrz znaczników `<style>`:

```markdown
<style>
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 20px auto;
  page-break-inside: avoid;
}

.mermaid {
  max-width: 100%;
  overflow-x: hidden;
}

/* Pozostałe style... */
</style>

# Twój tytuł
```

2. Następnie uruchom zwykłe polecenie md2pdf:

```bash
md2pdf Reflexio.md Reflexio.pdf
```

### Metoda 2: Używanie zewnętrznego pliku CSS

1. Utwórz oddzielny plik CSS (np. `custom.css`) zawierający wszystkie potrzebne style:

```css
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 20px auto;
  page-break-inside: avoid;
}

.mermaid {
  max-width: 100%;
  overflow-x: hidden;
}

/* Pozostałe style... */
```

2. Uruchom md2pdf z opcją `--css-file`:

```bash
md2pdf Reflexio.md Reflexio.pdf --css-file=custom.css
```

### Dodatkowe opcje konfiguracji

Możesz również dodać więcej opcji, aby lepiej kontrolować wygląd wyjściowego PDF:

```bash
md2pdf Reflexio.md Reflexio.pdf --css-file=custom.css --highlight-style=github --pdf-options='{"format": "A4", "margin": "20mm", "printBackground": true}'
```

Gdzie:
- `--highlight-style=github` określa styl podświetlania składni kodu
- `--pdf-options` pozwala na przekazanie opcji formatowania PDF, takich jak:
  - `format`: rozmiar strony (A4, Letter itp.)
  - `margin`: marginesy strony
  - `printBackground`: drukowanie kolorów tła

### Jeśli masz problemy z renderowaniem diagramów Mermaid

Jeśli md2pdf ma problemy z właściwym renderowaniem diagramów Mermaid, możesz wypróbować alternatywne rozwiązania:

1. **Użyj narzędzia obsługującego Mermaid**:
   ```bash
   md-to-pdf Reflexio.md --stylesheet custom.css --md-file-encoding utf-8 --highlight-style github
   ```

2. **Wygeneruj statyczne obrazy diagramów**:
   - Użyj Mermaid Live Editor (https://mermaid.live/)
   - Eksportuj diagramy jako PNG lub SVG
   - Zastąp kod Mermaid w pliku Markdown odnośnikami do obrazów:
     ```markdown
     ![Poziomy rzeczywistości](./images/poziomy-rzeczywistosci.png)
     ```

3. **Modyfikuj opcje Mermaid** - jeśli Twoje narzędzie obsługuje konfigurację Mermaid:
   ```bash
   md2pdf Reflexio.md Reflexio.pdf --css-file=md2pdf/custom.css --mermaid-options='{"theme":"neutral","securityLevel":"loose"}'
   ```

Najlepszym rozwiązaniem jest zazwyczaj pierwsza metoda (osadzanie CSS w pliku Markdown), ponieważ działa z większością narzędzi do konwersji Markdown na PDF i zapewnia, że style będą zawsze dołączone do dokumentu.