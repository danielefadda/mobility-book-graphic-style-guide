# Book Mobility Design System

This repository contains the design system for Book Mobility, including color palettes, design tokens, and builders for various visualization libraries such as Altair and Matplotlib. The goal is to ensure consistent styling across all visualizations related to Book Mobility.

## Repository Structure

```
book_mobility_style/
│
├─ colors/
│  ├─ alias_colors.py
│  └─ preview_palette.ipynb
├─ design_tokens/
│  └─ design_tokens.py
├─ builders/
│  ├─ altair_builder.py
│  ├─ matplotlib_builder.py
│  ├─ css_builder.py              # (opzionale)
│  └─ latex_builder.py            # ⚠️ Feature to be added
├─ themes/
│  ├─ altair_mobility_theme.py
│  ├─ mpl_mobility_style.mplstyle
│  └─ latex_mobility_style.tex    # ⚠️ Feature to be added
├─ examples/
│  ├─ altair_demo.ipynb
│  ├─ matplotlib_demo.ipynb
│  └─ latex_demo.tex              # ⚠️ Feature to be added
├─ docs/
│  ├─ index.md
│  ├─ _config.yml
│  ├─ assets/
│  └─ sections/ (colors.md, tokens.md, builders.md, templates.md, examples.md)
└─ README.md
```

## Workflow Overview

The workflow for creating and using the Book Mobility design system can be summarized in three main steps:

1. Define the primitive color palette (aliases)
2. Create design tokens based on the primitive palette
3. Build templates or libraries using the design tokens

| PALETTE PRIMITIVA (alias) | DESIGN TOKENS (semantici) | TEMPLATE / LIBRERIA |
| --- | --- | --- |
| `alias_colors = {`<br>`  "blue-10": "#E6F2FF",`<br>`  "blue-20": "#CCE6FF",`<br>`  "blue-30": "#99CCFF",`<br>`  … }` | `tokens = {`<br>`  "color-accent-1": alias_colors["blue-60"],`<br>`  "color-accent-2": alias_colors["teal-50"],`<br>`  "color-text": alias_colors["gray-90"],`<br>`  … }` | `altair_theme = {`<br>`  "config": { … }`<br>`}`<br><br>`matplotlib_style = {`<br>`  "axes.facecolor": tokens["color-background"],`<br>`  "text.color": tokens["color-text"],`<br>`  … }` |
```

## Eseguire gli esempi

Gli esempi si trovano in `examples/` e generano alcuni file di output in `examples/outputs/`:

- `mpl_test.png`: semplice grafico Matplotlib con il tema applicato
- `altair_test.html`: grafico Altair esportato come HTML (usa un dataset di fallback se `vega_datasets` non è installato)

Per eseguire rapidamente lo script di check dell'ambiente (`examples/check_env.py`), scegli una delle opzioni qui sotto (zsh su macOS):

1) Esecuzione come modulo (consigliata)

```zsh
python -m examples.check_env
```

2) Impostare il PYTHONPATH al volo

```zsh
PYTHONPATH=. python examples/check_env.py
```

3) Installare il progetto in modalità editable (sviluppo)

```zsh
python -m pip install -e .
python examples/check_env.py
```

Dipendenze: per usare il dataset di esempio di Altair (`vega_datasets`) installa i requirements:

```zsh
python -m pip install -r requirements.txt
```

## Uso rapido dei temi in uno script

Matplotlib

```python
from builders.matplotlib_builder import apply_mpl_theme
import matplotlib.pyplot as plt

apply_mpl_theme()  # applica lo stile
plt.plot([1, 2, 3], [3, 5, 2])
plt.title("Esempio Matplotlib")
plt.show()
```

Altair

```python
import altair as alt
# Importa il tema per registrarlo (e abilitarlo automaticamente)
from themes.altair_mobility_theme import mobility_theme  # noqa: F401

chart = alt.Chart(alt.Data(values=[{"x": "A", "y": 1}, {"x": "B", "y": 2}])) \
	.mark_bar() \
	.encode(x="x:N", y="y:Q")

# HTML
chart.save("chart.html")

# PNG (richiede una dipendenza opzionale)
# Opzione consigliata: installa 'vl-convert-python' (in requirements.txt)
# Altro fallback: 'altair_saver' con un backend disponibile (selenium o node)
chart.save("chart.png")
```

Se l'esportazione PNG fallisce, installa una delle dipendenze opzionali:

```zsh
# consigliato
python -m pip install vl-convert-python

# alternativa
python -m pip install altair_saver
```
