"""Test per il modulo altair."""

import pytest


def test_altair_import():
    """Verifica che il modulo altair si importi correttamente."""
    import mobility_book_style as mbs

    # Dovrebbe essere importabile
    assert hasattr(mbs, "enable_altair_theme")
    assert hasattr(mbs, "disable_altair_theme")


def test_enable_altair_theme_without_altair():
    """Verifica che senza Altair venga sollevata ImportError."""
    import mobility_book_style.altair as alt_module

    if not alt_module.ALTAIR_AVAILABLE:
        with pytest.raises(ImportError, match="Altair non è installato"):
            import mobility_book_style as mbs

            mbs.enable_altair_theme()


def test_enable_altair_theme_with_altair():
    """Test che richiede Altair installato."""
    import mobility_book_style.altair as alt_module

    if alt_module.ALTAIR_AVAILABLE:
        import altair as alt

        import mobility_book_style as mbs

        # Abilita tema
        mbs.enable_altair_theme()

        # Verifica che il tema sia registrato
        assert "mobility_theme" in alt.themes.names()

        # Verifica che sia attivo
        active_theme = alt.themes.active
        # Il tema dovrebbe essere 'mobility_theme'
        assert active_theme == "mobility_theme"

        # Disabilita e verifica
        mbs.disable_altair_theme()
        assert alt.themes.active == "default"
    else:
        pytest.skip("Altair non installato")


def test_altair_theme_config():
    """Verifica la struttura della configurazione del tema."""
    import mobility_book_style.altair as alt_module

    if alt_module.ALTAIR_AVAILABLE:
        theme = alt_module._build_altair_theme()

        # Verifica struttura base
        assert "config" in theme
        assert "background" in theme["config"]
        assert "font" in theme["config"]
        assert "title" in theme["config"]
        assert "axis" in theme["config"]

        # Verifica che i colori siano stati impostati
        assert theme["config"]["background"] == "#FFFFFF"
        assert "Inter" in theme["config"]["font"]
    else:
        pytest.skip("Altair non installato")
