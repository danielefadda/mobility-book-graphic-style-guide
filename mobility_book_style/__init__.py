"""
Mobility Book Graphic Style Guide
==================================

Una libreria per applicare lo stile grafico standardizzato di Mobility Book
alle visualizzazioni Matplotlib e Altair.

Uso base:

Matplotlib
----------
>>> import mobility_book_style as mbs
>>> import matplotlib.pyplot as plt
>>> 
>>> mbs.apply_matplotlib_theme()
>>> plt.plot([1, 2, 3], [4, 5, 6])
>>> plt.title("Grafico con stile Mobility Book")
>>> plt.show()

Altair
------
>>> import mobility_book_style as mbs
>>> import altair as alt
>>> 
>>> mbs.enable_altair_theme()
>>> chart = alt.Chart(data).mark_bar().encode(x='x:N', y='y:Q')
>>> chart.save("output.html")

Note:
    Lo stile definito in questa libreria NON è modificabile dall'utente.
    I design tokens e i colori sono immutabili per garantire coerenza visiva.
    
    I font Inter sono registrati automaticamente all'import del pacchetto.
"""

__version__ = "0.1.0"
__author__ = "Daniele Fadda"

# API pubblica principale
from ._tokens import token
from .matplotlib import apply_matplotlib_theme, style_table
from .altair import enable_altair_theme, disable_altair_theme
from .export import export_ase, export_colors_dict

__all__ = [
    "token",
    "apply_matplotlib_theme",
    "style_table",
    "enable_altair_theme",
    "disable_altair_theme",
    "export_ase",
    "export_colors_dict",
]
