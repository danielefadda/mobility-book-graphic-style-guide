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

from pathlib import Path
import base64

try:
    import altair as alt

    ALTAIR_AVAILABLE = True
except ImportError:
    ALTAIR_AVAILABLE = False
    alt = None

from ._tokens import token
from .utils import to_px, palette_from_numeric_keys


# Esponi le scale personalizzate a livello di modulo
_sequential_scales = {}
_FONTS_DIR = Path(__file__).parent / "fonts"


def _encode_font_as_data_uri(font_path: Path) -> str:
    raw = font_path.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:font/ttf;base64,{b64}"


def get_altair_font_css() -> str:
    """Restituisce il CSS @font-face per Inter 18pt (regular/italic/bold/bold italic).

    Il CSS usa data URI per incorporare i TTF direttamente nell'HTML esportato.
    """

    faces = [
        ("Inter 18pt", "normal", "400", "Inter_18pt-Regular.ttf"),
        ("Inter 18pt", "italic", "400", "Inter_18pt-Italic.ttf"),
        ("Inter 18pt", "normal", "700", "Inter_18pt-Bold.ttf"),
        ("Inter 18pt", "italic", "700", "Inter_18pt-BoldItalic.ttf"),
    ]

    blocks: list[str] = []
    for family, style, weight, filename in faces:
        font_path = _FONTS_DIR / filename
        if not font_path.exists():
            continue
        data_uri = _encode_font_as_data_uri(font_path)
        blocks.append(
            "@font-face {"
            f" font-family: '{family}';"
            f" font-style: {style};"
            f" font-weight: {weight};"
            f" src: url({data_uri}) format('truetype');"
            " }"
        )

    return "\n".join(blocks)


def altair_embed_options_with_inter() -> dict:
    """Restituisce le embed options Altair con Inter 18pt incorporato via CSS.

    Usa in chart.save(..., embed_options=altair_embed_options_with_inter()).
    """

    css = get_altair_font_css()
    return {"defaultStyle": css} if css else {}


def _build_altair_theme():
    """
    Costruisce la configurazione del tema Altair dai design tokens.
    
    Returns:
        dict: Configurazione tema Altair completa
    
    Note:
        Questa funzione è interna e non dovrebbe essere chiamata direttamente.
        Usa enable_altair_theme() invece.
        
        Altair/Vega-Lite usa pixel CSS, quindi tutti i valori in pt dai token
        vengono convertiti in px usando to_px().
    """
    categorical = palette_from_numeric_keys(token.color.chart.categorical)
    divergent = palette_from_numeric_keys(token.color.chart.divergent)
    
    # Scale sequenziali personalizzate
    global _sequential_scales
    _sequential_scales = {
        "teal": palette_from_numeric_keys(token.color.chart.sequential.teal),
        "burgundy": palette_from_numeric_keys(token.color.chart.sequential.burgundy),
        "neutral": palette_from_numeric_keys(token.color.chart.sequential.neutral),
        "purple": palette_from_numeric_keys(token.color.chart.sequential.purple),
        "olive": palette_from_numeric_keys(token.color.chart.sequential.olive),
        "gold": palette_from_numeric_keys(token.color.chart.sequential.gold),
        "rust": palette_from_numeric_keys(token.color.chart.sequential.rust),
    }

    return {
        "config": {
            "background": token.color.background.default,
            "font": token.font.family.sans,
            "mark": {"color": token.color.brand.primary},
            "rect": {
                "stroke": token.cartography.heatmap.cell.stroke,
                "strokeWidth": to_px(token.cartography.heatmap.cell.strokeWidth),
                "cornerRadius": to_px(token.cartography.heatmap.cell.cornerRadius),
            },
            "title": {
                "color": token.chart.typography.title.color,
                "anchor": "start",
                "dy": -15,
                "fontSize": to_px(token.chart.typography.title.fontSize),
                "font": token.chart.typography.title.fontFamily,
                "fontWeight": token.chart.typography.title.fontWeight,
                "frame": "group",
            },
            "axis": {
                "labelColor": token.chart.typography.label.color,
                "labelFontSize": to_px(token.chart.typography.label.fontSize),
                "labelFont": token.chart.typography.label.fontFamily,
                "labelFontWeight": token.chart.typography.label.fontWeight,
                "titleColor": token.chart.typography.label.color,
                "titleFontSize": to_px(token.chart.typography.label.fontSize),
                "titleFont": token.chart.typography.label.fontFamily,
                "titleFontWeight": token.chart.typography.label.fontWeight,
                "grid": True,
                "gridColor": token.chart.element.grid.color,
                "labelAngle": 0,
                "domainWidth": to_px(token.chart.element.axis.x.width),
                "labelPadding": 2,
                "tickWidth": to_px(token.chart.element.tick.width),
            },
            "axisX": {
                "grid": False,
                "ticks": True,
                "tickSize": to_px(token.chart.element.tick.x.length),
                "tickWidth": to_px(token.chart.element.tick.x.width),
                "tickColor": token.chart.element.tick.x.color,
                "domainWidth": to_px(token.chart.element.axis.x.width),
            },
            "axisY": {
                "grid": True,
                "gridWidth": to_px(token.chart.element.grid.width),
                "gridColor": token.chart.element.grid.color,
                "ticks": False,
                "tickSize": 0,
                "domain": False,
            },
            "legend": {
                "labelFontSize": to_px(token.chart.typography.annotation.fontSize),
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
            "range": {
                "category": categorical,
                "diverging": divergent,
                "ordinal": _sequential_scales["teal"],
                "ramp": _sequential_scales["teal"],
                "heatmap": _sequential_scales["teal"],
                # Named scales for explicit use
                "teal": _sequential_scales["teal"],
                "burgundy": _sequential_scales["burgundy"],
                "neutral": _sequential_scales["neutral"],
                "purple": _sequential_scales["purple"],
                "olive": _sequential_scales["olive"],
                "gold": _sequential_scales["gold"],
                "rust": _sequential_scales["rust"],
            },
            "point": {
                "filled": True,
                "size": (to_px(token.chart.data.line.markerSize)*1.3) ** 2,  # Altair usa area, non raggio
            },
            "line": {
                "strokeWidth": to_px(token.chart.data.line.width),
                "strokeCap": token.chart.data.line.capStyle,
                "strokeJoin": token.chart.data.line.joinStyle,
            },
            "view": {
                "stroke": "transparent",
                # Dimensioni di default per view in px, usando i token
                # continuous* per assi quantitativi/continui, discrete* per assi categorici
                "continuousWidth": to_px(token.component.figure.default.width),
                "continuousHeight": to_px(token.component.figure.default.height),
                "discreteWidth": to_px(token.component.figure.default.width),
                "discreteHeight": to_px(token.component.figure.default.height),
                },
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
    
    @alt.theme.register("mobility_theme", enable=True)
    def custom_theme():
        return _build_altair_theme()

    # Imposta embed options di default con font Inter 18pt incorporato via @font-face.
    # In questo modo i grafici inline e gli export HTML includono il font senza
    # codice aggiuntivo nel notebook.
    try:
        css_opts = altair_embed_options_with_inter()
        if css_opts:
            alt.renderers.set_embed_options(**css_opts)
    except Exception:
        # Non bloccare l'attivazione del tema se l'embed option fallisce
        pass


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
        alt.theme.enable("default")


def get_color_scale(scale_name: str) -> list:
    """
    Ottiene una scala di colori personalizzata dal tema Mobility Book.
    
    Args:
        scale_name: Nome della scala ('teal', 'burgundy', 'neutral', 'purple', 
                   'olive', 'gold', 'rust', 'categorical', 'divergent')
    
    Returns:
        Lista di colori hex per la scala richiesta
        
    Raises:
        ValueError: Se il nome della scala non è valido
        
    Esempio:
        >>> import mobility_book_style as mbs
        >>> import altair as alt
        >>> 
        >>> mbs.enable_altair_theme()
        >>> rust_colors = mbs.get_color_scale('rust')
        >>> 
        >>> # Usa nella chart
        >>> chart = alt.Chart(data).mark_rect().encode(
        ...     color=alt.Color('value:Q', scale=alt.Scale(range=rust_colors))
        ... )
    
    Note:
        È necessario aver chiamato enable_altair_theme() prima di usare questa funzione.
    """
    valid_scales = list(_sequential_scales.keys()) + ['categorical', 'divergent']
    
    if scale_name not in valid_scales:
        raise ValueError(
            f"Scale '{scale_name}' non valida. "
            f"Scegli tra: {', '.join(valid_scales)}"
        )
    
    if scale_name == 'categorical':
        return palette_from_numeric_keys(token.color.chart.categorical)
    elif scale_name == 'divergent':
        return palette_from_numeric_keys(token.color.chart.divergent)
    else:
        return _sequential_scales.get(scale_name, [])


def get_heatmap_axis_config() -> dict:
    """
    Restituisce una configurazione axis (x, y) per heatmap basata sui design tokens.

    Returns:
        dict: Dizionario con chiavi 'x', 'y' (Axis config) e 'legend_orient'.

    Esempio:
        >>> cfg = mbs.get_heatmap_axis_config()
        >>> heatmap = alt.Chart(df).mark_rect().encode(
        ...   x=alt.X('X:O', axis=alt.Axis(**cfg['x'])),
        ...   y=alt.Y('Y:O', axis=alt.Axis(**cfg['y']))
        ... ).configure_legend(orient=cfg['legend_orient'])
    """
    def _to_bool(val):
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.strip().lower() in {"true", "1", "yes", "y"}
        return bool(val)

    grid = _to_bool(token.chart.heatmap.grid)
    
    x = {
        "labelAngle": int(token.chart.heatmap.axis.x.labelAngle),
        "ticks": _to_bool(token.chart.heatmap.axis.x.ticks),
        "domain": _to_bool(token.chart.heatmap.axis.x.domain),
        "labelFontSize": to_px(token.chart.heatmap.axis.x.labelFontSize),
        "grid": grid,
    }
    y = {
        "ticks": _to_bool(token.chart.heatmap.axis.y.ticks),
        "domain": _to_bool(token.chart.heatmap.axis.y.domain),
        "labelFontSize": to_px(token.chart.heatmap.axis.y.labelFontSize),
        "grid": grid,
    }
    legend_orient = token.chart.heatmap.legend.orient
    return {"x": x, "y": y, "legend_orient": legend_orient}
