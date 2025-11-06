# Risoluzione Problemi 🔧

Guida rapida per risolvere i problemi comuni con `mobility-book-style`.

---

## ❌ ModuleNotFoundError: No module named 'mobility_book_style'

### Problema
```python
import mobility_book_style as mbs
# ModuleNotFoundError: No module named 'mobility_book_style'
```

### Causa
Il pacchetto non è installato nell'ambiente Python che stai usando, oppure Jupyter sta usando un kernel diverso.

### Soluzioni

#### ✅ Soluzione 1: Installa nel Notebook (più semplice)

Se usi Jupyter Notebook, aggiungi e esegui questa cella:

```python
import sys
import subprocess

# Installa nel kernel corrente
subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."])
```

Poi **riavvia il kernel**: `Kernel → Restart Kernel`

#### ✅ Soluzione 2: Installa da Terminale

```bash
# Vai alla directory del progetto
cd /path/to/mobility-book-graphic-style-guide

# Verifica di essere nel branch corretto
git branch  # dovrebbe mostrare * refactor/package-structure

# Installa
pip install -e .

# Verifica installazione
python -c "import mobility_book_style; print('OK')"
```

#### ✅ Soluzione 3: Verifica Environment

```bash
# Quale Python sta usando Jupyter?
jupyter --paths

# Attiva l'environment corretto (se usi conda/venv)
conda activate nome_environment  # oppure
source venv/bin/activate

# Poi installa
pip install -e .
```

#### ✅ Soluzione 4: Reinstalla Kernel Jupyter

```bash
# Installa ipykernel nell'environment
pip install ipykernel

# Registra il kernel
python -m ipykernel install --user --name=mobility_env --display-name="Python (Mobility)"

# Poi in Jupyter: Kernel → Change Kernel → Python (Mobility)
```

---

## ❌ Import Error: Altair non è installato

### Problema
```python
mbs.enable_altair_theme()
# ImportError: Altair non è installato. Installalo con: pip install mobility-book-style[altair]
```

### Causa
Altair è una dipendenza opzionale e non è installato.

### Soluzione

```bash
# Opzione 1: Solo Altair
pip install altair

# Opzione 2: Reinstalla con tutte le dipendenze
pip install -e ".[all]"
```

---

## ❌ Font Inter non applicato

### Problema
I grafici non usano il font Inter, ma un font di default.

### Causa
Il font Inter non è installato sul sistema o Matplotlib non riesce a trovarlo.

### Verifica

```python
import matplotlib as mpl
print(mpl.rcParams['font.sans-serif'])
# Dovrebbe contenere 'Inter' come primo elemento
```

### Soluzione

Il tema usa un **font stack con fallback**:
```
Inter → IBM Plex Sans → DejaVu Sans → Arial → sans-serif
```

Se Inter non è disponibile, Matplotlib userà automaticamente il primo font disponibile.

**Per installare Inter sul sistema:**

- **macOS**: [Download Inter](https://rsms.me/inter/) → Installa .ttf
- **Linux**: `sudo apt install fonts-inter` (Ubuntu/Debian)
- **Windows**: [Download Inter](https://rsms.me/inter/) → Installa .ttf

Dopo l'installazione:
```python
# Ricarica la cache dei font di Matplotlib
import matplotlib.font_manager as fm
fm._load_fontmanager(try_read_cache=False)
```

---

## ❌ Altair PNG export fallisce

### Problema
```python
chart.save("output.png")
# ValueError: Cannot save chart as PNG...
```

### Causa
Altair richiede dipendenze aggiuntive per esportare PNG.

### Soluzione

```bash
# Opzione consigliata: vl-convert
pip install vl-convert-python

# Alternativa: altair_saver
pip install altair_saver

# Poi riprova
chart.save("output.png")
```

---

## ❌ Test falliscono con pytest

### Problema
```bash
pytest
# alcuni test falliscono
```

### Soluzione

```bash
# Installa dipendenze di sviluppo
pip install -e ".[dev]"

# Verifica che matplotlib e altair siano installati
pip list | grep -E "matplotlib|altair"

# Esegui test con verbose
pytest -v

# Salta test Altair se non installato
pytest -v -k "not altair"
```

---

## ❌ Il tema non si applica / sembra ignorato

### Problema
Dopo `mbs.apply_matplotlib_theme()` i grafici hanno ancora lo stile di default.

### Causa possibili

1. **Tema applicato dopo la creazione della figura**
2. **Style context manager attivo**
3. **rcParams sovrascritti**

### Soluzione

```python
import mobility_book_style as mbs
import matplotlib.pyplot as plt

# CORRETTO: Applica PRIMA di creare figure
mbs.apply_matplotlib_theme()
plt.plot([1, 2, 3])  # ✅ Usa il tema

# SBAGLIATO: Applica DOPO
plt.plot([1, 2, 3])
mbs.apply_matplotlib_theme()  # ❌ Troppo tardi
```

**Se usi context manager**, applica dentro:
```python
with plt.style.context('default'):
    mbs.apply_matplotlib_theme()  # Applica qui
    plt.plot([1, 2, 3])
```

---

## ❌ ImportError: No module named '_colors' o '_tokens'

### Problema
```python
from mobility_book_style._tokens import TOKENS
# ImportError...
```

### Causa
Stai cercando di importare moduli privati (prefisso `_`).

### Soluzione

**Non dovresti importare direttamente i moduli privati.** Usa l'API pubblica:

```python
# ❌ SBAGLIATO (moduli privati)
from mobility_book_style._tokens import TOKENS

# ✅ CORRETTO (API pubblica)
import mobility_book_style as mbs
mbs.apply_matplotlib_theme()
mbs.enable_altair_theme()
```

Se **davvero** hai bisogno di accedere ai tokens (sconsigliato):
```python
# Per debug/ispezione SOLAMENTE
import mobility_book_style._tokens as _tokens
print(_tokens.TOKENS['color']['text'])
```

---

## ❌ Git: branch refactor/package-structure non trovato

### Problema
```bash
git checkout refactor/package-structure
# error: pathspec 'refactor/package-structure' did not match...
```

### Causa
Non hai ancora fatto pull del branch o non esiste localmente.

### Soluzione

```bash
# Fetch tutti i branch
git fetch --all

# Lista branch disponibili
git branch -a

# Checkout del branch
git checkout refactor/package-structure

# Oppure crea da zero (se hai solo i commit)
git checkout -b refactor/package-structure
```

---

## ❌ pip install -e . fallisce

### Problema
```bash
pip install -e .
# ERROR: File "setup.py" not found...
```

### Causa possibili

1. **Non sei nella directory root del progetto**
2. **pyproject.toml mancante**
3. **setuptools troppo vecchio**

### Soluzione

```bash
# 1. Verifica di essere nella root
ls pyproject.toml
# Dovrebbe esistere

# 2. Aggiorna setuptools
pip install --upgrade setuptools wheel pip

# 3. Riprova
pip install -e .

# 4. Se ancora non funziona, prova senza editable
pip install .
```

---

## 🆘 Altre Soluzioni

### Reset completo

Se niente funziona, prova un reset completo:

```bash
# 1. Disinstalla tutto
pip uninstall mobility-book-style -y

# 2. Pulisci cache
pip cache purge
rm -rf build dist *.egg-info

# 3. Pulisci __pycache__
find . -type d -name __pycache__ -exec rm -r {} +

# 4. Reinstalla
pip install -e ".[all]"

# 5. Verifica
python -c "import mobility_book_style as mbs; print(mbs.__version__)"
```

### Verifica Installazione

Script di test completo:

```python
import sys
print(f"Python: {sys.version}")
print(f"Executable: {sys.executable}")

try:
    import mobility_book_style as mbs
    print(f"✅ mobility_book_style v{mbs.__version__}")
except Exception as e:
    print(f"❌ Import error: {e}")

try:
    import matplotlib
    print(f"✅ matplotlib v{matplotlib.__version__}")
except Exception as e:
    print(f"❌ matplotlib: {e}")

try:
    import altair
    print(f"✅ altair v{altair.__version__}")
except Exception as e:
    print(f"⚠️  altair: {e}")
```

---

## 📞 Supporto

Se il problema persiste:

1. Apri un issue su GitHub con:
   - Output di `pip list`
   - Output di `python --version`
   - Traceback completo dell'errore
   - Sistema operativo

2. Consulta la documentazione:
   - **README_NEW.md**: Documentazione completa
   - **MIGRATION.md**: Guida migrazione
   - **examples/demo_new_api.ipynb**: Esempi funzionanti

---

**Ultimo aggiornamento**: 6 Novembre 2025  
**Branch**: `refactor/package-structure`
