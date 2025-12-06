"""
Matplotlib theme per Mobility Book.

Questo modulo fornisce funzioni per applicare il tema standardizzato
di Mobility Book alle visualizzazioni Matplotlib.

Esempio:
    >>> import mobility_book_style as mbs
    >>> import matplotlib.pyplot as plt
    >>> 
    >>> mbs.apply_matplotlib_theme()
    >>> plt.plot([1, 2, 3], [4, 5, 6])
    >>> plt.title("Grafico con stile Mobility Book")
    >>> plt.show()

Note:
    Lo stile applicato è immutabile e non può essere modificato dall'utente
    per garantire coerenza visiva in tutte le pubblicazioni Mobility Book.
"""

import matplotlib as mpl
from ._tokens import TOKENS, TOKENS_PT


def apply_matplotlib_theme():
    """
    Applica il tema Matplotlib di Mobility Book.
    
    Questa funzione configura tutti i parametri rcParams di Matplotlib
    per utilizzare i colori, font e stili definiti nei design tokens.
    
    Lo stile include:
    - Font Inter (con fallback)
    - Palette colori category10 personalizzata
    - Griglie e assi stilizzati
    - Dimensioni e pesi dei testi ottimizzati
    
    Esempio:
        >>> import mobility_book_style as mbs
        >>> import matplotlib.pyplot as plt
        >>> 
        >>> mbs.apply_matplotlib_theme()
        >>> fig, ax = plt.subplots()
        >>> ax.plot([1, 2, 3, 4], [3, 5, 2, 6], label='Serie A')
        >>> ax.set_title('Grafico Mobility Book')
        >>> ax.set_xlabel('X')
        >>> ax.set_ylabel('Y')
        >>> ax.legend()
        >>> plt.show()
    
    Note:
        Questa funzione modifica i parametri globali di Matplotlib (rcParams).
        L'effetto persiste per tutta la sessione fino a quando non viene
        chiamato plt.style.use() o modificato manualmente rcParams.
    """
    import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

    # 1. FUNZIONI DI UTILITÀ
    # ---------------------------------------------------------
def px_to_pt(px):
    """Converte pixel in punti tipografici (1 px = 0.75 pt standard)"""
    return px * 0.50

# Funzione dummy per simulare la risoluzione dei colori alias nel JSON.
# Sostituisci questa logica con il tuo vero resolver di token se i valori sono ancora stringhe "{alias...}"
def get_color(path):
    # ESEMPIO: Se path è "text", cerca in TOKENS["color"]["text"]
    # Qui dovresti restituire il codice HEX reale (es. #333333). 
    # Per ora restituisco direttamente il valore assumendo che sia stato risolto.
    val = path
    return val 

# 2. PREPARAZIONE DATI
# ---------------------------------------------------------
# Estraiamo la lista dei font pulita
font_stack = [f.strip() for f in TOKENS["font"]["base_stack"].split(',')]

# Risolviamo la palette categoriale (Chart Colors)
cat10_palette = [c for c in TOKENS["chart"]["category10"]]

# 3. CONFIGURAZIONE RCPARAMS
# ---------------------------------------------------------
mpl.rcParams.update({
    # --- DIMENSIONI & RISOLUZIONE ---
    'figure.figsize': [6, 3],     # Standard 6x3 pollici
    'figure.dpi': 150,            # Alta risoluzione per schermi
    
    # --- COLORI DI SFONDO ---
    "figure.facecolor": TOKENS["color"]["background"],
    "axes.facecolor": TOKENS["color"]["background"],
    "savefig.facecolor": TOKENS["color"]["background"],
    
    # --- FONT & TESTO ---
    "font.family": "sans-serif",
    # Matplotlib prova i font in ordine finché non ne trova uno installato
    "font.sans-serif": font_stack,
    "text.color": TOKENS["color"]["text"],
    
    # --- TITOLI (Chart Title) ---
    # Altair "title" -> Matplotlib "axes.title"
    "axes.titlesize": px_to_pt(TOKENS["chart"]["title_size_px"]),
    "axes.titleweight": TOKENS["font"]["weight_bold"], # Accetta 600
    "axes.titlelocation": "left",
    "axes.titlepad": 10,  # Sposta il titolo più vicino all'asse
    "axes.titlecolor": TOKENS["color"]["text"],

    # --- ETICHETTE ASSI (Axis Labels es. "Tempo") ---
    "axes.labelsize": px_to_pt(TOKENS["chart"]["label_size_px"]),
    "axes.labelweight": TOKENS["font"]["weight_regular"], # Accetta 400
    "axes.labelcolor": TOKENS["color"]["text"],
    "axes.labelpad": 8,

    # --- TICKS (Numeri sugli assi es. "10, 20") ---
    "xtick.labelsize": px_to_pt(TOKENS["chart"]["tick_size_px"]),
    "ytick.labelsize": px_to_pt(TOKENS["chart"]["tick_size_px"]),
    "xtick.color": TOKENS["chart"]["tick_color"],
    "ytick.color": TOKENS["chart"]["tick_color"],
    # Dimensioni tacche (ticks)
    "xtick.major.size": 4, 
    "ytick.major.size": 4,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    
    # --- ASSI (Spines / Domain) ---
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": True,
    "axes.spines.bottom": True,
    "axes.linewidth": 0.5,
    "axes.edgecolor": TOKENS["chart"]["axis_color"], # Colore linea assi

    # --- GRIGLIA ---
    "axes.grid": True,
    "axes.axisbelow": True,       # Griglia sotto i dati
    "grid.color": TOKENS["chart"]["grid_color"],
    "grid.linewidth": 0.5,        # 0.25px potrebbe essere troppo sottile in stampa
    "grid.linestyle": (0, (6, 3)), # Replica il dash [6, 3] di Altair
    "grid.alpha": 1.0,

    # --- LINEE E COLORI ---
    "lines.linewidth": px_to_pt(TOKENS["chart"]["line_width"]),
    "lines.solid_capstyle": "round",
    # Applica la palette category10 automaticamente ai grafici multi-linea
    "axes.prop_cycle": cycler(color=cat10_palette),

    # --- MARKER ---
    "lines.markersize": TOKENS["chart"]["line_width"] * 1.5,
    "lines.marker": TOKENS["chart"]["lines_marker"],

    # --- LEGENDA ---
    "legend.fontsize": px_to_pt(TOKENS["chart"]["legend_size_px"]),
    "legend.title_fontsize": px_to_pt(TOKENS["chart"]["legend_size_px"]),
    "legend.frameon": False,      # Niente box attorno alla legenda
    "legend.loc": "upper right"
})

def style_table(table, *, body_face=None, header_face=None):
    """
    Applica lo stile Mobility Book a una tabella Matplotlib.
    
    Questa utility stilizza le tabelle create con matplotlib.table.Table
    applicando colori, font e formattazione coerenti con il design system.
    
    Args:
        table: Oggetto Table ritornato da plt.table(...) o ax.table(...)
        body_face: Colore di sfondo per le celle del corpo (default: bianco)
        header_face: Colore di sfondo per le celle header (default: gray-10)
    
    Esempio:
        >>> import matplotlib.pyplot as plt
        >>> import mobility_book_style as mbs
        >>> 
        >>> mbs.apply_matplotlib_theme()
        >>> 
        >>> fig, ax = plt.subplots()
        >>> ax.axis('off')
        >>> 
        >>> data = [['Nome', 'Valore'], ['Item A', '100'], ['Item B', '200']]
        >>> table = ax.table(cellText=data, loc='center', cellLoc='left')
        >>> mbs.style_table(table)
        >>> plt.show()
    
    Note:
        La prima riga (row == 0) viene trattata come header.
        Il font utilizzato è Inter, coerente con il resto del design system.
    """
    body_face = body_face or "white"
    header_face = header_face or TOKENS["color"]["cell_shade"]

    for (row, col), cell in table.get_celld().items():
        # header: row == 0
        if row == 0:
            cell.set_facecolor(header_face)
            cell.set_edgecolor(TOKENS["table"]["body_border"])
            cell.set_linewidth(0.8)
            cell.get_text().set_fontsize(TOKENS_PT["table"]["header_pt"])
            cell.get_text().set_fontfamily("Inter")
            cell.get_text().set_fontweight(TOKENS["font"]["weight_bold"])
            cell.get_text().set_color(TOKENS["color"]["text"])
        else:
            cell.set_facecolor(body_face)
            cell.set_edgecolor(TOKENS["table"]["body_border"])
            cell.set_linewidth(0.5)
            cell.get_text().set_fontsize(TOKENS_PT["table"]["body_pt"])
            cell.get_text().set_fontfamily("Inter")
            cell.get_text().set_color(TOKENS["color"]["text"])
