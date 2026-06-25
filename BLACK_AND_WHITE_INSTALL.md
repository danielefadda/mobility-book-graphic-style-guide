# Mobility Book Style Guide - Branch Black and White

Questa guida spiega come installare e usare la versione **bianco e nero** della libreria, basata sul branch `black-and-white`.

## 1. Installazione da GitHub (consigliata)

Se vuoi usare direttamente il branch remoto:

```bash
pip install "git+https://github.com/danielefadda/mobility-book-graphic-style-guide.git@black-and-white"
```

Con extra opzionali:

```bash
pip install "git+https://github.com/danielefadda/mobility-book-graphic-style-guide.git@black-and-white#egg=mobility-book-style[all]"
```

## 2. Installazione locale in editable mode (sviluppo)

```bash
git clone https://github.com/danielefadda/mobility-book-graphic-style-guide.git
cd mobility-book-graphic-style-guide
git checkout black-and-white
pip install -e .
```

Con dipendenze complete:

```bash
pip install -e ".[all]"
```

## 3. Uso rapido - Matplotlib (bianco e nero)

```python
import mobility_book_style as mbs
import matplotlib.pyplot as plt

mbs.apply_matplotlib_theme()

fig, ax = plt.subplots()
ax.bar(["A", "B", "C"], [10, 7, 12])
ax.set_title("Esempio B/N")
plt.show()
```

## 4. Uso rapido - Altair (bianco e nero)

```python
import mobility_book_style as mbs
import altair as alt
import pandas as pd

mbs.enable_altair_theme()

df = pd.DataFrame({"x": ["A", "B", "C"], "y": [10, 7, 12]})

chart = alt.Chart(df).mark_bar().encode(
    x="x:N",
    y="y:Q"
).properties(title="Esempio B/N")

chart
```

## 5. Verifica veloce dei token B/N

```python
import mobility_book_style as mbs

print(mbs.token.color.brand.primary)
print(mbs.token.color.chart.categorical["1"])
print(mbs.token.color.chart.categorical["7"])
```

Nel branch `black-and-white`, tutti i token colore sono convertiti in scala di grigi (dal nero al bianco), mantenendo invariata l'API della libreria.
