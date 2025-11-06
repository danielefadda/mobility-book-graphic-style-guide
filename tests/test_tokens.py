"""Test per i design tokens."""

import mobility_book_style._tokens as tokens_module


def test_tokens_exist():
    """Verifica che i tokens principali esistano."""
    assert hasattr(tokens_module, "TOKENS")
    assert hasattr(tokens_module, "TOKENS_PT")


def test_tokens_structure():
    """Verifica la struttura dei TOKENS."""
    tokens = tokens_module.TOKENS

    # Verifica categorie principali
    assert "font" in tokens
    assert "color" in tokens
    assert "chart" in tokens
    assert "table" in tokens

    # Verifica font
    assert "base_stack" in tokens["font"]
    assert "Inter" in tokens["font"]["base_stack"]

    # Verifica colori
    assert "text" in tokens["color"]
    assert "background" in tokens["color"]
    assert tokens["color"]["background"] == "#FFFFFF"

    # Verifica chart
    assert "category10" in tokens["chart"]
    assert len(tokens["chart"]["category10"]) == 10


def test_tokens_pt_structure():
    """Verifica la struttura dei TOKENS_PT."""
    tokens_pt = tokens_module.TOKENS_PT

    assert "chart" in tokens_pt
    assert "table" in tokens_pt

    # Verifica conversione px->pt
    assert tokens_pt["chart"]["title_pt"] == 12.0  # 16px * 0.75


def test_px_to_pt_conversion():
    """Verifica la funzione di conversione px->pt."""
    px_to_pt = tokens_module.px_to_pt

    assert px_to_pt(16) == 12.0
    assert px_to_pt(12) == 9.0
    assert px_to_pt(0) == 0.0


def test_tokens_immutability_awareness():
    """
    Verifica che i tokens siano accessibili (non testa vera immutabilità,
    ma documenta l'intenzione che dovrebbero essere read-only).
    """
    tokens = tokens_module.TOKENS

    # I tokens dovrebbero essere leggibili
    assert tokens["color"]["text"] == "#000000"

    # Nota: in Python non possiamo rendere veramente immutabile un dict
    # senza wrapping speciale, ma documentiamo l'intenzione
