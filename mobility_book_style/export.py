"""
Utility per esportare i colori in formati esterni.

Questo modulo fornisce funzioni per esportare la palette di colori
e i design tokens in formati utilizzabili da software di design come
Adobe Creative Suite (ASE - Adobe Swatch Exchange).
"""

import struct
from pathlib import Path
from typing import Dict, Tuple

from ._tokens import token, token_dict


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


def _flatten_colors(data: Dict, prefix: str = "") -> Dict[str, str]:
    flat: Dict[str, str] = {}
    for key, val in data.items():
        if str(key).startswith("_"):
            continue  # salta commenti/metadati
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(val, dict):
            flat.update(_flatten_colors(val, full_key))
        elif isinstance(val, str) and val.startswith("#"):
            flat[full_key] = val
    return flat


def _ordered_palette(mapping: Dict[str, str]) -> list[str]:
    try:
        return [mapping[k] for k in sorted(mapping.keys(), key=lambda v: int(v))]
    except Exception:
        return list(mapping.values())


def export_ase(output_path: str | Path, *, include_base: bool = True) -> Path:
    """Esporta i colori in formato Adobe Swatch Exchange (.ase)."""

    output_path = Path(output_path)
    blocks = []

    colors_flat = _flatten_colors(token_dict["color"], prefix="color")

    for name, hex_val in colors_flat.items():
        if not include_base and name.startswith("color.base"):
            continue
        label = f"{name} ({hex_val.upper()})"
        blocks.append(_ase_color_block(label, hex_to_rgb01(hex_val)))

    header = b"ASEF" + struct.pack(">HHI", 1, 0, len(blocks))
    ase_bytes = header + b"".join(blocks)

    output_path.write_bytes(ase_bytes)
    return output_path


def export_colors_dict() -> Dict[str, str]:
    """Esporta i colori come dizionario annidato e flatten."""

    categorical = _flatten_colors(token_dict["color"]["chart"], prefix="color.chart")
    return {
        "color": token_dict["color"],
        "color_flat": _flatten_colors(token_dict["color"], prefix="color"),
        "categorical_palette": _ordered_palette(token.color.chart.categorical),
        "divergent_palette": _ordered_palette(token.color.chart.divergent),
        "chart_colors": categorical,
    }
