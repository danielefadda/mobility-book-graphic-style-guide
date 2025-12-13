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
from .export import export_ase, export_colors_dict
from . import theme

# Nota: avvolgiamo le funzioni Altair in semplici wrapper per ricaricare
# il modulo altair interno prima di abilitarne il tema. In questo modo
# l'utente non deve più chiamare esplicitamente `importlib.reload(mbs.altair)`.
from . import altair as _altair  # type: ignore


def enable_altair_theme(auto_reload: bool = True):
    """Abilita il tema Altair, ricaricando il modulo se richiesto.

    Args:
        auto_reload: se True (default) ricarica `mobility_book_style.altair`
            prima di attivare il tema, così si ottiene sempre l'ultima patch
            senza dover chiamare manualmente ``importlib.reload`` nel notebook.
    """

    if auto_reload:
        import importlib

        importlib.reload(_altair)
    return _altair.enable_altair_theme()


def disable_altair_theme():
    return _altair.disable_altair_theme()


def get_color_scale(scale_name: str) -> list:
    return _altair.get_color_scale(scale_name)


def get_heatmap_axis_config() -> dict:
    return _altair.get_heatmap_axis_config()


def get_altair_font_css() -> str:
    return _altair.get_altair_font_css()


def altair_embed_options_with_inter() -> dict:
    return _altair.altair_embed_options_with_inter()

__all__ = [
    "token",
    "theme",
    "apply_matplotlib_theme",
    "style_table",
    "enable_altair_theme",
    "disable_altair_theme",
    "get_color_scale",
    "get_heatmap_axis_config",
    "get_altair_font_css",
    "altair_embed_options_with_inter",
    "export_ase",
    "export_colors_dict",
]
