<style>
/* CSS do umieszczenia na początku pliku Markdown */

img {
  max-width: 100%; /* Upewnia się, że obrazy nigdy nie przekroczą szerokości kontenera */
  height: auto;    /* Zachowuje proporcje obrazu */
  display: block;  /* Sprawia, że obraz jest elementem blokowym */
  margin: 20px auto; /* Centruje obraz z marginesem na górze i dole */
  page-break-inside: avoid; /* Zapobiega łamaniu obrazu między stronami */
}

/* Style dla diagramów Mermaid */
.mermaid {
  max-width: 100%;
  overflow-x: hidden; /* Zapobiega poziomemu przewijaniu */
  svg {
    max-width: 100%;
    height: auto !important; /* Nadpisuje wysokość ustawioną przez Mermaid */
  }
}

/* Style dla tabeli */
table {
  width: 100%;
  max-width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  page-break-inside: avoid; /* Zapobiega łamaniu tabeli między stronami */
}

th, td {
  padding: 8px;
  border: 1px solid #ddd;
  word-wrap: break-word; /* Zawijanie długich tekstów */
}

/* Style dla bloków kodu */
pre {
  white-space: pre-wrap; /* Zawijanie długich linii kodu */
  max-width: 100%;
  overflow-x: hidden;
  padding: 10px;
  background-color: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 4px;
  page-break-inside: avoid;
}

/* Zapewnienie prawidłowych podziałów stron */
h1, h2, h3 {
  page-break-after: avoid; /* Nagłówki nie powinny być ostatnim elementem na stronie */
}

p {
  page-break-inside: avoid; /* Jeśli to możliwe, nie dziel akapitów między stronami */
}
h1 {
  page-break-before: always;
}

h2 {
  page-break-before: always;
}

/* Nagłówek na pierwszej stronie nie powinien wymuszać podziału strony */
body > h1:first-of-type,
body > h2:first-of-type {
  page-break-before: avoid;
}
</style>