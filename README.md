# 🎨 Mobility Book Graphic Style Guide

Una libreria Python per applicare lo stile grafico Mobility Book a visualizzazioni **Matplotlib** e **Altair**.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📦 Installazione

### Da Sviluppatore (Modalità Editable)

```bash
git clone https://github.com/danielefadda/mobility-book-graphic-style-guide.git
cd mobility-book-graphic-style-guide
pip install -e .
```

### Con Dipendenze Complete

```bash
pip install -e ".[all]"
```

---

## 🚀 Uso Rapido

### Matplotlib

```python
import mobility_book_style as mbs
import matplotlib.pyplot as plt

# Applica il tema
mbs.apply_matplotlib_theme()

# Crea il tuo grafico
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [3, 5, 2, 6], label='Serie A')
ax.set_title('Grafico Mobility Book')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.legend()
plt.show()
```

### Altair

```python
import mobility_book_style as mbs
import altair as alt
import pandas as pd

# Abilita il tema
mbs.enable_altair_theme()

# Crea il tuo grafico
data = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D'],
    'y': [5, 3, 6, 7]
})

chart = alt.Chart(data).mark_bar().encode(
    x='x:N',
    y='y:Q'
).properties(
    title='Grafico Mobility Book',
    width=600,
    height=400
)

chart.save('chart.html')  # il tema incorpora già Inter 18pt via @font-face
```

### Tabelle Matplotlib

```python
import mobility_book_style as mbs
import matplotlib.pyplot as plt

mbs.apply_matplotlib_theme()

fig, ax = plt.subplots(figsize=(8, 3))
ax.axis('off')

data = [
    ['Città', 'Popolazione', 'Area (km²)'],
    ['Milano', '1,396,059', '181.8'],
    ['Roma', '2,860,009', '1,287.4'],
]

table = ax.table(cellText=data, loc='center', cellLoc='left')
mbs.style_table(table)

plt.savefig('table.png', dpi=144, bbox_inches='tight')
```

### Esportare Colori per Adobe

```python
import mobility_book_style as mbs

# Esporta palette come Adobe Swatch Exchange (.ase)
mbs.export_ase('mobility_colors.ase', include_base=True)

# Ottieni dizionario colori risolto
colors = mbs.export_colors_dict()
print(f"Colori (flat): {len(colors['color_flat'])}")
print(f"Palette categoriale: {len(colors['categorical_palette'])}")
print(f"Palette divergente: {len(colors['divergent_palette'])}")

# Accesso dot-notation ai token
brand_primary = mbs.token.color.brand.primary
table_title_size = mbs.token.component.table.typography.title.fontSize
print(brand_primary, table_title_size)
```

---

## 📚 Documentazione

- **[UPDATING.md](UPDATING.md)** - Come modificare i design token
- **[examples/demo_new_api.ipynb](examples/demo_new_api.ipynb)** - Notebook completo con esempi

---

## 🏗️ Architettura

```
mobility_book_style/
├── data/
│   └── design_tokens.json      # Design token (unica source of truth)
├── _tokens.py                  # Loader + dot-notation token
├── matplotlib.py               # Tema Matplotlib basato sui token
├── altair.py                   # Tema Altair basato sui token
├── export.py                   # Export ASE e dizionari
└── fonts/                      # Font Inter (TTF)
```

### Principio Fondamentale

**design_tokens.json è la sola source of truth.** I moduli Python leggono quel file e lo espongono come oggetto `mbs.token` navigabile via dot-notation.

---

## 🎨 Design Tokens

### Token (design_tokens.json)

```json
{
  "color": {
    "brand": {
      "primary": { "value": "{color.base.teal.500}" }
    },
    "text": {
      "primary": { "value": "{color.base.neutral.black}" },
      "secondary": { "value": "{color.base.slate.600}" }
    },
    "chart": {
      "categorical": {
        "1": { "value": "{color.base.teal.500}" },
        "2": { "value": "{color.base.burgundy.500}" }
      }
    }
  }
}
```

I riferimenti come `{color.base.teal.500}` vengono risolti automaticamente all'import.

---

## 🔧 Modifica dei Token

Vedi **[UPDATING.md](UPDATING.md)** per una guida completa.

### Quick Start

1. Modifica `mobility_book_style/data/design_tokens.json`
2. Valida il JSON: `python -m json.tool mobility_book_style/data/design_tokens.json > /dev/null`
3. Riavvia il kernel Python (o riesegui lo script)
4. I nuovi valori vengono caricati automaticamente ✅

---

## 🧪 Test

```bash
# Esegui tutti i test
pytest tests/ -v

# Test con coverage
pytest tests/ --cov=mobility_book_style --cov-report=html
```

Tutti i test devono passare prima del commit.

---

## 📊 Esempi

Esplora i notebook in `examples/`:

- **check_env.py** - Script di verifica ambiente
- **check_env.ipynb** - Notebook di verifica
- **demo_new_api.ipynb** - Demo completa con tutti i casi d'uso

---

## 🛠️ Struttura dei File

```
.
├── README.md                   # Questo file
├── UPDATING.md                 # Guida per aggiornare i token
├── LICENSE                     # Licenza MIT
├── pyproject.toml              # Configurazione pacchetto
├── requirements.txt            # Dipendenze
│
├── mobility_book_style/        # Libreria principale
│   ├── __init__.py
│   ├── _tokens.py
│   ├── matplotlib.py
│   ├── altair.py
│   ├── export.py
│   ├── data/
│   │   └── design_tokens.json
│   └── fonts/
│       └── Inter-*.ttf
│
├── examples/                   # Esempi e demo
│   ├── check_env.py
│   ├── check_env.ipynb
│   └── demo_new_api.ipynb
│
├── tests/                      # Test suite
│   ├── test_tokens.py
│   ├── test_matplotlib.py
│   ├── test_altair.py
│   ├── test_export.py
│   └── test_fonts.py
│
└── [deprecated folders]        # Cartelle con suffisso __D
```

---

## 🎯 Funzionalità

### ✅ Implementato

- ✅ Design token system (JSON based)
- ✅ Design token system (JSON unico)
- ✅ Token semantici (brand, text, background, chart, component, etc.)
- ✅ Builder Matplotlib (grafici, tabelle)
- ✅ Builder Altair (grafici interattivi)
- ✅ Font Inter (auto-registrato)
- ✅ Export Adobe Swatch Exchange (.ase)
- ✅ Export dizionario colori
- ✅ Test suite completa (27 test)
- ✅ Documentazione e esempi

### ⚠️ Da Implementare

- ⚠️ LaTeX builder (file .sty personalizzato)
- ⚠️ CSS builder
- ⚠️ Pubblicazione su PyPI

---

## 🤝 Contribuire

1. Fai fork del repository
2. Crea un branch per la tua feature: `git checkout -b feature/nome-feature`
3. Modifica i file necessari
4. Esegui i test: `pytest tests/`
5. Commit: `git commit -am 'Add new feature'`
6. Push: `git push origin feature/nome-feature`
7. Apri una Pull Request

---

## 📝 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.

---

## 👤 Autori

**Daniele Fadda [github.com/danielefadda](https://www.github.com/danielefadda)**

- Repository: [mobility-book-graphic-style-guide](https://github.com/danielefadda/mobility-book-graphic-style-guide)

---

## 📧 Contatti

Per domande o supporto, apri un issue su GitHub.

---

**Made with ❤️ for data visualization**
