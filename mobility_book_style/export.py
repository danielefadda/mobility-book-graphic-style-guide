"""
Utility per esportare i colori in formati esterni.

Questo modulo fornisce funzioni per esportare la palette di colori
e i design tokens in formati utilizzabili da software di design come
Adobe Creative Suite (ASE - Adobe Swatch Exchange).
"""

import struct
from pathlib import Path
from typing import Dict, Tuple

from ._colors import ALIAS_COLORS
from ._tokens import TOKENS


def hex_to_rgb01(hex_color: str) -> Tuple[float, float, float]:
    """
    Converte un colore esadecimale in tupla RGB normalizzata (0.0-1.0).
    
    Args:
        hex_color: Colore in formato esadecimale (#RRGGBB o RRGGBB)
    
    Returns:
        Tupla (R, G, B) con valori float tra 0.0 e 1.0
    
    Example:
        >>> hex_to_rgb01("#1696D2")
        (0.08627450980392157, 0.5882352941176471, 0.8235294117647058)
    """
    h = hex_color.strip().lstrip("#")
    if len(h) != 6:
        raise ValueError(f"Colore non valido (atteso #RRGGBB): {hex_color}")
    return (int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0)


def _safe_name(name: str) -> str:
    """Rimuove caratteri non validi dai nomi dei colori."""
    for bad in ("/", "\\", ":", "|", "\t", "\n", "\r"):
        name = name.replace(bad, " - ")
    return name.strip()


def _utf16be_name_block(name: str) -> bytes:
    """Crea un blocco nome UTF-16BE per formato ASE."""
    s = _safe_name(name).encode("utf-16-be")
    # length = number of UTF-16 code units INCLUDING the null terminator
    char_count = len(s) // 2 + 1
    return struct.pack(">H", char_count) + s + b"\x00\x00"


def _ase_color_block(name: str, rgb: Tuple[float, float, float]) -> bytes:
    """
    Crea un blocco colore ASE.
    
    ASE Color Entry block (type 0x0001):
      - UTF-16BE name (with length incl. null)
      - color model (4 bytes, 'RGB ')
      - 3 big-endian floats
      - color type (uint16): 0=Global/Process, 1=Spot, 2=Normal
    """
    payload = bytearray()
    payload += _utf16be_name_block(name)
    payload += b"RGB "  # color model
    payload += struct.pack(">fff", *rgb)  # R G B
    payload += struct.pack(">H", 0)  # 0 = process/global
    return struct.pack(">HI", 0x0001, len(payload)) + payload


def export_ase(output_path: str | Path, *, include_aliases: bool = True) -> Path:
    """
    Esporta la palette colori in formato Adobe Swatch Exchange (.ase).
    
    Questo formato è compatibile con Adobe Photoshop, Illustrator, InDesign
    e altre applicazioni che supportano le palette ASE.
    
    Args:
        output_path: Percorso del file .ase da creare
        include_aliases: Se True, include anche i colori alias primitivi
    
    Returns:
        Path: Percorso del file creato
    
    Example:
        >>> import mobility_book_style as mbs
        >>> mbs.export_ase("my_colors.ase")
        PosixPath('my_colors.ase')
    
    Note:
        Il file ASE conterrà:
        - Alias colors (se include_aliases=True): colori primitivi della palette
        - Token colors: colori semantici (text, background, accent, ecc.)
        - Chart category10: palette categoriale per grafici multi-serie
    """
    output_path = Path(output_path)
    blocks = []

    # Aliases (colori primitivi)
    if include_aliases:
        for key, hex_val in ALIAS_COLORS.items():
            label = f"alias {key} ({hex_val.upper()})"
            blocks.append(_ase_color_block(label, hex_to_rgb01(hex_val)))

    # Token colors (colori semantici)
    for key, hex_val in TOKENS["color"].items():
        label = f"token color-{key} ({hex_val.upper()})"
        blocks.append(_ase_color_block(label, hex_to_rgb01(hex_val)))

    # Chart category10 palette
    for i, hex_val in enumerate(TOKENS["chart"]["category10"], start=1):
        label = f"chart category10-{i:02d} ({hex_val.upper()})"
        blocks.append(_ase_color_block(label, hex_to_rgb01(hex_val)))

    # Header ASE (version 1.0, block count)
    header = b"ASEF" + struct.pack(">HHI", 1, 0, len(blocks))
    ase_bytes = header + b"".join(blocks)

    output_path.write_bytes(ase_bytes)
    return output_path


def export_colors_dict() -> Dict[str, str]:
    """
    Esporta tutti i colori come dizionario Python.
    
    Returns:
        Dict: Dizionario con tutte le palette
            - 'aliases': Colori primitivi
            - 'tokens': Colori semantici
            - 'category10': Palette categoriale
    
    Example:
        >>> import mobility_book_style as mbs
        >>> colors = mbs.export_colors_dict()
        >>> colors['tokens']['text']
        '#000000'
        >>> colors['category10'][0]
        '#1696D2'
    
    Note:
        Questa funzione è utile per:
        - Debugging
        - Export in altri formati (JSON, YAML, ecc.)
        - Integrazione con altri tool
    """
    return {
        "aliases": ALIAS_COLORS.copy(),
        "tokens": TOKENS["color"].copy(),
        "category10": TOKENS["chart"]["category10"].copy(),
    }
