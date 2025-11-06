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
    """Verifica che include_aliases funzioni."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Con aliases
        with_aliases = Path(tmpdir) / "with_aliases.ase"
        mbs.export_ase(with_aliases, include_aliases=True)

        # Senza aliases
        without_aliases = Path(tmpdir) / "without_aliases.ase"
        mbs.export_ase(without_aliases, include_aliases=False)

        # Il file con aliases dovrebbe essere più grande
        assert with_aliases.stat().st_size > without_aliases.stat().st_size


def test_export_colors_dict_structure():
    """Verifica la struttura del dizionario esportato."""
    colors = mbs.export_colors_dict()

    # Verifica chiavi principali
    assert "aliases" in colors
    assert "tokens" in colors
    assert "category10" in colors

    # Verifica che siano dizionari/liste
    assert isinstance(colors["aliases"], dict)
    assert isinstance(colors["tokens"], dict)
    assert isinstance(colors["category10"], list)


def test_export_colors_dict_content():
    """Verifica il contenuto del dizionario esportato."""
    colors = mbs.export_colors_dict()

    # Verifica alcuni colori specifici
    assert "black" in colors["aliases"]
    assert colors["aliases"]["black"] == "#000000"

    assert "text" in colors["tokens"]
    assert colors["tokens"]["text"] == "#000000"

    # Verifica category10 (10 colori)
    assert len(colors["category10"]) == 10
    assert colors["category10"][0] == "#D21616"  # blue-60 (modificato a rosso)


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
