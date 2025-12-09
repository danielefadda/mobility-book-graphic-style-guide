"""Verifiche basilari sui font inclusi nel pacchetto."""

from pathlib import Path
import matplotlib.font_manager as fm

import mobility_book_style as mbs
import mobility_book_style.matplotlib as mbs_mpl


def test_fonts_directory_exists():
    fonts_dir = Path(mbs_mpl.__file__).parent / "fonts"
    assert fonts_dir.exists() and fonts_dir.is_dir()
    assert any(fonts_dir.glob("*.ttf"))


def test_inter_font_registered():
    # apply_matplotlib_theme registra i font bundled
    mbs.apply_matplotlib_theme()

    available_fonts = [f.name for f in fm.fontManager.ttflist]
    assert any("Inter" in name for name in available_fonts)


def test_font_license_included():
    fonts_dir = Path(mbs_mpl.__file__).parent / "fonts"
    license_path = fonts_dir / "OFL.txt"

    if license_path.exists():
        content = license_path.read_text()
        assert "SIL OPEN FONT LICENSE" in content.upper()
