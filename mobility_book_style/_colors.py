"""
Palette colori primitiva (alias) - Letta dinamicamente da JSON.

Questa è la palette "alias" con i valori grezzi dei colori.
Non ha semantica, serve solo come base per i design tokens.

Il dizionario ALIAS_COLORS viene popolato dinamicamente dal file
mobility_book_style/data/alias.json all'import.
"""

import json
import warnings
from pathlib import Path


def _load_alias_colors() -> dict:
    """
    Legge il file alias.json e crea il dizionario ALIAS_COLORS.
    
    Returns:
        dict: Dizionario con chiavi "colore-intensità" e valori HEX.
    
    Raises:
        FileNotFoundError: Se il file alias.json non esiste.
        json.JSONDecodeError: Se il file JSON è malformato.
    """
    json_path = Path(__file__).parent / "data" / "alias.json"
    
    if not json_path.exists():
        raise FileNotFoundError(
            f"File alias.json non trovato: {json_path}\n"
            "Assicurati che il file esista in mobility_book_style/data/"
        )
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            colors = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"File alias.json malformato: {e.msg} (linea {e.lineno}, colonna {e.colno})",
            e.doc,
            e.pos
        )
    
    # Avviso se in site-packages (ambiente non-editable)
    if "site-packages" in str(json_path):
        warnings.warn(
            "Stai usando una versione installata di mobility_book_style. "
            "Le modifiche ai JSON potrebbero non essere persistenti. "
            "Per sviluppare, usa: pip install -e .",
            UserWarning
        )
    
    return colors


# Carica il dizionario una sola volta
ALIAS_COLORS: dict = _load_alias_colors()
