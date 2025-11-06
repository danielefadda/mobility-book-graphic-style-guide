# Mobility Book Style Guide 📊

Una libreria Python per applicare lo stile grafico standardizzato di **Mobility Book** alle visualizzazioni Matplotlib e Altair.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Caratteristiche

- **Stile immutabile**: Design tokens centralizzati e non modificabili per garantire coerenza visiva
- **Font Inter**: Tipografia professionale con fallback automatici
- **Palette colori ottimizzata**: Colori accessibili e distinguibili
- **Facile da usare**: 2-3 funzioni per applicare lo stile completo
- **Dipendenze opzionali**: Installa solo ciò di cui hai bisogno (Matplotlib, Altair o entrambi)

## 📦 Installazione

### Solo Matplotlib (dipendenza minima)

```bash
pip install mobility-book-style
```

### Con supporto Altair

```bash
pip install mobility-book-style[altair]
```

### Installazione completa (include dataset di esempio)

```bash
pip install mobility-book-style[all]
```

### Installazione per sviluppo

```bash
git clone https://github.com/danielefadda/mobility-book-graphic-style-guide.git
cd mobility-book-graphic-style-guide
pip install -e ".[dev]"
```

## 🚀 Uso Rapido

### Matplotlib

```python
import mobility_book_style as mbs
import matplotlib.pyplot as plt

# Applica il tema (una volta per sessione)
mbs.apply_matplotlib_theme()

# Crea i tuoi grafici normalmente
plt.figure(figsize=(10, 6))
plt.plot([1, 2, 3, 4], [3, 5, 2, 6], label='Serie A')
plt.title('Grafico con stile Mobility Book')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()
```

#### Stilizzare tabelle Matplotlib

```python
import matplotlib.pyplot as plt
import mobility_book_style as mbs

mbs.apply_matplotlib_theme()

fig, ax = plt.subplots(figsize=(8, 4))
ax.axis('off')

data = [
    ['Nome', 'Valore', 'Categoria'],
    ['Item A', '100', 'Tipo 1'],
    ['Item B', '200', 'Tipo 2'],
    ['Item C', '150', 'Tipo 1'],
]

table = ax.table(cellText=data, loc='center', cellLoc='left')
mbs.style_table(table)

plt.tight_layout()
plt.show()
```

### Altair

```python
import mobility_book_style as mbs
import altair as alt
import pandas as pd

# Abilita il tema (una volta per sessione)
mbs.enable_altair_theme()

# Crea i tuoi grafici normalmente
data = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D', 'E'],
    'y': [10, 20, 15, 25, 18]
})

chart = alt.Chart(data).mark_bar().encode(
    x='x:N',
    y='y:Q',
    color=alt.Color('x:N', legend=None)
).properties(
    title='Grafico Altair con stile Mobility Book',
    width=600,
    height=400
)

# Visualizza inline (Jupyter) o salva
chart.save('output.html')
chart.save('output.png')  # Richiede vl-convert-python
```

Per disabilitare il tema Altair:

```python
mbs.disable_altair_theme()
```

## 📚 Documentazione API

### `apply_matplotlib_theme()`

Applica il tema Matplotlib di Mobility Book. Configura globalmente i parametri `rcParams`.

**Effetti:**
- Font: Inter (con fallback)
- Colori: palette category10 personalizzata
- Griglie e assi stilizzati
- Rimozione bordi superiore/destro

### `style_table(table, *, body_face=None, header_face=None)`

Stilizza tabelle Matplotlib create con `plt.table()` o `ax.table()`.

**Parametri:**
- `table`: Oggetto Table da stilizzare
- `body_face`: Colore sfondo celle corpo (default: bianco)
- `header_face`: Colore sfondo celle header (default: grigio chiaro)

### `enable_altair_theme()`

Abilita il tema Altair di Mobility Book. Il tema rimane attivo per tutta la sessione.

**Nota:** Richiede Altair installato (`pip install mobility-book-style[altair]`)

### `disable_altair_theme()`

Ripristina il tema Altair di default.

## 🎨 Design System

Il design system si basa su tre livelli:

1. **Palette primitiva** (`_colors.py`): Colori grezzi senza semantica
2. **Design tokens** (`_tokens.py`): Valori semantici derivati dalla palette
3. **Temi** (`matplotlib.py`, `altair.py`): Applicazione dei tokens alle librerie

### Colori principali

- **Text**: `#000000` (nero)
- **Background**: `#FFFFFF` (bianco)
- **Accent**: `#1696D2` (blu Urban Institute)
- **Grid**: `#D2D2D2` (grigio chiaro)

### Font stack

```
Inter, IBM Plex Sans, DejaVu Sans, Arial, sans-serif
```

### Palette categoriale (10 colori)

Utilizzata per grafici multi-serie, ottimizzata per distinguibilità e accessibilità.

## 🧪 Testing

Esegui i test con pytest:

```bash
# Installa dipendenze di sviluppo
pip install -e ".[dev]"

# Esegui tutti i test
pytest

# Con coverage
pytest --cov=mobility_book_style --cov-report=html

# Solo test Matplotlib
pytest tests/test_matplotlib.py

# Solo test Altair (se installato)
pytest tests/test_altair.py
```

## 📂 Struttura del Progetto

```
mobility-book-graphic-style-guide/
├── mobility_book_style/        # Pacchetto principale
│   ├── __init__.py            # API pubblica
│   ├── matplotlib.py          # Tema Matplotlib
│   ├── altair.py              # Tema Altair
│   ├── _colors.py             # Palette primitiva (privato)
│   └── _tokens.py             # Design tokens (privato)
├── tests/                     # Test suite
│   ├── test_matplotlib.py
│   ├── test_altair.py
│   └── test_tokens.py
├── examples/                  # Esempi e demo
│   └── check_env.ipynb
├── docs/                      # Documentazione statica
├── pyproject.toml            # Configurazione pacchetto
├── LICENSE                   # Licenza MIT
└── README.md                 # Questo file
```

## 🔒 Nota sull'Immutabilità

**Lo stile definito in questa libreria NON è modificabile dall'utente.**

I design tokens e i colori sono intenzionalmente privati (prefisso `_`) per garantire coerenza visiva in tutte le pubblicazioni Mobility Book. Gli utenti possono solo:

- ✅ Applicare il tema completo
- ✅ Disabilitare il tema (tornare al default)
- ❌ Modificare colori, font o altri parametri

## 🤝 Contribuire

Contributi sono benvenuti! Per modifiche ai design tokens o alla palette:

1. Fork del repository
2. Crea un branch feature (`git checkout -b feature/nuova-funzionalita`)
3. Commit delle modifiche (`git commit -am 'Aggiunge nuova funzionalità'`)
4. Push al branch (`git push origin feature/nuova-funzionalita`)
5. Apri una Pull Request

**Nota:** Le modifiche ai design tokens devono essere discusse e approvate per mantenere coerenza.

## 📝 Esempi Completi

Vedi la cartella [`examples/`](examples/) per notebook Jupyter con esempi dettagliati:

- `check_env.ipynb`: Verifica ambiente e test completo di entrambi i temi
- Output salvati in `examples/outputs/`

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per dettagli.

## 🔗 Link Utili

- **Repository**: [github.com/danielefadda/mobility-book-graphic-style-guide](https://github.com/danielefadda/mobility-book-graphic-style-guide)
- **Issues**: [github.com/danielefadda/mobility-book-graphic-style-guide/issues](https://github.com/danielefadda/mobility-book-graphic-style-guide/issues)
- **PyPI**: _(da pubblicare)_

## 👥 Autori

- **Daniele Fadda** - Sviluppo iniziale

## 🙏 Ringraziamenti

Design system ispirato allo stile dell'[Urban Institute](https://www.urban.org/).

---

**Made with ❤️ for Mobility Book**
