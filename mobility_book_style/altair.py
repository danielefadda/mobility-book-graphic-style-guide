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

from ._tokens import token


def _palette_from_numeric_keys(mapping: dict) -> list:
    try:
        return [mapping[k] for k in sorted(mapping, key=lambda v: int(v))]
    except Exception:
        return list(mapping.values())


def _num(value: str | float | int) -> float:
    if isinstance(value, (float, int)):
        return float(value)
    cleaned = value.replace("pt", "").replace("px", "")
    return float(cleaned)


def _build_altair_theme():
    """
    Costruisce la configurazione del tema Altair dai design tokens.
    
    Returns:
        dict: Configurazione tema Altair completa
    
    Note:
        Questa funzione è interna e non dovrebbe essere chiamata direttamente.
        Usa enable_altair_theme() invece.
    """
    palette = _palette_from_numeric_keys(token.color.chart.categorical)

    return {
        "config": {
            "background": token.color.background.default,
            "font": token.font.family.sans,
            "mark": {"color": token.color.brand.accent},
            "title": {
                "color": token.chart.typography.title.color,
                "anchor": "start",
                "dy": -15,
                "fontSize": _num(token.chart.typography.title.fontSize),
                "font": token.font.family.sans,
                "fontWeight": token.chart.typography.title.fontWeight,
            },
            "axis": {
                "labelColor": token.chart.typography.label.color,
                "labelFontSize": _num(token.chart.typography.label.fontSize),
                "labelFont": token.font.family.sans,
                "labelFontWeight": token.chart.typography.label.fontWeight,
                "titleColor": token.chart.typography.label.color,
                "titleFontSize": _num(token.chart.typography.label.fontSize),
                "titleFont": token.font.family.sans,
                "titleFontWeight": token.chart.typography.title.fontWeight,
                "grid": True,
                "gridColor": token.chart.element.grid.color,
                "labelAngle": 0,
                "domainWidth": _num(token.chart.element.axis.width),
                "labelPadding": 2,
                "tickSize": _num(token.chart.element.tick.length),
                "tickWidth": _num(token.chart.element.tick.width),
            },
            "axisX": {
                "gridDash": [_num(v) for v in token.chart.element.grid.dash.split()],
                "gridWidth": _num(token.chart.element.grid.width) / 2,
                "gridColor": token.chart.element.grid.color,
            },
            "axisY": {
                "gridDash": [_num(v) for v in token.chart.element.grid.dash.split()],
                "gridWidth": _num(token.chart.element.grid.width) / 2,
                "gridColor": token.chart.element.grid.color,
            },
            "legend": {
                "labelFontSize": _num(token.chart.typography.annotation.fontSize),
                "padding": 1,
                "symbolType": "square",
                "labelFont": token.font.family.sans,
                "titleFont": token.font.family.sans,
            },
            "style": {
                "guide-label": {
                    "font": token.font.family.sans,
                    "fill": token.chart.typography.label.color,
                },
                "guide-title": {
                    "font": token.font.family.sans,
                    "fill": token.chart.typography.label.color,
                },
            },
            "range": {"category": palette},
            "point": {"filled": True},
            "line": {"strokeWidth": _num(token.chart.element.axis.width) * 2},
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
