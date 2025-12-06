"""
Altair theme per Mobility Book.

Questo modulo fornisce funzioni per applicare il tema standardizzato
di Mobility Book alle visualizzazioni Altair.

Esempio:
    >>> import mobility_book_style as mbs
    >>> import altair as alt
    >>> 
    >>> mbs.enable_altair_theme()
    >>> chart = alt.Chart(data).mark_bar().encode(x='x:N', y='y:Q')
    >>> chart.save("output.html")

Note:
    Lo stile applicato è immutabile e non può essere modificato dall'utente
    per garantire coerenza visiva in tutte le pubblicazioni Mobility Book.
    
    Altair è una dipendenza opzionale. Installala con:
    pip install mobility-book-style[altair]
"""

try:
    import altair as alt

    ALTAIR_AVAILABLE = True
except ImportError:
    ALTAIR_AVAILABLE = False
    alt = None

from ._tokens import TOKENS


def _build_altair_theme():
    """
    Costruisce la configurazione del tema Altair dai design tokens.
    
    Returns:
        dict: Configurazione tema Altair completa
    
    Note:
        Questa funzione è interna e non dovrebbe essere chiamata direttamente.
        Usa enable_altair_theme() invece.
    """
    return {
        "config": {
            "background": TOKENS["color"]["background"],
            "font": TOKENS["font"]["base_stack"],
            "mark": {"color": TOKENS["color"]["accent"]},
            "title": {
                "color": TOKENS["color"]["text"],
                "anchor": "start",
                "dy": -15,
                "fontSize": TOKENS["chart"]["title_size_px"],
                "font": TOKENS["font"]["base_stack"],
                "fontWeight": TOKENS["font"]["weight_bold"],
            },
            "axis": {
                "labelColor": TOKENS["color"]["text"],
                "labelFontSize": TOKENS["chart"]["tick_size_px"],
                "labelFont": TOKENS["font"]["base_stack"],
                "labelFontWeight": TOKENS["font"]["weight_regular"],
                "titleColor": TOKENS["color"]["text"],
                "titleFontSize": TOKENS["chart"]["label_size_px"],
                "titleFont": TOKENS["font"]["base_stack"],
                "titleFontWeight": TOKENS["font"]["weight_bold"],
                "grid": True,
                "gridColor": TOKENS["chart"]["grid_color"],
                "labelAngle": 0,
                "domainWidth": 0.5,
                "labelPadding": 2,
                "tickSize": 5,
                "tickWidth": 0.5,
            },
            "axisX": {
                "gridDash": [6, 3],
                "gridWidth": 0.25,
                "gridColor": TOKENS["color"]["grid"],
            },
            "axisY": {
                "gridDash": [6, 3],
                "gridWidth": 0.25,
                "gridColor": TOKENS["color"]["grid"],
            },
            "legend": {
                "labelFontSize": TOKENS["chart"]["legend_size_px"],
                "padding": 1,
                "symbolType": "square",
                "labelFont": TOKENS["font"]["base_stack"],
                "titleFont": TOKENS["font"]["base_stack"],
            },
            "style": {
                "guide-label": {
                    "font": TOKENS["font"]["base_stack"],
                    "fill": TOKENS["color"]["text"],
                },
                "guide-title": {
                    "font": TOKENS["font"]["base_stack"],
                    "fill": TOKENS["color"]["text"],
                },
            },
            "range": {"category": TOKENS["chart"]["category10"]},
            "point": {"filled": True},
            "line": {"strokeWidth": TOKENS["chart"]["line_width"]},
            "view": {"stroke": "transparent"},
        }
    }


def enable_altair_theme():
    """
    Abilita il tema Altair di Mobility Book.
    
    Questa funzione registra e attiva il tema personalizzato per Altair.
    Tutti i grafici creati dopo questa chiamata utilizzeranno automaticamente
    lo stile Mobility Book.
    
    Esempio:
        >>> import mobility_book_style as mbs
        >>> import altair as alt
        >>> import pandas as pd
        >>> 
        >>> mbs.enable_altair_theme()
        >>> 
        >>> data = pd.DataFrame({'x': ['A', 'B', 'C'], 'y': [10, 20, 15]})
        >>> chart = alt.Chart(data).mark_bar().encode(
        ...     x='x:N',
        ...     y='y:Q'
        ... ).properties(title='Grafico Mobility Book')
        >>> 
        >>> chart.save('output.html')
    
    Raises:
        ImportError: Se Altair non è installato
    
    Note:
        Il tema rimane attivo per tutta la sessione fino a quando non viene
        chiamato disable_altair_theme() o alt.themes.enable('default').
        
        Per installare Altair:
        pip install mobility-book-style[altair]
    """
    if not ALTAIR_AVAILABLE:
        raise ImportError(
            "Altair non è installato. "
            "Installalo con: pip install mobility-book-style[altair]"
        )

    alt.themes.register("mobility_theme", _build_altair_theme)
    alt.themes.enable("mobility_theme")


def disable_altair_theme():
    """
    Disabilita il tema Altair di Mobility Book e ripristina il tema default.
    
    Esempio:
        >>> import mobility_book_style as mbs
        >>> 
        >>> mbs.enable_altair_theme()
        >>> # ... crea grafici con stile Mobility Book
        >>> 
        >>> mbs.disable_altair_theme()
        >>> # ... torna allo stile default di Altair
    
    Note:
        Questa funzione è utile se vuoi creare alcuni grafici con lo stile
        Mobility Book e altri con lo stile default di Altair nella stessa sessione.
    """
    if ALTAIR_AVAILABLE:
        alt.themes.enable("default")
