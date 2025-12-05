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
    mpl.rcParams.update(
        {
            # Colori di sfondo
            "figure.facecolor": TOKENS["color"]["background"],
            "axes.facecolor": TOKENS["color"]["background"],
            "savefig.facecolor": TOKENS["color"]["background"],
            "savefig.edgecolor": TOKENS["color"]["background"],
            
            # Font
            "font.family": "sans-serif",
            "font.sans-serif": [f.strip() for f in TOKENS["font"]["base_stack"].split(",")],
            
            # Titoli e etichette
            "axes.titlesize": TOKENS_PT["chart"]["title_pt"],
            "axes.titleweight": TOKENS["font"]["weight_bold"],
            "axes.labelsize": TOKENS_PT["chart"]["label_pt"],
            "axes.labelweight": TOKENS["font"]["weight_regular"],
            "axes.labelcolor": TOKENS["color"]["text"],
            
            # Ticks
            "xtick.labelsize": TOKENS_PT["chart"]["tick_pt"],
            "ytick.labelsize": TOKENS_PT["chart"]["tick_pt"],
            "xtick.color": TOKENS["color"]["text"],
            "ytick.color": TOKENS["color"]["text"],
            "xtick.major.width": 0.5,
            "ytick.major.width": 0.5,
            "xtick.major.size": 5,
            "ytick.major.size": 5,
            
            # Assi
            "axes.edgecolor": TOKENS["color"]["domain"],
            "axes.linewidth": 0.5,
            "axes.grid": True,
            "axes.grid.axis": "y",
            
            # Griglia
            "grid.color": TOKENS["color"]["grid"],
            "grid.linestyle": "--",
            "grid.linewidth": 0.25,
            "grid.alpha": 1.0,
            "axes.axisbelow": True,  # Griglia dietro i dati
            
            # Spines (bordi)
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": True,
            "axes.spines.bottom": True,
            
            # Colori del testo
            "text.color": TOKENS["color"]["text"],
            
            # Linee
            "lines.linewidth": TOKENS["chart"]["line_width"],
            "lines.markersize": 6,
            "lines.solid_capstyle": "round",
            
            # Ciclo colori (palette)
            "axes.prop_cycle": mpl.cycler(color=TOKENS["chart"]["category10"]),
            
            # Legenda
            "legend.fontsize": TOKENS_PT["chart"]["legend_pt"],
            "legend.frameon": False,
            "legend.fancybox": False,
            "legend.edgecolor": "none",
        }
    )


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
