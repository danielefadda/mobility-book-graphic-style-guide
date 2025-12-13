# Theme Visualization - Design Token HTML Generator

Questo sistema genera automaticamente visualizzazioni HTML interattive dei design token di Mobility Book.

## 📁 File Generati

- **`docs/theme-visualization.html`** - Visualizzazione interattiva completa con tutte le palette, colori semantici e sequenze

## 🚀 Come Usarlo

### Generare l'HTML

```bash
# Opzione 1: Script Python
python scripts/generate_theme_visualization.py

# Opzione 2: Dal notebook Python
from mobility_book_style.theme_visualizer import save_theme_html
html_path = save_theme_html()
```

### Visualizzare nel Browser

Apri il file `docs/theme-visualization.html` nel tuo browser preferito:

```bash
# macOS
open docs/theme-visualization.html

# Linux
xdg-open docs/theme-visualization.html

# Windows
start docs/theme-visualization.html
```

## 🎨 Cosa Contiene

L'HTML generato include:

1. **🎨 Palette Base** - Tutte le palette disponibili con i loro colori ordinati
2. **🎯 Colori Semantici** - Colori raggruppati per ruolo (Brand, Intent, Text, Background)
3. **📊 Sequenze Grafici** - Sequenze sequenziali e divergenti per i grafici

## ✨ Caratteristiche

- ✅ **Dinamico** - Utilizza le funzioni del modulo `theme` per ottenere i colori
- ✅ **Auto-aggiornabile** - Se cambiano i design token, basta rigenerare per vedere i cambiamenti
- ✅ **Interattivo** - Hover effects e visualizzazione dei codici hex
- ✅ **Responsive** - Funziona bene su desktop e mobile
- ✅ **Autonomo** - Nessuna dipendenza da librerie esterne

## 🔄 Flusso di Lavoro Consigliato

1. Modifica i design token in `mobility_book_style/data/design_tokens.json`
2. Esegui lo script di generazione:
   ```bash
   python scripts/generate_theme_visualization.py
   ```
3. Apri l'HTML generato nel browser per verificare le visualizzazioni

## 📝 Moduli Coinvolti

### `mobility_book_style/theme_visualizer.py`

Modulo Python che gestisce la generazione dell'HTML.

**Funzioni principali:**

- `generate_theme_html()` - Genera HTML come stringa
- `save_theme_html(output_path=None)` - Genera e salva l'HTML
- `_dict_to_js(data)` - Converte dict Python in JavaScript object

## 🛠️ Personalizzazione

Se vuoi modificare lo stile o il layout dell'HTML, modifica il template in `theme_visualizer.py`:

```python
# In theme_visualizer.py, nella funzione generate_theme_html()
html = f"""<!DOCTYPE html>
...
# Personalizza CSS e HTML qui
...
"""
```

## 📦 Automazione CI/CD

Per includere la generazione dell'HTML in una pipeline CI/CD:

```yaml
# Esempio con GitHub Actions
- name: Generate theme visualization
  run: python scripts/generate_theme_visualization.py
```

Questo assicura che l'HTML sia sempre aggiornato nei commit.
