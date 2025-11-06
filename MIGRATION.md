# Guida alla Migrazione 🔄

Questa guida spiega come migrare dal vecchio sistema di import alla nuova struttura a libreria.

## 📊 Confronto API

### Prima (vecchio sistema)

```python
# Setup manuale del PYTHONPATH
from pathlib import Path
import sys
ROOT = Path.cwd().parent  # o navigazione manuale
sys.path.insert(0, str(ROOT))

# Import da moduli interni
from builders.matplotlib_builder import apply_mpl_theme
from themes.altair_mobility_theme import mobility_theme  # noqa: F401
from design_tokens.design_tokens import TOKENS

# Uso
apply_mpl_theme()
# Altair si auto-registrava all'import
```

### Dopo (nuova libreria)

```python
# Nessun setup del path necessario!
import mobility_book_style as mbs

# Matplotlib
mbs.apply_matplotlib_theme()

# Altair
mbs.enable_altair_theme()
```

## 🔄 Mappatura Funzioni

| Vecchio | Nuovo | Note |
|---------|-------|------|
| `from builders.matplotlib_builder import apply_mpl_theme` | `import mobility_book_style as mbs`<br>`mbs.apply_matplotlib_theme()` | Nome più esplicito |
| `from themes.altair_mobility_theme import mobility_theme` | `mbs.enable_altair_theme()` | Registrazione esplicita |
| `from builders.matplotlib_builder import style_table` | `mbs.style_table(table)` | Uguale, ma import diverso |
| `from design_tokens.design_tokens import TOKENS` | **NON DISPONIBILE** | Tokens ora privati (_tokens.py) |

## ⚠️ Breaking Changes

1. **Design tokens non accessibili direttamente**
   - **Prima**: `from design_tokens.design_tokens import TOKENS`
   - **Dopo**: Non esposti pubblicamente (sono privati)
   - **Motivo**: Garantire immutabilità dello stile

2. **Altair richiede chiamata esplicita**
   - **Prima**: Auto-registrazione all'import
   - **Dopo**: `mbs.enable_altair_theme()` esplicito
   - **Motivo**: Più controllo, possibilità di disable

3. **Nome pacchetto diverso**
   - **Prima**: Import relativi da cartelle
   - **Dopo**: `import mobility_book_style`
   - **Motivo**: Pacchetto Python standard

## 📝 Esempi di Migrazione

### Esempio 1: Script Matplotlib Semplice

**Prima:**
```python
from pathlib import Path
import sys
cwd = Path.cwd()
ROOT = next((p for p in [cwd] + list(cwd.parents) if (p / "requirements.txt").exists()), cwd)
sys.path.insert(0, str(ROOT))

from builders.matplotlib_builder import apply_mpl_theme
import matplotlib.pyplot as plt

apply_mpl_theme()
plt.plot([1, 2, 3], [4, 5, 6])
plt.show()
```

**Dopo:**
```python
import mobility_book_style as mbs
import matplotlib.pyplot as plt

mbs.apply_matplotlib_theme()
plt.plot([1, 2, 3], [4, 5, 6])
plt.show()
```

### Esempio 2: Script Altair

**Prima:**
```python
from pathlib import Path
import sys
ROOT = Path.cwd().parent
sys.path.insert(0, str(ROOT))

import altair as alt
from themes.altair_mobility_theme import mobility_theme  # noqa: F401

chart = alt.Chart(data).mark_bar()...
```

**Dopo:**
```python
import mobility_book_style as mbs
import altair as alt

mbs.enable_altair_theme()

chart = alt.Chart(data).mark_bar()...
```

### Esempio 3: Accesso ai Tokens (non più supportato)

**Prima:**
```python
from design_tokens.design_tokens import TOKENS
print(TOKENS['color']['text'])
```

**Dopo:**
```python
# Non più possibile direttamente
# Se necessario per debug, puoi fare:
from mobility_book_style._tokens import TOKENS  # sconsigliato!
print(TOKENS['color']['text'])

# Ma è meglio non dipendere da valori interni
```

## 🚀 Processo di Migrazione

### 1. Installa la nuova libreria

```bash
# Modalità sviluppo (nel repository)
cd /path/to/mobility-book-graphic-style-guide
pip install -e ".[all]"
```

### 2. Aggiorna i tuoi script/notebook

- Rimuovi codice di setup del PYTHONPATH
- Sostituisci `from builders...` con `import mobility_book_style as mbs`
- Sostituisci `apply_mpl_theme()` con `mbs.apply_matplotlib_theme()`
- Sostituisci import Altair con `mbs.enable_altair_theme()`

### 3. Testa

```bash
# Esegui i tuoi script
python your_script.py

# Oppure apri i notebook
jupyter notebook
```

### 4. Rimuovi dipendenze dal vecchio sistema

Una volta migrato tutto, puoi rimuovere:
- Codice di navigazione path in ogni script
- Import da `builders/`, `themes/`, `design_tokens/`

## 📦 Installazione in Progetti Esterni

Se usi questa libreria in altri progetti (fuori dal repository):

```bash
# Opzione 1: Da repository locale
pip install /path/to/mobility-book-graphic-style-guide

# Opzione 2: Da GitHub (una volta pushato)
pip install git+https://github.com/danielefadda/mobility-book-graphic-style-guide.git

# Opzione 3: Da PyPI (dopo pubblicazione)
pip install mobility-book-style[all]
```

Poi nel progetto:

```python
import mobility_book_style as mbs
mbs.apply_matplotlib_theme()
```

## ✅ Checklist Migrazione

- [ ] Libreria installata (`pip install -e ".[all]"`)
- [ ] Rimosso setup PYTHONPATH da script/notebook
- [ ] Aggiornati import da vecchia struttura a `mobility_book_style`
- [ ] Sostituito `apply_mpl_theme()` con `mbs.apply_matplotlib_theme()`
- [ ] Sostituito import Altair con `mbs.enable_altair_theme()`
- [ ] Rimossi accessi diretti a TOKENS (se presenti)
- [ ] Testati tutti gli script/notebook
- [ ] Verificato che output siano identici

## 🆘 Risoluzione Problemi

### Import Error: "No module named 'mobility_book_style'"

**Soluzione**: Installa la libreria
```bash
pip install -e .
```

### Import Error: "Altair non è installato"

**Soluzione**: Installa con supporto Altair
```bash
pip install -e ".[altair]"
# oppure
pip install altair
```

### I font non vengono applicati

**Verifica**:
```python
import matplotlib as mpl
print(mpl.rcParams['font.sans-serif'])
# Dovrebbe contenere 'Inter'
```

Se Inter non è disponibile sul sistema, Matplotlib userà i fallback (DejaVu Sans, Arial).

## 📚 Risorse

- **README**: Documentazione completa della nuova API
- **Esempi**: `examples/demo_new_api.ipynb`
- **Test**: `tests/` per vedere come vengono testati i moduli

---

**Nota**: La vecchia struttura (`builders/`, `themes/`, `design_tokens/`) rimane nel repository per compatibilità temporanea, ma sarà deprecata nelle prossime versioni.
