# 🔧 Guida all'Aggiornamento dei Design Token

Questa guida spiega come modificare i design token della libreria Mobility Book Style.

---

## 📚 Indice

- Architettura
- Workflow di Modifica
- Esempi Pratici
- Troubleshooting

---

## 🏗️ Architettura

La libreria usa **design_tokens.json** come unica source of truth:

```
mobility_book_style/
├── data/
│   └── design_tokens.json      ← Token (colori, chart, component, font)
├── _tokens.py                  ← Loader + oggetto token (dot-notation)
└── matplotlib.py / altair.py   ← Usano i token risolti
```

### Flusso di Caricamento

```
1. import mobility_book_style as mbs
   ↓
2. _tokens.py carica design_tokens.json e risolve i riferimenti {color...}
   ↓
3. Espone mbs.token (dot-notation) e token_dict (dizionario) già risolti
   ↓
4. matplotlib.py / altair.py / export.py leggono quei valori
```

**Principio**: Modifica i JSON, il resto si aggiorna automaticamente. ✨

---

## 📝 Workflow di Modifica

### Step 1: Identifica il File da Modificare

| Cosa vuoi cambiare | File da modificare |
|--------------------|-------------------|
| Palette base, semantica, chart/component/font | `mobility_book_style/data/design_tokens.json` |

### Step 2: Modifica il JSON

#### Esempio: Aggiungere nuovo spessore linea

**File**: `mobility_book_style/data/design_tokens.json`

```json
{
  "chart": {
    "element": {
      "axis": {
        "width": { "value": "1.2pt" }
      }
    }
  }
}
```

### Step 3: Valida il JSON

```bash
python -m json.tool mobility_book_style/data/design_tokens.json > /dev/null
```

### Step 4: Ricarica il Kernel

- In Jupyter: `Kernel → Restart`
- In uno script: riesegui lo script

### Step 5: Verifica

```python
import mobility_book_style as mbs

print(mbs.token.color.brand.primary)
print(mbs.token.chart.element.grid.width)
```

---

## 📝 Esempi Pratici

### Esempio 1: Schiarire il Colore Primario

**Obiettivo**: Il teal è troppo scuro.

```json
{
  "color": {
    "base": {
      "teal": {
        "500": { "value": "#4bb5bf" }
      }
    },
    "brand": {
      "primary": { "value": "{color.base.teal.500}" }
    }
  }
}
```

Valida, riavvia il kernel, verifica con un grafico.

### Esempio 2: Aggiungere una Scala Orange

```json
{
  "color": {
    "base": {
      "orange": {
        "100": { "value": "#ffe0b2" },
        "500": { "value": "#ff9800" },
        "900": { "value": "#e65100" }
      }
    },
    "intent": {
      "warning": { "value": "{color.base.orange.500}" }
    }
  }
}
```

### Esempio 3: Modificare Spessore Linee

```json
{
  "chart": {
    "element": {
      "line": {
        "width": { "value": "2.5pt" }
      }
    }
  }
}
```

### Esempio 4: Cambiare Brand Accent

```json
{
  "color": {
    "brand": {
      "accent": { "value": "{color.base.purple.500}" }
    }
  }
}
```

---

## 🔍 Troubleshooting

### ❌ "FileNotFoundError: design_tokens.json non trovato"

**Soluzione**: Verifica che il file esista in `mobility_book_style/data/design_tokens.json`.

### ❌ "JSONDecodeError: File malformato"

Valida con:

```bash
python -m json.tool mobility_book_style/data/design_tokens.json
```

Errori comuni: virgole finali, apici singoli, commenti.

### ❌ "KeyError: path non trovato"

Il percorso `{color....}` non esiste. Aggiungilo in `design_tokens.json` nella famiglia corretta (es. `color.base.custom`).

### ❌ "I colori non cambiano nei grafici"

Riavvia il kernel o la sessione Python dopo la modifica del JSON.

---

## ✅ Checklist Pre-Commit

- [ ] Ho modificato `mobility_book_style/data/design_tokens.json`
- [ ] Ho validato il JSON: `python -m json.tool mobility_book_style/data/design_tokens.json > /dev/null`
- [ ] Ho riavviato il kernel e verificato i valori
- [ ] Ho testato visivamente un grafico
- [ ] I test passano: `pytest tests/`

---

## 💡 Best Practices

1. Modifica sempre il JSON, non `_tokens.py`.
2. Usa nomi semantici coerenti (es. `color.brand.primary`).
3. Valida sempre con `python -m json.tool`.
4. Testa visivamente (Matplotlib/Altair) dopo le modifiche.
5. Documenta i cambiamenti nei commit.

---

## �� Riferimento Rapido: Struttura design_tokens.json (minimale)

```json
{
  "color": {
    "base": {
      "teal": {
        "500": { "value": "#348b96" }
      }
    },
    "brand": {
      "primary": { "value": "{color.base.teal.500}" }
    }
  },
  "font": {
    "family": {
      "sans": { "value": "Inter, sans-serif" }
    }
  }
}
```
