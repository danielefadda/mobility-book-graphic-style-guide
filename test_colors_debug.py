#!/usr/bin/env python3
"""Script di debug per verificare i colori caricati"""

import mobility_book_style as mbs
from mobility_book_style._tokens import TOKENS

print("=== Debug colori ===")
print(f"\nPrimo colore category10: {TOKENS['chart']['category10'][0]}")
print(f"\nIntera palette category10:")
for i, color in enumerate(TOKENS['chart']['category10'], 1):
    print(f"  {i}. {color}")

print(f"\nColore accent: {TOKENS['color']['accent']}")
print(f"\nColore logo_blue: {TOKENS['color']['logo_blue']}")
