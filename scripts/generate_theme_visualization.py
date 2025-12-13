#!/usr/bin/env python3
"""
Script per generare la visualizzazione HTML dei design token.

Uso:
    python scripts/generate_theme_visualization.py

Questo genererà un file HTML in docs/theme-visualization.html
"""

import sys
from pathlib import Path

# Aggiungi il parent directory al path per importare il package
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mobility_book_style.theme_visualizer import save_theme_html


def main():
    """Genera e salva l'HTML di visualizzazione del tema."""
    try:
        output_path = save_theme_html()
        print(f"✅ HTML di tema generato con successo!")
        print(f"📁 Salvato in: {output_path}")
        print(f"🌐 Apri in browser: {output_path.as_uri()}")
        return 0
    except Exception as e:
        print(f"❌ Errore durante la generazione: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
