# 🔧 Guida all'Aggiornamento dei Design Token

Questa guida spiega come modificare i design token e gli alias colori della libreria Mobility Book Style.

---

## 📚 Indice

- [Architettura](#architettura)
- [Workflow di Modifica](#workflow-di-modifica)
- [Esempi Pratici](#esempi-pratici)
- [Troubleshooting](#troubleshooting)

---

## 🏗️ Architettura

La libreria usa **JSON come source of truth**:

```
mobility_book_style/
├── data/
│   ├── alias.json              ← Colori primitivi (HEX)
│   └── design_tokens.json      ← Token semantici e configurazioni
├── _colors.py                  ← Carica alias.json → ALIAS_COLORS
├── _tokens.py                  ← Carica design_tokens.json → TOKENS
└── matplotlib.py / altair.py   ← Usano TOKENS
```

### Flusso di Caricamento

```
1. Import: from mobility_book_style import TOKENS
   ↓
2. _tokens.py carica design_tokens.json
   ↓
3. Risolve {alias.xxx} usando ALIAS_COLORS (da alias.json)
   ↓
4. I builder (matplotlib, altair) usano TOKENS
```

**Principio**: Modifica i JSON, il resto si aggiorna automaticamente! ✨

---

## 📝 Workflow di Modifica

### Step 1: Identifica il File da Modificare

| Cosa vuoi cambiare | File da modificare |
|--------------------|-------------------|
| Valore HEX di un colore | `mobility_book_style/data/alias.json` |
| Aggiungere un nuovo colore | `mobility_book_style/data/alias.json` |
| Cambiare semantica (brand, text, etc.) | `mobility_book_style/data/design_tokens.json` |
| Spessore linee, dimensioni font | `mobility_book_style/data/design_tokens.json` |

### Step 2: Modifica il JSON

#### Esempio: Cambiare il colore teal

**File**: `mobility_book_style/data/alias.json`

```json
{
  "teal-500": "#3fa5ac"  // ← Nuovo valore (era #348b96)
}
```

#### Esempio: Aggiungere nuovo spessore linea

**File**: `mobility_book_style/data/design_tokens.json`

```json
{
  "chart": {
    "line_width": 2.5  // ← Modificato (era 2.0)
  }
}
```

### Step 3: Valida il JSON

```bash
python -m json.tool mobility_book_style/data/alias.json > /dev/null
python -m json.tool mobility_book_style/data/design_tokens.json > /dev/null
```

Se non mostra errori → ✅ OK!

### Step 4: Ricarica il Kernel

**In Jupyter Notebook:**

```
Menu → Kernel → Restart
```

**In Script Python:**

```bash
python mio_script.py  # Riesegui semplicemente
```

**Con importlib (avanzato):**

```python
import importlib
import mobility_book_style._colors
import mobility_book_style._tokens

importlib.reload(mobility_book_style._colors)
importlib.reload(mobility_book_style._tokens)
```

### Step 5: Verifica

```python
from mobility_book_style import ALIAS_COLORS, TOKENS

print(ALIAS_COLORS["teal-500"])  # Nuovo valore
print(TOKENS["chart"]["line_width"])  # Nuovo valore
```

---

## 📝 Esempi Pratici

### Esempio 1: Schiarire il Colore Primario

**Obiettivo**: Il teal è troppo scuro, vogliamo schiarirlo.

#### 1. Modifica `alias.json`

```json
{
  "teal-500": "#4bb5bf"  // ← Più chiaro (era #348b96)
}
```

#### 2. Valida

```bash
python -m json.tool mobility_book_style/data/alias.json > /dev/null
# ✅ OK
```

#### 3. Restart Kernel

```python
# In Jupyter: Kernel → Restart
```

#### 4. Testa

```python
import mobility_book_style as mbs
import matplotlib.pyplot as plt

mbs.apply_matplotlib_theme()

plt.plot([1, 2, 3], [1, 2, 3])
plt.show()  # Il colore sarà più chiaro ✅
```

---

### Esempio 2: Aggiungere Nuovi Colori

**Obiettivo**: Vogliamo aggiungere una scala di arancio.

#### 1. Aggiungi ad `alias.json`

```json
{
  "orange-050": "#fff5e6",
  "orange-100": "#ffe0b2",
  "orange-200": "#ffcc80",
  "orange-300": "#ffb74d",
  "orange-400": "#ffa726",
  "orange-500": "#ff9800",
  "orange-600": "#fb8c00",
  "orange-700": "#f57c00",
  "orange-800": "#ef6c00",
  "orange-900": "#e65100"
}
```

#### 2. Usa in `design_tokens.json`

```json
{
  "colors": {
    "orange": {
      "500": "{alias.orange-500}"
    }
  },
  "semantic": {
    "warning": { "value": "{colors.orange.500}" }
  }
}
```

#### 3. Valida e Restart

```bash
python -m json.tool mobility_book_style/data/alias.json > /dev/null
python -m json.tool mobility_book_style/data/design_tokens.json > /dev/null
# Kernel → Restart
```

---

### Esempio 3: Modificare Spessore Linee

**Obiettivo**: Le linee nei grafici sono troppo sottili.

#### 1. Modifica `design_tokens.json`

```json
{
  "chart": {
    "line_width": 2.5  // ← Più spesse (era 2.0)
  }
}
```

#### 2. Valida e Restart

```bash
python -m json.tool mobility_book_style/data/design_tokens.json > /dev/null
# Kernel → Restart
```

#### 3. Testa

```python
import mobility_book_style as mbs
import matplotlib.pyplot as plt

mbs.apply_matplotlib_theme()

plt.plot([1, 2, 3], [1, 4, 2], linewidth=None)  # Usa il default
plt.show()  # Linee più spesse ✅
```

---

### Esempio 4: Cambiare Brand Accent

**Obiettivo**: L'accent deve passare da burgundy a purple.

#### 1. Modifica `design_tokens.json`

```json
{
  "semantic": {
    "brand-accent": { "value": "{colors.purple.500}" }  // ← Era burgundy.500
  }
}
```

#### 2. Valida e Restart

```bash
python -m json.tool mobility_book_style/data/design_tokens.json > /dev/null
# Kernel → Restart
```

Tutti gli elementi "accent" ora usano purple ✅

---

## 🔍 Troubleshooting

### ❌ "FileNotFoundError: alias.json non trovato"

**Soluzione**: Verifica che i file siano in:
```
mobility_book_style/data/alias.json
mobility_book_style/data/design_tokens.json
```

---

### ❌ "JSONDecodeError: File malformato"

**Causa**: Errore di sintassi nel JSON.

**Soluzione**: Valida il JSON per vedere l'errore esatto:

```bash
python -m json.tool mobility_book_style/data/alias.json
```

Errori comuni:
- ❌ Virgola finale: `{"a": 1,}` → ✅ `{"a": 1}`
- ❌ Apici singoli: `{'a': 1}` → ✅ `{"a": 1}`
- ❌ Commenti: JSON non li supporta

---

### ❌ "I colori non cambiano nei grafici"

**Causa**: Il kernel Python non è stato restartato.

**Soluzione**:
```python
# In Jupyter
Kernel → Restart

# Oppure
import importlib
import mobility_book_style._colors
import mobility_book_style._tokens
importlib.reload(mobility_book_style._colors)
importlib.reload(mobility_book_style._tokens)
```

---

### ❌ "KeyError: 'my-color' non trovato"

**Causa**: Stai usando un alias che non esiste.

**Soluzione**: Aggiungilo prima ad `alias.json`:

```json
{
  "my-color": "#abcdef"
}
```

Poi puoi riferirlo in `design_tokens.json`:

```json
{
  "colors": {
    "custom": {
      "500": "{alias.my-color}"
    }
  }
}
```

---

## ✅ Checklist Pre-Commit

Prima di committare modifiche ai token:

- [ ] Ho modificato i file in `mobility_book_style/data/`
- [ ] Ho validato i JSON: `python -m json.tool file.json > /dev/null`
- [ ] Ho restartato il kernel e verificato i valori
- [ ] Ho testato visivamente un grafico
- [ ] I test passano: `pytest tests/`

---

## 💡 Best Practices

1. **Modifica sempre i JSON**: Non modificare `_colors.py` o `_tokens.py`
2. **Usa nomi semantici**: `brand-primary` invece di `teal-500`
3. **Mantieni pochi valori**: 3-5 spessori, colori principali + varianti
4. **Valida sempre**: `python -m json.tool` prima di committare
5. **Testa visivamente**: Genera un grafico per verificare
6. **Documenta cambiamenti**: Aggiungi commenti nei commit

---

## 📚 Riferimenti Rapidi

### Struttura alias.json

```json
{
  "colore-variante": "#RRGGBB"
}
```

Esempio:
```json
{
  "teal-500": "#348b96",
  "burgundy-600": "#7b0029"
}
```

### Struttura design_tokens.json

```json
{
  "colors": {
    "famiglia": {
      "variante": "{alias.colore-variante}"
    }
  },
  "semantic": {
    "nome-semantico": { "value": "{colors.famiglia.variante}" }
  }
}
```

### Riferimenti Supportati

- `{alias.nome}` - Riferimento ad alias.json
- `{colors.famiglia.variante}` - Riferimento a colors in design_tokens.json
- `{semantic.nome}` - Riferimento a semantic in design_tokens.json

---

## 🚀 Deploy

Dopo le modifiche, per distribuire:

```bash
# I JSON sono automaticamente inclusi nel package
pip install -e .

# Oppure build per distribuzione
python -m build
```

I file JSON sono inclusi grazie a `pyproject.toml`:

```toml
[tool.setuptools.package-data]
mobility_book_style = ["data/*.json", "fonts/*.ttf"]
```

---

**Ultima modifica**: Dicembre 2025  
**Versione**: 2.0
