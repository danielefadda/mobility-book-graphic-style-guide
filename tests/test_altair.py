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
        assert "mobility_theme" in alt.theme.names()

        # Verifica che sia attivo
        active_theme = alt.theme.active
        # Il tema dovrebbe essere 'mobility_theme'
        assert active_theme == "mobility_theme"

        # Disabilita e verifica
        mbs.disable_altair_theme()
        assert alt.theme.active == "default"
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
        assert theme["config"]["background"].upper() == "#FFFFFF"
        assert "Inter" in theme["config"]["font"]
    else:
        pytest.skip("Altair non installato")


def test_altair_font_css_inline():
    """Verifica che il CSS inline includa Inter (senza '18pt' per evitare confusione)."""
    import mobility_book_style.altair as alt_module

    css = alt_module.get_altair_font_css()
    assert "font-family: 'Inter'" in css
    assert "@font-face" in css

    embed_opts = alt_module.altair_embed_options_with_inter()
    assert "defaultStyle" in embed_opts
    assert "font-family: 'Inter'" in embed_opts["defaultStyle"]

def test_altair_css_injection_in_html():
    """Verifica che il CSS @font-face sia iniettato nel HTML generato da to_html()."""
    import mobility_book_style.altair as alt_module

    if alt_module.ALTAIR_AVAILABLE:
        import altair as alt
        import mobility_book_style as mbs

        # Abilita il tema (che applica il monkey-patch)
        mbs.enable_altair_theme()

        # Crea un semplice chart
        data = alt.Data(values=[{"x": "A", "y": 10}, {"x": "B", "y": 20}])
        chart = alt.Chart(data).mark_bar().encode(x="x:N", y="y:Q")

        # Genera HTML
        html = chart.to_html()

        # Verifica che il CSS sia presente
        assert "@font-face" in html, "CSS @font-face non trovato nel HTML"
        assert "font-family: 'Inter'" in html, "Font Inter non trovato nel HTML"
        assert "data:font/ttf;base64," in html, "Data URI dei font non trovato nel HTML"
    else:
        pytest.skip("Altair non installato")