"""
Utility per la conversione di unità di misura e gestione dei design tokens.

Questo modulo centralizza le conversioni tra diverse unità di misura utilizzate
nei design tokens e nelle librerie di visualizzazione.

Conversioni supportate:
- pt (punti tipografici) ↔ px (pixel CSS)
- pt ↔ inch (per Matplotlib)
- Parsing di stringhe con unità (es. "12pt", "16px")

Note:
    - 1 pt = 1/72 inch (standard tipografico)
    - 1 px = 0.75 pt (convenzione CSS a 96 DPI)
    - Matplotlib usa inches per le dimensioni delle figure
    - Altair/Vega-Lite usa pixel CSS per le dimensioni
"""

from __future__ import annotations

from typing import Iterable


# Fattori di conversione standard
PT_PER_INCH = 72.0
PX_PER_PT = 4.0 / 3.0  # 1 px = 0.75 pt, quindi 1 pt = 1.333... px


def pt_to_px(pt: float) -> float:
    """
    Converte punti tipografici in pixel CSS.
    
    Args:
        pt: Valore in punti tipografici
        
    Returns:
        Valore equivalente in pixel CSS
        
    Example:
        >>> pt_to_px(12)
        16.0
        >>> pt_to_px(9)
        12.0
    """
    return pt * PX_PER_PT


def px_to_pt(px: float) -> float:
    """
    Converte pixel CSS in punti tipografici.
    
    Args:
        px: Valore in pixel CSS
        
    Returns:
        Valore equivalente in punti tipografici
        
    Example:
        >>> px_to_pt(16)
        12.0
        >>> px_to_pt(12)
        9.0
    """
    return px / PX_PER_PT


def pt_to_inches(pt: float) -> float:
    """
    Converte punti tipografici in pollici (per Matplotlib).
    
    Args:
        pt: Valore in punti tipografici
        
    Returns:
        Valore equivalente in pollici
        
    Example:
        >>> pt_to_inches(72)
        1.0
        >>> pt_to_inches(36)
        0.5
    """
    return pt / PT_PER_INCH


def inches_to_pt(inches: float) -> float:
    """
    Converte pollici in punti tipografici.
    
    Args:
        inches: Valore in pollici
        
    Returns:
        Valore equivalente in punti tipografici
        
    Example:
        >>> inches_to_pt(1)
        72.0
        >>> inches_to_pt(0.5)
        36.0
    """
    return inches * PT_PER_INCH


def parse_dimension(value: str | float | int) -> float:
    """
    Estrae il valore numerico da una stringa con unità di misura.
    
    Supporta: "12pt", "16px", "1.5in", o valori numerici puri.
    
    Args:
        value: Stringa con unità o valore numerico
        
    Returns:
        Valore numerico senza unità
        
    Example:
        >>> parse_dimension("12pt")
        12.0
        >>> parse_dimension("16px")
        16.0
        >>> parse_dimension(10)
        10.0
    """
    if isinstance(value, (float, int)):
        return float(value)
    
    value_str = str(value).strip().lower()
    
    # Rimuovi unità comuni
    for unit in ["pt", "px", "in", "em", "rem"]:
        if value_str.endswith(unit):
            return float(value_str[:-len(unit)])
    
    # Se non ha unità, prova a convertirlo direttamente
    return float(value_str)


def to_px(value: str | float | int, from_unit: str = "pt") -> float:
    """
    Converte un valore con unità in pixel CSS.
    
    Args:
        value: Valore da convertire (può includere unità nella stringa)
        from_unit: Unità di partenza se value è numerico ('pt', 'px', 'in')
        
    Returns:
        Valore in pixel CSS
        
    Example:
        >>> to_px("12pt")
        16.0
        >>> to_px("16px")
        16.0
        >>> to_px(12, from_unit="pt")
        16.0
    """
    # Se è una stringa, estrai l'unità
    if isinstance(value, str):
        value_str = value.strip().lower()
        if "px" in value_str:
            return parse_dimension(value)
        elif "pt" in value_str:
            return pt_to_px(parse_dimension(value))
        elif "in" in value_str:
            return pt_to_px(inches_to_pt(parse_dimension(value)))
    
    # Se è numerico, usa from_unit
    num_value = float(value)
    if from_unit == "px":
        return num_value
    elif from_unit == "pt":
        return pt_to_px(num_value)
    elif from_unit == "in":
        return pt_to_px(inches_to_pt(num_value))
    
    return num_value


def to_pt(value: str | float | int, from_unit: str = "pt") -> float:
    """
    Converte un valore con unità in punti tipografici.
    
    Args:
        value: Valore da convertire (può includere unità nella stringa)
        from_unit: Unità di partenza se value è numerico ('pt', 'px', 'in')
        
    Returns:
        Valore in punti tipografici
        
    Example:
        >>> to_pt("16px")
        12.0
        >>> to_pt("12pt")
        12.0
        >>> to_pt(16, from_unit="px")
        12.0
    """
    # Se è una stringa, estrai l'unità
    if isinstance(value, str):
        value_str = value.strip().lower()
        if "pt" in value_str:
            return parse_dimension(value)
        elif "px" in value_str:
            return px_to_pt(parse_dimension(value))
        elif "in" in value_str:
            return inches_to_pt(parse_dimension(value))
    
    # Se è numerico, usa from_unit
    num_value = float(value)
    if from_unit == "pt":
        return num_value
    elif from_unit == "px":
        return px_to_pt(num_value)
    elif from_unit == "in":
        return inches_to_pt(num_value)
    
    return num_value


def to_inches(value: str | float | int, from_unit: str = "pt") -> float:
    """
    Converte un valore con unità in pollici (per Matplotlib).
    
    Args:
        value: Valore da convertire (può includere unità nella stringa)
        from_unit: Unità di partenza se value è numerico ('pt', 'px', 'in')
        
    Returns:
        Valore in pollici
        
    Example:
        >>> to_inches("72pt")
        1.0
        >>> to_inches(72, from_unit="pt")
        1.0
        >>> to_inches(1, from_unit="in")
        1.0
    """
    # Se è una stringa, estrai l'unità
    if isinstance(value, str):
        value_str = value.strip().lower()
        if "in" in value_str:
            return parse_dimension(value)
        elif "pt" in value_str:
            return pt_to_inches(parse_dimension(value))
        elif "px" in value_str:
            return pt_to_inches(px_to_pt(parse_dimension(value)))
    
    # Se è numerico, usa from_unit
    num_value = float(value)
    if from_unit == "in":
        return num_value
    elif from_unit == "pt":
        return pt_to_inches(num_value)
    elif from_unit == "px":
        return pt_to_inches(px_to_pt(num_value))
    
    return num_value


def parse_dash_pattern(spec: str) -> tuple[int, Iterable[float]]:
    """
    Converte una specifica di pattern tratteggiato in formato Matplotlib.
    
    Args:
        spec: Stringa tipo "1pt 3pt" o "2 4 1 4"
        
    Returns:
        Tupla (offset, pattern) per Matplotlib
        
    Example:
        >>> parse_dash_pattern("1pt 3pt")
        (0, (1.0, 3.0))
        >>> parse_dash_pattern("2 4")
        (0, (2.0, 4.0))
    """
    parts = [p for p in spec.replace("pt", "").replace("px", "").split() if p]
    nums = tuple(float(p) for p in parts)
    return (0, nums)


def palette_from_numeric_keys(mapping: dict) -> list:
    """
    Estrae valori da un dizionario ordinando le chiavi numericamente.
    
    Utile per estrarre palette categoriali dai token dove le chiavi
    sono stringhe numeriche ("1", "2", "3", ecc.).
    
    Args:
        mapping: Dizionario con chiavi numeriche (stringhe o int)
        
    Returns:
        Lista di valori ordinati per chiave numerica
        
    Example:
        >>> palette = {"1": "#aaa", "3": "#ccc", "2": "#bbb"}
        >>> palette_from_numeric_keys(palette)
        ['#aaa', '#bbb', '#ccc']
    """
    try:
        return [mapping[k] for k in sorted(mapping, key=lambda v: int(v))]
    except Exception:
        return list(mapping.values())



