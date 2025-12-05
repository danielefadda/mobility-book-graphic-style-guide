# 🎨 Guida alla Modifica dei Design Token, Alias e Temi

Questa guida spiega come aggiornare i design token, gli alias colore e i temi della libreria di stile Mobility Book.

---

## 📚 Indice

- [Concetti Fondamentali](#concetti-fondamentali)
- [Architettura dei Token](#architettura-dei-token)
- [Workflow Completo](#workflow-completo)
- [Esempi Pratici](#esempi-pratici)
- [Checklist per Aggiornamenti](#checklist-per-aggiornamenti)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Concetti Fondamentali

Il sistema di design token si basa su **3 livelli interconnessi**:

### 1️⃣ **Alias Primitivi** (`colors/alias.json`)
Valori esadecimali grezzi — la base di tutto.

```
Alias → #348b96 (valore concreto)
```

### 2️⃣ **Design Tokens Semantici** (`design_tokens/design_tokens.json`)
Concetti e riferimenti ai colori primitivi — struttura logica.

```
Design Token → brand-primary → {colors.teal.500} → {alias.teal-500} → #348b96
```

### 3️⃣ **Python** (`mobility_book_style/_tokens.py`, `_colors.py`)
Implementazione pratica usata dai builder (Matplotlib, Altair, Plotly).

```
TOKENS["color"]["accent"] → ALIAS_COLORS["teal-500"] → #348b96
```

**Principio fondamentale**: Modifica sempre dal livello più basso e il resto si propaga automaticamente.

---

## 🏗️ Architettura dei Token

### Gerarchia dei File

```
colors/
├── alias.json              ← Valori HEX primitivi
└── alias_colors.py         ← Wrapper Python per gli alias

design_tokens/
├── design_tokens.json      ← Struttura semantica (riferimenti)
└── design_tokens.py        ← Python dict con i token

mobility_book_style/
├── _colors.py              ← ALIAS_COLORS importato
├── _tokens.py              ← TOKENS per i builder
└── [matplotlib.py, altair.py, ...]  ← Usano i token
```

### Flusso di Propagazione

```
alias.json (primario)
    ↓ (riferimento JSON)
design_tokens.json (semantico)
    ↓ (importazione Python)
_colors.py / _tokens.py
    ↓ (consumo)
Builder (matplotlib, altair, plotly)
    ↓
Visualizzazione finale
```

---

## 🔄 Workflow Completo

### **Livello 1: Alias Primitivi** (`colors/alias.json`)

Questo file contiene i valori esadecimali grezzi per tutti i colori.

**Struttura attuale:**

```json
{
  "teal-050": "#aaffff",
  "teal-100": "#8fe3ee",
  "teal-500": "#348b96",
  "teal-600": "#00616c",
  "burgundy-500": "#981b40",
  "burgundy-600": "#7b0029",
  "purple-500": "#534e93",
  "black-500": "#262a33",
  "white-500": "#ffffff"
}
```

#### Come Modificare

**Caso 1: Aggiornare un colore esistente**

Prima:
```json
{
  "teal-500": "#348b96"
}
```

Dopo:
```json
{
  "teal-500": "#3fa5ac"    // ← Teal più chiaro
}
```

**Caso 2: Aggiungere un nuovo colore**

```json
{
  "teal-500": "#348b96",
  "teal-550": "#378a98",    // ← Nuovo step intermedio
  "teal-600": "#00616c"
}
```

**Regole:**
- ✅ Modifica solo valori HEX
- ✅ Mantieni la nomenclatura `{colore}-{intensità}` (050-900)
- ✅ Cambia anche in `_colors.py` se necessario
- ❌ Non aggiungere commenti (JSON puro)

---

### **Livello 2: Design Tokens Semantici** (`design_tokens/design_tokens.json`)

Qui i colori primitivi diventano concetti logici (brand, stato, componente).

**Struttura:**

```json
{
  "colors": {
    "teal": {
      "500": "{alias.teal-500}",
      "600": "{alias.teal-600}"
    }
  },
  "semantic": {
    "brand-primary": { "value": "{colors.teal.500}" },
    "success": { "value": "{colors.teal.600}" }
  },
  "components": {
    "button": {
      "primary-bg": { "value": "{semantic.brand-primary}" },
      "primary-hover": { "value": "{colors.teal.600}" }
    }
  },
  "stroke": {
    "thin": { "value": "1px" },
    "medium": { "value": "2px" },
    "bold": { "value": "3px" }
  }
}
```

#### Come Modificare

**Caso 1: Cambiare un colore semantico**

Prima:
```json
{
  "semantic": {
    "brand-primary": { "value": "{colors.teal.500}" }
  }
}
```

Dopo:
```json
{
  "semantic": {
    "brand-primary": { "value": "{colors.teal.600}" }  // ← Usa il 600 invece
  }
}
```

**Caso 2: Aggiungere uno spessore di linea**

```json
{
  "stroke": {
    "thin": { "value": "1px" },
    "medium": { "value": "2px" },
    "bold": { "value": "3px" },
    "extra-bold": { "value": "4px" }    // ← Nuovo
  }
}
```

**Caso 3: Aggiungere un nuovo colore semantico**

```json
{
  "semantic": {
    "brand-primary": { "value": "{colors.teal.500}" },
    "brand-secondary": { "value": "{colors.burgundy.500}" },  // ← Nuovo
    "info": { "value": "{colors.darkviolet.500}" }
  }
}
```

**Regole:**
- ✅ Usa sempre riferimenti `{alias.xxx}` o `{colors.xxx}` o `{semantic.xxx}`
- ✅ Mantieni la struttura gerarchica
- ✅ Non duplicare valori: se esiste `teal-500`, usalo
- ❌ Non inserire valori HEX direttamente (eccetto casi speciali come componenti hardcoded)

---

### **Livello 3: Python** (`mobility_book_style/_tokens.py`)

Qui i token vengono **consumati** dai builder.

**Struttura attuale:**

```python
from ._colors import ALIAS_COLORS

TOKENS = {
    "font": {
        "base_stack": "Inter, IBM Plex Sans, DejaVu Sans, Arial, sans-serif",
        "weight_regular": 400,
        "weight_bold": 600,
    },
    "color": {
        "text": ALIAS_COLORS["black"],
        "accent": ALIAS_COLORS["blue-60"],
        "body_border": ALIAS_COLORS["gray-20"],
    },
    "chart": {
        "title_size_px": 16,
        "label_size_px": 12,
        "line_width": 2.0,
    },
    "table": {
        "title_px": 18,
        "header_px": 14,
        "body_px": 14,
        "spanner_color": ALIAS_COLORS["black"],
        "body_border": ALIAS_COLORS["gray-20"],
    },
}

# Derivati in punti tipografici (Matplotlib/LaTeX)
TOKENS_PT = {
    "chart": {
        "title_pt": px_to_pt(TOKENS["chart"]["title_size_px"]),
    },
}
```

#### Come Modificare

**Caso 1: Cambiare uno spessore di linea**

Prima:
```python
TOKENS = {
    "chart": {
        "line_width": 2.0,
    }
}
```

Dopo:
```python
TOKENS = {
    "chart": {
        "line_width": 2.5,    # ← Linee più spesse
    }
}
```

**Caso 2: Cambiare un colore**

Prima:
```python
TOKENS = {
    "color": {
        "accent": ALIAS_COLORS["blue-60"],
    }
}
```

Dopo:
```python
TOKENS = {
    "color": {
        "accent": ALIAS_COLORS["teal-500"],    # ← Usa teal invece
    }
}
```

**Caso 3: Aggiungere un nuovo token**

```python
TOKENS = {
    "chart": {
        "line_width": 2.0,
        "line_width_hover": 3.0,    # ← Nuovo
    }
}
```

**Regole:**
- ✅ Usa sempre `ALIAS_COLORS["key"]` per i colori
- ✅ Aggiungi conversioni in `TOKENS_PT` se necessario
- ✅ Documenta con commenti se non ovvio
- ✅ I derivati in PT si calcolano automaticamente con `px_to_pt()`
- ❌ Non usare valori HEX direttamente

---

## 🔄 Sincronizzazione e Aggiornamento della Libreria

### Come si Propaga un Cambiamento?

La libreria **legge direttamente i file Python** (`_colors.py`, `_tokens.py`) al momento dell'import. Questo significa:

**✅ Modifiche Python → Effetto Immediato**
- Se modifichi `mobility_book_style/_tokens.py` o `_colors.py`
- **Basta riavviare il kernel/script Python**
- Nessun build necessario

**⚠️ Modifiche JSON → Manuale**
- Se modifichi `colors/alias.json` o `design_tokens/design_tokens.json`
- **Devi sincronizzare manualmente i file Python**

### Workflow di Sincronizzazione

#### Caso 1: Modifiche solo a Python (`_tokens.py`)

```python
# File: mobility_book_style/_tokens.py

TOKENS = {
    "chart": {
        "line_width": 2.5,  # ← Cambio da 2.0 a 2.5
    }
}
```

**Azione richiesta:**
```python
# Riavvia kernel o script
import importlib
import mobility_book_style
importlib.reload(mobility_book_style)  # Ricarica le modifiche
```

**Nessun build necessario** ✅

---

#### Caso 2: Modifiche a JSON (`alias.json`)

```json
// File: colors/alias.json

{
  "teal-500": "#3fa5ac"  // ← Cambio da #348b96
}
```

**Azione richiesta:**

1. **Sincronizza manualmente** `_colors.py`:
   ```python
   # File: mobility_book_style/_colors.py
   
   ALIAS_COLORS = {
       "teal-500": "#3fa5ac",  # ← Aggiorna manualmente
   }
   ```

2. **Riavvia il kernel/script:**
   ```python
   import importlib
   import mobility_book_style
   importlib.reload(mobility_book_style)
   ```

**⚠️ Attenzione**: `alias.json` è documentazione/riferimento, ma **`_colors.py` è la source of truth** per Python.

---

#### Caso 3: Modifiche a `design_tokens.json`

I `design_tokens.json` sono principalmente **documentazione della struttura logica**. I builder Python (`matplotlib.py`, `altair.py`) leggono direttamente da `_tokens.py`.

**Se modifichi** `design_tokens.json`:
1. Aggiorna i corrispondenti token in `_tokens.py`
2. Riavvia il kernel

**Nessuno script di build da eseguire** ✅

---

### Riepilogo: Cosa Fare Dopo le Modifiche?

| Modifica | File Python | Script Build | Riavvio Kernel |
|----------|-------------|--------------|----------------|
| `_tokens.py` | ✅ Modificato | ❌ No | ✅ Sì |
| `_colors.py` | ✅ Modificato | ❌ No | ✅ Sì |
| `alias.json` | ⚠️ Sincronizza `_colors.py` manualmente | ❌ No | ✅ Sì |
| `design_tokens.json` | ⚠️ Sincronizza `_tokens.py` manualmente | ❌ No | ✅ Sì |

### Come Riavviare Correttamente

**In Jupyter Notebook:**
```python
# Opzione 1: Restart Kernel (UI)
# Menu → Kernel → Restart

# Opzione 2: Reload moduli (in cella)
import importlib
import mobility_book_style
importlib.reload(mobility_book_style)
```

**In Script Python:**
```bash
# Riesegui lo script
python my_chart.py
```

**Nessun comando `npm run build`, `make`, o simili** — la libreria è puramente Python e legge i file direttamente.

---

## 📝 Esempi Pratici

### Esempio 1: Schiarire il Teal Primario

**Obiettivo**: Il `teal-500` è troppo scuro, vogliamo schiarirlo da `#348b96` a `#3fa5ac`

#### Step 1: Modifica alias.json

```bash
File: colors/alias.json
```

```diff
{
  "teal-050": "#aaffff",
- "teal-500": "#348b96",
+ "teal-500": "#3fa5ac",
  "teal-600": "#00616c",
}
```

#### Step 2: Verifica design_tokens.json

```bash
File: design_tokens/design_tokens.json
```

```json
{
  "colors": {
    "teal": {
      "500": "{alias.teal-500}"    // ✅ È già un riferimento!
    }
  },
  "semantic": {
    "brand-primary": { "value": "{colors.teal.500}" }  // ✅ Automatico
  }
}
```

**Non serve modificare nulla**: il riferimento si aggiorna automaticamente.

#### Step 3: Verifica Python

```bash
File: mobility_book_style/_tokens.py
```

Se in `_colors.py` esiste:

```python
ALIAS_COLORS = {
    "teal-500": "#3fa5ac",  # ← Aggiornato da alias.json
}
```

Allora in `_tokens.py`:

```python
TOKENS = {
    "color": {
        "accent": ALIAS_COLORS["teal-500"],  # ✅ Già usa il nuovo valore
    }
}
```

**Risultato finale**: Tutti i grafici che usano `brand-primary` o `accent` diventano più chiari.

---

### Esempio 2: Aggiungere Spessori di Linea Configurabili

**Obiettivo**: Passare da un singolo `line_width: 2.0` a spessori configurabili (thin/medium/bold)

#### Step 1: design_tokens.json

```bash
File: design_tokens/design_tokens.json
```

Aggiungi una nuova sezione:

```json
{
  "stroke": {
    "thin": { "value": "1.0" },
    "medium": { "value": "2.0" },
    "bold": { "value": "3.0" },
    "extra-bold": { "value": "4.0" }
  }
}
```

#### Step 2: _tokens.py

```bash
File: mobility_book_style/_tokens.py
```

Modifica:

```python
TOKENS = {
    "chart": {
        "line_width": 2.0,              # ← Vecchio singolo valore
    }
}
```

In:

```python
TOKENS = {
    "chart": {
        "line_width_thin": 1.0,
        "line_width_medium": 2.0,
        "line_width_bold": 3.0,
        "line_width_extra_bold": 4.0,
    }
}
```

#### Step 3: Usa nel Builder

```bash
File: builders/matplotlib_builder.py (o altair_builder.py)
```

Invece di:

```python
plt.plot(x, y, linewidth=TOKENS["chart"]["line_width"])
```

Usa:

```python
plt.plot(x, y, linewidth=TOKENS["chart"]["line_width_medium"])
```

---

### Esempio 3: Cambiare Colore Semantico Globale

**Obiettivo**: Il brand secondary deve passare da burgundy a purple

#### Step 1: design_tokens.json

```bash
File: design_tokens/design_tokens.json
```

Prima:
```json
{
  "semantic": {
    "brand-secondary": { "value": "{colors.burgundy.500}" }
  }
}
```

Dopo:
```json
{
  "semantic": {
    "brand-secondary": { "value": "{colors.purple.500}" }
  }
}
```

#### Step 2: _tokens.py

Se usi il token semantico, non serve modificare nulla. Se hai una reference diretta:

```python
TOKENS = {
    "color": {
        "accent_secondary": ALIAS_COLORS["burgundy-500"],
    }
}
```

Cambia in:

```python
TOKENS = {
    "color": {
        "accent_secondary": ALIAS_COLORS["purple-500"],
    }
}
```

**Risultato**: Tutti gli elementi "secondary" diventano purple.

---

## ✅ Checklist per Aggiornamenti

Prima di fare un commit, verifica:

### Modifica Colore Primitivo

- [ ] Ho aggiornato `colors/alias.json`
- [ ] Ho controllato che il nuovo HEX sia valido
- [ ] Ho aggiornato `_colors.py` se necessario (di solito generato automaticamente)
- [ ] Ho verificato che tutti i riferimenti rimangano validi
- [ ] Ho testato i builder (Matplotlib/Altair) per visibilità

### Aggiunta Token Nuovo

- [ ] Ho aggiunto in `design_tokens.json` con nomenclatura coerente
- [ ] Ho documentato il nuovo token con commenti
- [ ] Ho aggiunto in `_tokens.py` se consumato dai builder
- [ ] Ho aggiunto in `TOKENS_PT` se serve conversione a punti
- [ ] Ho testato l'accesso dal builder

### Cambio Struttura Semantica

- [ ] Ho mantenuto la gerarchia logica
- [ ] Ho usato riferimenti `{...}` non valori HEX
- [ ] Ho documentato perché cambio
- [ ] Ho cercato tutti gli usi del token vecchio
- [ ] Ho aggiornato docstrings se necessario

### Test Finali

- [ ] Ho importato i moduli senza errori (`python -c "from mobility_book_style import TOKENS"`)
- [ ] Ho verificato che i builder leggano i nuovi token
- [ ] Ho fatto girare gli esempi in `examples/demo_new_api.ipynb`
- [ ] Ho controllato che il colore sia visivamente corretto

---

## 🔍 Troubleshooting

### ❌ "KeyError: 'teal-500' in _colors.py"

**Causa**: Hai modificato `alias.json` ma `_colors.py` non è aggiornato.

**Soluzione**: 
```bash
# Rigenera _colors.py da alias.json (se hai uno script)
python generate_colors.py
```

Oppure aggiorna manualmente `_colors.py`:
```python
ALIAS_COLORS = {
    "teal-500": "#3fa5ac",  # ← Aggiornato
}
```

---

### ❌ "ReferenceError: {alias.teal-999} not found"

**Causa**: Hai usato un alias che non esiste in `alias.json`.

**Soluzione**: 
1. Verifica l'ortografia in `alias.json`
2. Se è nuovo, aggiungilo prima di usare il riferimento

```json
// alias.json
{
  "teal-999": "#abcdef"  // ← Aggiungi qui
}

// design_tokens.json
{
  "colors": {
    "teal": {
      "999": "{alias.teal-999}"  // ← Ora esiste
    }
  }
}
```

---

### ❌ "I colori non cambiano nei grafici"

**Causa**: Il builder non legge i token aggiornati.

**Soluzione**:
1. Verifica che il builder importi `TOKENS` da `_tokens.py`
   ```python
   from mobility_book_style._tokens import TOKENS  # ✅ Corretto
   ```

2. Verifica che il builder usi il token aggiornato
   ```python
   color = TOKENS["color"]["accent"]  # ← Controlla la chiave
   ```

3. Ripulisci cache Python
   ```bash
   find . -type d -name __pycache__ -exec rm -rf {} +
   python -c "import mobility_book_style; print('OK')"
   ```

---

### ❌ "JSON invalido in design_tokens.json"

**Causa**: Errore di sintassi JSON (parentesi, virgole, quote).

**Soluzione**: Valida il JSON
```bash
python -m json.tool design_tokens/design_tokens.json > /dev/null
```

Se fallisce, mostra l'errore. Correggi:
- ✅ Tutte le virgole prima di `}` o `]`
- ✅ Tutti i `{` chiusi con `}`
- ✅ Tutte le stringhe con `"` doppi

---

### ❌ "Il riferimento {colors.teal.500} non si risolve"

**Causa**: La gerarchia in `design_tokens.json` non è corretta.

**Soluzione**: Verifica la struttura:

```json
// ✅ Corretto
{
  "colors": {
    "teal": {
      "500": "{alias.teal-500}"
    }
  },
  "semantic": {
    "brand-primary": { "value": "{colors.teal.500}" }
  }
}

// ❌ Sbagliato: teal non è annidato
{
  "colors": {
    "teal-500": "{alias.teal-500}"
  }
}
```

---

## 📚 File di Riferimento Rapido

| File | Scopo | Quando Modificare |
|------|-------|-------------------|
| `colors/alias.json` | Valori HEX primitivi | Quando cambiano i colori base |
| `colors/alias_colors.py` | Dict Python dei colori | Quando aggiungi alias nuovi |
| `design_tokens/design_tokens.json` | Semantica e componenti | Quando definisci nuovi concetti |
| `design_tokens/design_tokens.py` | (Documentazione) | Raramente |
| `mobility_book_style/_colors.py` | ALIAS_COLORS importato | Auto-sincronizzato da alias.json |
| `mobility_book_style/_tokens.py` | TOKENS consumati dai builder | Quando aggiungi token nuovi |
| `mobility_book_style/matplotlib.py` | Builder Matplotlib | Quando usi token nei grafici |
| `mobility_book_style/altair.py` | Builder Altair | Quando usi token nei grafici |

---

## 🎯 Best Practices

1. **Partisci sempre dal livello più basso** (alias.json)
   - I livelli superiori si aggiornano automaticamente

2. **Usa referenze, non valori HEX**
   - Scrivi `{alias.teal-500}` non `"#348b96"`
   - Rende tutto tracciabile e manutenibile

3. **Nomina semanticamente**
   - `brand-primary` anziché `teal-primary`
   - `danger` anziché `red-600`
   - Facilita i cambiamenti futuri

4. **Mantieni pochi valori standard**
   - 3-4 spessori di linea (`thin`, `medium`, `bold`)
   - Colori principali + varianti scure/chiare
   - Riduce complessità e mantiene coerenza

5. **Documenta con commenti**
   ```python
   # Spessore delle linee nei grafici (attenzione: Matplotlib converte in pt)
   "line_width": 2.0,
   ```

6. **Testa sempre dopo modifiche**
   - Import: `python -c "from mobility_book_style import TOKENS"`
   - Visuale: Genera un grafico con il builder aggiornato
   - Generato: Valida JSON con `python -m json.tool`

---

## 📞 Supporto

Se hai domande o problemi:

1. Controlla il **Troubleshooting** sopra
2. Verifica la **Checklist for Aggiornamenti**
3. Rivedi gli **Esempi Pratici** per il tuo caso
4. Leggi i commenti nel codice sorgente

---

**Ultima modifica**: Dicembre 2025  
**Versione**: 1.0  
**Autore**: Mobility Book Team
