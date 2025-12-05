"""
Design tokens semantici - Letti dinamicamente da JSON.

I design tokens definiscono la semantica dei colori e delle dimensioni
utilizzate nelle visualizzazioni. Sono costruiti a partire dal file
mobility_book_style/data/design_tokens.json.

Importante:
    Questi valori sono immutabili e letti dal JSON. Per modificare i token,
    edita il file design_tokens.json e riavvia il kernel Python.
"""

import json
import re
from pathlib import Path
from typing import Any

from ._colors import ALIAS_COLORS


def px_to_pt(px: float) -> float:
    """
    Converte pixel in punti tipografici.
    
    1pt = 1/72 inch; 1px ~ 0.75pt (96dpi standard).
    Manteniamo 0.75 per coerenza editoriale.
    
    Args:
        px: Valore in pixel
        
    Returns:
        float: Valore convertito in punti
    """
    return px * 0.75


def _resolve_references(data: Any, alias_colors: dict) -> Any:
    """
    Risolve i riferimenti nel formato {alias.xxx} o {colors.xxx} ricorsivamente.
    
    Esempio:
        Input: "{alias.teal-500}"
        Output: "#348b96"
    
    Args:
        data: Dati grezzi (dict, list, string, etc.)
        alias_colors: Dizionario ALIAS_COLORS per risolvere i riferimenti
        
    Returns:
        Dati con tutti i riferimenti risolti
    """
    if isinstance(data, dict):
        return {k: _resolve_references(v, alias_colors) for k, v in data.items()}
    elif isinstance(data, list):
        return [_resolve_references(item, alias_colors) for item in data]
    elif isinstance(data, str):
        # Risolvi {alias.xxx-yyy} → valore HEX
        match = re.match(r'\{alias\.([^}]+)\}', data)
        if match:
            key = match.group(1)
            if key not in alias_colors:
                raise KeyError(
                    f"Alias '{key}' non trovato in alias.json. "
                    f"Chiavi disponibili: {list(alias_colors.keys())}"
                )
            return alias_colors[key]
        
        # I riferimenti {colors.xxx} o {semantic.xxx} rimangono come stringa
        # (per ora non sono risolti, potrebbero essere usati per validazione)
        return data
    else:
        return data


def _load_tokens() -> dict:
    """
    Legge il file design_tokens.json, risolve i riferimenti e popola TOKENS.
    
    Returns:
        dict: Dizionario con i token organizzati per categoria
        
    Raises:
        FileNotFoundError: Se il file design_tokens.json non esiste
        json.JSONDecodeError: Se il file JSON è malformato
        KeyError: Se un riferimento non può essere risolto
    """
    json_path = Path(__file__).parent / "data" / "design_tokens.json"
    
    if not json_path.exists():
        raise FileNotFoundError(
            f"File design_tokens.json non trovato: {json_path}\n"
            "Assicurati che il file esista in mobility_book_style/data/"
        )
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            raw_tokens = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"File design_tokens.json malformato: {e.msg} (linea {e.lineno}, colonna {e.colno})",
            e.doc,
            e.pos
        )
    
    # Risolvi i riferimenti {alias.xxx}
    resolved = _resolve_references(raw_tokens, ALIAS_COLORS)
    
    return resolved


# Carica i token dal JSON
_raw_tokens = _load_tokens()

# Estrai le sezioni principali
TOKENS = {
    "font": _raw_tokens.get("font", {}),
    "color": _raw_tokens.get("color", {}),
    "chart": _raw_tokens.get("chart", {}),
    "table": _raw_tokens.get("table", {}),
    "semantic": _raw_tokens.get("semantic", {}),
    "components": _raw_tokens.get("components", {}),
}

# Derivati in pt per Matplotlib/LaTeX
TOKENS_PT = {
    "chart": {
        "title_pt": px_to_pt(TOKENS.get("chart", {}).get("title_size_px", 16)),
        "label_pt": px_to_pt(TOKENS.get("chart", {}).get("label_size_px", 12)),
        "tick_pt": px_to_pt(TOKENS.get("chart", {}).get("tick_size_px", 11)),
        "legend_pt": px_to_pt(TOKENS.get("chart", {}).get("legend_size_px", 11)),
    },
    "table": {
        "title_pt": px_to_pt(TOKENS.get("table", {}).get("title_px", 18)),
        "subtitle_pt": px_to_pt(TOKENS.get("table", {}).get("subtitle_px", 14)),
        "header_pt": px_to_pt(TOKENS.get("table", {}).get("header_px", 14)),
        "units_pt": px_to_pt(TOKENS.get("table", {}).get("units_px", 14)),
        "body_pt": px_to_pt(TOKENS.get("table", {}).get("body_px", 14)),
        "logo_pt": px_to_pt(TOKENS.get("table", {}).get("logo_px", 14)),
        "notes_pt": px_to_pt(TOKENS.get("table", {}).get("notes_px", 12)),
        "row_1line_pt": px_to_pt(TOKENS.get("table", {}).get("row_1line_px", 34)),
        "row_2line_pt": px_to_pt(TOKENS.get("table", {}).get("row_2line_px", 51)),
        "row_3line_pt": px_to_pt(TOKENS.get("table", {}).get("row_3line_px", 60)),
    },
}
