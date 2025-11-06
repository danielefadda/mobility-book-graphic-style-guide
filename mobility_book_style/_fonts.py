"""
Gestione font per Mobility Book Style.

Questo modulo gestisce la registrazione automatica dei font Inter
in Matplotlib, eliminando il warning "Font family 'Inter' not found".
"""

from pathlib import Path
import matplotlib.font_manager as fm
import warnings

# Path alla cartella fonts del pacchetto
FONTS_DIR = Path(__file__).parent / "fonts"

# Font disponibili nel pacchetto
AVAILABLE_FONTS = {
    "Inter-Variable": FONTS_DIR / "Inter-VariableFont_opsz,wght.ttf",
    "Inter-Italic-Variable": FONTS_DIR / "Inter-Italic-VariableFont_opsz,wght.ttf",
}


def register_fonts():
    """
    Registra i font Inter in Matplotlib.
    
    Questa funzione viene chiamata automaticamente all'import del pacchetto.
    Registra i font Inter inclusi nella libreria nella cache di Matplotlib,
    eliminando il warning "Font family 'Inter' not found".
    
    Returns:
        int: Numero di font registrati con successo
    
    Note:
        - Viene chiamata automaticamente quando importi mobility_book_style
        - I font restano disponibili per tutta la sessione Python
        - Se i font sono già registrati, non viene fatto nulla
    """
    registered = 0
    
    for font_name, font_path in AVAILABLE_FONTS.items():
        if not font_path.exists():
            warnings.warn(
                f"Font {font_name} non trovato in {font_path}. "
                f"Il tema userà i font di fallback.",
                UserWarning
            )
            continue
        
        try:
            # Registra il font in Matplotlib
            fm.fontManager.addfont(str(font_path))
            registered += 1
        except Exception as e:
            warnings.warn(
                f"Impossibile registrare font {font_name}: {e}. "
                f"Il tema userà i font di fallback.",
                UserWarning
            )
    
    # Ricostruisci la cache dei font
    if registered > 0:
        fm._load_fontmanager(try_read_cache=False)
    
    return registered


def list_available_fonts():
    """
    Lista i font Inter disponibili nel pacchetto.
    
    Returns:
        dict: Dizionario con nome font → path
    
    Example:
        >>> from mobility_book_style._fonts import list_available_fonts
        >>> fonts = list_available_fonts()
        >>> for name, path in fonts.items():
        ...     print(f"{name}: {path.exists()}")
    """
    return {
        name: path 
        for name, path in AVAILABLE_FONTS.items() 
        if path.exists()
    }


def get_font_family_name():
    """
    Ottiene il nome della famiglia di font da usare in Matplotlib.
    
    Returns:
        str: Nome famiglia font ("Inter" se disponibile, altrimenti primo fallback)
    
    Note:
        Questa funzione verifica se Inter è stato registrato correttamente
        e ritorna il nome appropriato da usare in rcParams.
    """
    # Verifica se Inter è disponibile
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    if any("Inter" in name for name in available_fonts):
        return "Inter"
    else:
        # Fallback alla prossima opzione nella font stack
        return "IBM Plex Sans"


# Auto-registrazione all'import (può essere disabilitata se necessario)
_AUTO_REGISTER = True

if _AUTO_REGISTER:
    try:
        _registered_count = register_fonts()
        if _registered_count > 0:
            # Messaggio silenzioso, solo per debug
            pass  # print(f"✓ {_registered_count} font Inter registrati")
    except Exception as e:
        warnings.warn(
            f"Impossibile auto-registrare i font Inter: {e}. "
            f"Il tema userà i font di fallback.",
            UserWarning
        )
