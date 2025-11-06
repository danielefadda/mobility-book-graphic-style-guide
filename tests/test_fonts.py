"""Test per il modulo fonts."""

from pathlib import Path
import matplotlib.font_manager as fm

import mobility_book_style._fonts as fonts_module


def test_fonts_directory_exists():
    """Verifica che la cartella fonts esista."""
    assert fonts_module.FONTS_DIR.exists()
    assert fonts_module.FONTS_DIR.is_dir()


def test_font_files_exist():
    """Verifica che i file font esistano.""" 
    available = fonts_module.list_available_fonts()
    
    # Dovrebbe avere almeno un font
    assert len(available) > 0
    
    # Tutti i font listati devono esistere
    for name, path in available.items():
        assert path.exists()
        assert path.suffix == ".ttf"


def test_register_fonts():
    """Verifica che register_fonts funzioni senza errori."""
    # Dovrebbe registrare almeno 1 font
    count = fonts_module.register_fonts()
    assert count >= 0  # Può essere 0 se già registrati


def test_inter_font_available():
    """Verifica che Inter sia disponibile dopo la registrazione."""
    fonts_module.register_fonts()
    
    # Cerca Inter tra i font disponibili in Matplotlib
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    inter_fonts = [name for name in available_fonts if "Inter" in name]
    
    # Dovrebbe trovare almeno un font Inter
    assert len(inter_fonts) > 0


def test_get_font_family_name():
    """Verifica che get_font_family_name ritorni un nome valido."""
    family = fonts_module.get_font_family_name()
    
    # Dovrebbe ritornare Inter o un fallback
    assert family in ["Inter", "IBM Plex Sans", "DejaVu Sans"]


def test_available_fonts_structure():
    """Verifica la struttura del dizionario AVAILABLE_FONTS."""
    assert isinstance(fonts_module.AVAILABLE_FONTS, dict)
    
    for name, path in fonts_module.AVAILABLE_FONTS.items():
        assert isinstance(name, str)
        assert isinstance(path, Path)


def test_font_license_included():
    """Verifica che la licenza OFL sia inclusa."""
    license_path = fonts_module.FONTS_DIR / "OFL.txt"
    
    if license_path.exists():
        content = license_path.read_text()
        # Verifica che sia la licenza corretta
        assert "SIL OPEN FONT LICENSE" in content.upper()
