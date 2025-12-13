# Guida alla Visualizzazione del Tema

## Panoramica

Il sistema di visualizzazione del tema genera una pagina HTML interattiva che mostra tutti i colori, i font e i dati di design del Mobility Book Design System.

## Caratteristiche

### 🎨 Palette di Colori
- Visualizzazione di tutte le palette disponibili (teal, burgundy, purple, rust, gray, orange, pink, brown, green, navy)
- Ogni colore mostra il codice hex sottostante
- **Nuovo**: Il colore principale (-500) di ogni palette è evidenziato con un bordo nero di 3px per facilitare l'identificazione

### 🎯 Colori Semantici
- Brand colors (primary, accent, secondary)
- Intent colors (info, success, warning, error)
- Text colors (primary, secondary, tertiary, disabled)
- Background colors (light, medium, dark)

### 📊 Sequenze per Grafici
- Sequential (monocromatiche): per visualizzare gradazioni di un singolo valore
- Divergent (divergenti): per confrontare valori positivi e negativi
- Utili per visualizzazioni di dati in Altair

### 🔤 Typography (Nuovo!)
Sezione dedicata ai font disponibili con tre sottosezioni:

1. **Families** - Famiglie di font disponibili:
   - Inter Sans
   - Inter Mono

2. **Sizes** - Dimensioni disponibili:
   - xs, s, m, l, xl, xxl (e altre secondo necessità)

3. **Weights** - Pesi dei font:
   - regular, medium, bold

## Generazione

### Opzione 1: Script CLI

```bash
python scripts/generate_theme_visualization.py
```

Output: `docs/theme-visualization.html`

### Opzione 2: Python programmatico

```python
from mobility_book_style.theme_visualizer import save_theme_html

# Genera nel percorso di default (docs/theme-visualization.html)
html_path = save_theme_html()
print(f"HTML salvato in: {html_path}")

# Genera in percorso custom
html_path = save_theme_html("/percorso/custom/theme.html")
```

### Opzione 3: Notebook Jupyter

Nel notebook `examples/helper.ipynb`, l'ultima cella genera automaticamente l'HTML:

```python
from mobility_book_style.theme_visualizer import save_theme_html
html_path = save_theme_html()
print(f"✅ HTML di tema generato: {html_path}")
```

## Architettura

### Componenti Principali

1. **mobility_book_style/theme_visualizer.py**
   - `generate_theme_html()` - Genera l'HTML completo
   - `save_theme_html(output_path)` - Salva l'HTML su disco
   - Utilizza `_dict_to_js()` per convertire i dati Python in JSON

2. **scripts/generate_theme_visualization.py**
   - CLI script per l'esecuzione facile
   - Utilizza `theme_visualizer.save_theme_html()`

3. **Funzioni del Modulo Theme Utilizzate**
   - `theme.list_palettes()` - Ottiene tutti i nomi delle palette
   - `theme.get_palette(name)` - Ottiene i colori di una palette
   - `theme.list_semantic_keys()` - Ottiene tutte le chiavi semantiche
   - `theme.get_color(role, section)` - Ottiene un colore semantico
   - `theme.list_chart_schemes()` - Ottiene tutti i tipi di sequenza
   - `theme.get_chart_sequence(name)` - Ottiene una sequenza
   - `theme.list_fonts()` - Ottiene le famiglie di font
   - `theme.list_font_sizes()` - Ottiene le dimensioni disponibili
   - `theme.list_font_weights()` - Ottiene i pesi disponibili

## HTML Generato

### Struttura della Pagina

```
┌─────────────────────────────────────┐
│  Header (Titolo + Info Generazione) │
├─────────────────────────────────────┤
│  🎨 Color Palettes                  │
│  (Grid di palettes con evidenziazione -500)
├─────────────────────────────────────┤
│  🎯 Semantic Colors                 │
│  (Grid organizzate per categoria)   │
├─────────────────────────────────────┤
│  📊 Chart Sequences                 │
│  (Bar lineari colorate)             │
├─────────────────────────────────────┤
│  🔤 Typography                      │
│  (Grid di font families/sizes/weights)
├─────────────────────────────────────┤
│  Footer                             │
└─────────────────────────────────────┘
```

### Dimensioni e Performance

- **File size**: ~20KB (non compresso)
- **Riga di codice**: 492 linee
- **Formato**: HTML singolo, autocontenuto (nessuna dipendenza esterna)
- **Compatibilità**: Tutti i browser moderni che supportano ES6

## Interattività

### Nel Browser

1. **Hover su colori**: Mostra informazioni e effetti visuali
2. **Clicca su colori**: Pronto per future funzionalità (es. copia hex)
3. **Sequenze grafiche**: Hover su segmenti per vedere il valore hex

### Evidenziazione -500

Il colore al 6° posto (indice 5, valore -500) in ogni palette è evidenziato con:
- Bordo nero di 3px
- Nome della classe CSS: `primary-500`
- Questo facilita l'identificazione del colore principale di ogni palette

## Data Binding

L'HTML è generato dinamicamente dalle funzioni del modulo `theme`:

```javascript
// Nel template HTML generato:
const palettes = {
  "teal": ["#f0f8f9", "#c4e8eb", ..., "#065c68"],
  "burgundy": [...],
  ...
}
```

I dati vengono serializzati come JSON all'interno del file HTML, quindi:
- ✅ Nessuna dipendenza di runtime
- ✅ Nessuna chiamata API o server
- ✅ Perfetto per documentazione statica
- ✅ Facilmente versionabile in git

## Manutenzione

### Quando Rigenerare

Rigenerare l'HTML quando:
- Vengono modificati i token nel file `design_tokens.json`
- Vengono aggiunte nuove palette
- Vengono modificati i colori semantici
- Vengono aggiunti/modificati i font

### Comando di Rigenerazione

```bash
# Dalla radice del progetto
python scripts/generate_theme_visualization.py
```

### Workflow di Sviluppo

```bash
# Modifica i token
nano mobility_book_style/data/design_tokens.json

# Rigenerare la visualizzazione
python scripts/generate_theme_visualization.py

# Visualizza nel browser
open docs/theme-visualization.html

# Commit dei cambiamenti
git add docs/theme-visualization.html
git commit -m "Aggiorna tema visualizzazione con nuovi token"
```

## Troubleshooting

### L'HTML non mostra i dati

1. Verifica che `theme.py` sia caricato correttamente
2. Esegui: `python scripts/generate_theme_visualization.py`
3. Verifica che il file `docs/theme-visualization.html` esista

### I font non compaiono

Verificare che le funzioni `theme.list_fonts()`, `theme.list_font_sizes()`, e `theme.list_font_weights()` ritornino dati:

```python
from mobility_book_style import theme
print(theme.list_fonts())
print(theme.list_font_sizes())
print(theme.list_font_weights())
```

### Performance

Se il file HTML è troppo grande, è possibile:
1. Minificare il CSS
2. Comprimere il JSON
3. Dividere in file separati per palette

## Estensioni Future

Potenziali miglioramenti:

- [ ] Esportare palette in formato ASE/ACO per Adobe
- [ ] Generare palette per altri strumenti (Figma, Sketch)
- [ ] Aggiungere contrastimetro WCAG
- [ ] Generare CSS custom properties
- [ ] Generare Tailwind config
- [ ] Sincronizzare con CDN per distribuzione
