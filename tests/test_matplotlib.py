"""Test per il modulo matplotlib."""

import matplotlib as mpl
import pytest

import mobility_book_style as mbs


def test_apply_matplotlib_theme():
    """Verifica che il tema Matplotlib venga applicato correttamente."""
    # Applica il tema
    mbs.apply_matplotlib_theme()

    # Verifica che i parametri siano stati impostati
    assert mpl.rcParams["font.family"] == ["sans-serif"]
    assert "Inter" in mpl.rcParams["font.sans-serif"]

    # Verifica colori
    assert mpl.rcParams["figure.facecolor"].upper() == "#FFFFFF"
    assert mpl.rcParams["axes.facecolor"].upper() == "#FFFFFF"
    assert mpl.rcParams["text.color"].startswith("#")

    # Verifica dimensioni
    assert mpl.rcParams["axes.titlesize"] == 12.0  # 16px * 0.75
    assert mpl.rcParams["lines.linewidth"] == 2.0

    # Verifica che la griglia sia abilitata
    assert mpl.rcParams["axes.grid"] is True

    # Verifica che top/right spine siano disabilitati
    assert mpl.rcParams["axes.spines.top"] is False
    assert mpl.rcParams["axes.spines.right"] is False


def test_style_table_no_crash():
    """Verifica che style_table non sollevi eccezioni."""
    import matplotlib.pyplot as plt

    # Applica tema
    mbs.apply_matplotlib_theme()

    # Crea una semplice tabella
    fig, ax = plt.subplots()
    ax.axis("off")

    data = [["Header1", "Header2"], ["Value1", "Value2"]]
    table = ax.table(cellText=data, loc="center")

    # Applica lo stile (non dovrebbe sollevare eccezioni)
    mbs.style_table(table)

    # Cleanup
    plt.close(fig)


def test_theme_persistence():
    """Verifica che il tema persista dopo l'applicazione."""
    # Salva valori originali
    original_font = mpl.rcParams["font.sans-serif"].copy()

    # Applica tema
    mbs.apply_matplotlib_theme()

    # Verifica che il tema sia applicato
    assert "Inter" in mpl.rcParams["font.sans-serif"]

    # Crea un nuovo plot (dovrebbe usare il tema)
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 2, 3])

    # Il tema dovrebbe essere ancora attivo
    assert "Inter" in mpl.rcParams["font.sans-serif"]

    # Cleanup
    plt.close(fig)

    # Ripristina (opzionale, per pulizia)
    mpl.rcParams["font.sans-serif"] = original_font
