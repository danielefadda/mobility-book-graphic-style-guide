"""Test per il modulo export."""

import tempfile
from pathlib import Path

import mobility_book_style as mbs


def test_export_ase_creates_file():
    """Verifica che export_ase crei un file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_colors.ase"
        result = mbs.export_ase(output_path)

        assert result.exists()
        assert result.suffix == ".ase"
        assert result.stat().st_size > 0


def test_export_ase_header():
    """Verifica che il file ASE abbia l'header corretto."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test.ase"
        mbs.export_ase(output_path)

        content = output_path.read_bytes()
        # Header ASE dovrebbe iniziare con "ASEF"
        assert content[:4] == b"ASEF"


def test_export_ase_with_and_without_aliases():
    """Verifica che include_base filtri le palette base."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Con base
        with_base = Path(tmpdir) / "with_base.ase"
        mbs.export_ase(with_base, include_base=True)

        # Senza base
        without_base = Path(tmpdir) / "without_base.ase"
        mbs.export_ase(without_base, include_base=False)

        # Il file con i colori base dovrebbe essere più grande
        assert with_base.stat().st_size > without_base.stat().st_size


def test_export_colors_dict_structure():
    """Verifica la struttura del dizionario esportato."""
    colors = mbs.export_colors_dict()

    # Verifica chiavi principali
    assert "color" in colors
    assert "color_flat" in colors
    assert "categorical_palette" in colors
    assert "divergent_palette" in colors

    # Verifica che siano dizionari/liste
    assert isinstance(colors["color"], dict)
    assert isinstance(colors["color_flat"], dict)
    assert isinstance(colors["categorical_palette"], list)
    assert isinstance(colors["divergent_palette"], list)


def test_export_colors_dict_content():
    """Verifica il contenuto del dizionario esportato."""
    colors = mbs.export_colors_dict()

    assert colors["color"]["brand"]["primary"].startswith("#")
    assert colors["color"]["text"]["primary"].startswith("#")

    # Palette categoriale
    assert len(colors["categorical_palette"]) == 7
    assert all(c.startswith("#") for c in colors["categorical_palette"])


def test_hex_to_rgb01():
    """Verifica la conversione hex to RGB."""
    from mobility_book_style.export import hex_to_rgb01

    # Nero
    assert hex_to_rgb01("#000000") == (0.0, 0.0, 0.0)

    # Bianco
    assert hex_to_rgb01("#FFFFFF") == (1.0, 1.0, 1.0)

    # Blue-60
    rgb = hex_to_rgb01("#1696D2")
    assert 0.08 < rgb[0] < 0.09  # R
    assert 0.58 < rgb[1] < 0.59  # G
    assert 0.82 < rgb[2] < 0.83  # B


def test_hex_to_rgb01_invalid():
    """Verifica che colori invalidi sollevino errore."""
    from mobility_book_style.export import hex_to_rgb01
    import pytest

    with pytest.raises(ValueError):
        hex_to_rgb01("#FFF")  # Troppo corto

    with pytest.raises(ValueError):
        hex_to_rgb01("not a color")


def test_export_ase_string_path():
    """Verifica che export_ase accetti sia str che Path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Con string
        output_str = str(Path(tmpdir) / "test_str.ase")
        result1 = mbs.export_ase(output_str)
        assert result1.exists()

        # Con Path
        output_path = Path(tmpdir) / "test_path.ase"
        result2 = mbs.export_ase(output_path)
        assert result2.exists()
