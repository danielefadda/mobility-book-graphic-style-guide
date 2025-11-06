from pathlib import Path
import sys

# 1) Verifica import e font Inter
import matplotlib as mpl
import matplotlib.pyplot as plt
import altair as alt
from vega_datasets import data
import pandas as pd

# Assicura che la root del repo sia nel PYTHONPATH (quando esegui da examples/)
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import dei tuoi moduli (devono esistere nel progetto)
from themes.altair_mobility_theme import mobility_theme  # registra/abilita il tema
from builders.matplotlib_builder import apply_mpl_theme
from design_tokens.design_tokens import TOKENS

# Cartella output
OUT = Path(__file__).parent / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

# 2) Applica tema Matplotlib
apply_mpl_theme()

# 3) Test Matplotlib (line plot)
plt.figure()
plt.plot([1, 2, 3, 4], [3, 5, 2, 6], label="Serie A")
plt.title("Matplotlib — test Inter + palette")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True, axis="y")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "mpl_test.png", dpi=144)
plt.close()

# 4) Test Altair (bar chart)
# Prova a usare vega_datasets; se non disponibile, usa un dataset minimo di fallback
try:
    import importlib
    data = importlib.import_module("vega_datasets.data")
    cars = data.cars()
except Exception:
    cars = pd.DataFrame(
        {
            "Name": ["Car A", "Car B", "Car C", "Car D", "Car E"],
            "Horsepower": [110, 95, 130, 120, 105],
            "Origin": ["USA", "Europe", "Japan", "USA", "Europe"],
        }
    )

chart = (
    alt.Chart(cars.head(15))
    .mark_bar()
    .encode(x="Name:N", y="Horsepower:Q", color=alt.Color("Origin:N", legend=None))
    .properties(title="Altair — test Inter + palette", width=600, height=300)
)
chart.save(OUT / "altair_test.html")

# 4b) Esporta anche in PNG se possibile
png_path = OUT / "altair_test.png"
png_saved = False
try:
    # Metodo preferito (usa vl-convert se disponibile)
    chart.save(png_path)
    png_saved = True
except Exception as e:
    # Fallback: prova altair_saver se installato
    try:
        import importlib
        altair_saver = importlib.import_module("altair_saver")
        altair_saver.save(chart, png_path)
        png_saved = True
    except Exception as e2:
        print(
            "[INFO] Impossibile esportare PNG automaticamente."
            " Installa una di queste dipendenze e riprova:"
            " 'vl-convert-python' (consigliato) oppure 'altair_saver'"
            " con un backend disponibile (es. selenium o node)."
        )

# 5) Stampa font in uso (utile per verificare Inter)
print("Matplotlib font family:", mpl.rcParams.get("font.sans-serif"))
print("Text color:", TOKENS["color"]["text"])
print("Output salvati in:", OUT.resolve())
if png_saved:
    print("PNG Altair salvato in:", png_path.resolve())
else:
    print("PNG Altair non generato (dipendenze opzionali mancanti)")
