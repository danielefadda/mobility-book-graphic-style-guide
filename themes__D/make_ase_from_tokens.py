#!/usr/bin/env python3
from __future__ import annotations
import importlib
import struct
import sys
from pathlib import Path
from typing import Dict, Tuple

THIS_FILE = Path(__file__).resolve()
ROOT = THIS_FILE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ---------- helpers ----------
def hex_to_rgb01(hex_color: str) -> Tuple[float, float, float]:
    h = hex_color.strip().lstrip("#")
    if len(h) != 6:
        raise ValueError(f"Colore non valido (atteso #RRGGBB): {hex_color}")
    return (int(h[0:2], 16)/255.0, int(h[2:4], 16)/255.0, int(h[4:6], 16)/255.0)

def safe_name(name: str) -> str:
    for bad in ("/", "\\", ":", "|", "\t", "\n", "\r"):
        name = name.replace(bad, " - ")
    return name.strip()

def utf16be_name_block(name: str) -> bytes:
    s = safe_name(name).encode("utf-16-be")
    # length = number of UTF-16 code units INCLUDING the null terminator
    char_count = len(s)//2 + 1
    return struct.pack(">H", char_count) + s + b"\x00\x00"

def ase_color_block(name: str, rgb):
    """
    ASE Color Entry block (type 0x0001):
      - UTF-16BE name (with length incl. null)
      - color model (4 bytes, 'RGB ')
      - 3 big-endian floats
      - color type (uint16): 0=Global/Process, 1=Spot, 2=Normal
    """
    payload = bytearray()
    payload += utf16be_name_block(name)
    payload += b"RGB "                     # color model
    payload += struct.pack(">fff", *rgb)   # R G B
    payload += struct.pack(">H", 0)        # 0 = process/global
    return struct.pack(">HI", 0x0001, len(payload)) + payload  # NOTE: 0x0001

# ---------- load tokens/aliases ----------
def load_tokens() -> Dict:
    mod = importlib.import_module("design_tokens.design_tokens")
    if not hasattr(mod, "TOKENS"):
        raise RuntimeError("TOKENS mancante in design_tokens/design_tokens.py")
    return mod.TOKENS

def load_alias_colors_if_any() -> Dict[str, str] | None:
    try:
        mod = importlib.import_module("colors.alias_colors")
        return getattr(mod, "ALIAS_COLORS", None)
    except Exception:
        return None

def resolve_color(value: str, aliases: Dict[str, str] | None) -> str:
    if isinstance(value, str) and value.startswith("alias:") and aliases:
        key = value.split(":", 1)[1]
        hexval = aliases.get(key)
        if not hexval:
            raise KeyError(f"Alias '{key}' non trovato in colors/alias_colors.py")
        return hexval
    return value

# ---------- main ----------
def main() -> Path:
    out_path = ROOT / "book_mobility_swatches.ase"

    TOKENS = load_tokens()
    ALIASES = load_alias_colors_if_any()

    blocks = []

    # Aliases (se presenti) -> campioni piatti
    if ALIASES:
        for k, hexval in ALIASES.items():
            blocks.append(ase_color_block(f"alias {k} ({hexval.upper()})", hex_to_rgb01(hexval)))

    # Tokens "color"
    for k, v in TOKENS.get("color", {}).items():
        hexval = resolve_color(v, ALIASES)
        blocks.append(ase_color_block(f"token color-{k} ({hexval.upper()})", hex_to_rgb01(hexval)))

    # Palette chart.category10 (se presente)
    for i, c in enumerate(TOKENS.get("chart", {}).get("category10", []), start=1):
        blocks.append(ase_color_block(f"chart category10-{i:02d} ({c.upper()})", hex_to_rgb01(c)))

    # Header ASE (version 1.0, block count = len(blocks))
    header = b"ASEF" + struct.pack(">HHI", 1, 0, len(blocks))
    ase_bytes = header + b"".join(blocks)

    out_path.write_bytes(ase_bytes)
    print(f"Creato: {out_path}  ({out_path.stat().st_size} bytes)")
    print(f"- Swatch totali: {len(blocks)}")
    return out_path

if __name__ == "__main__":
    main()
