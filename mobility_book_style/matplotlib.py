"""Applicazione del tema Matplotlib basato sui design token."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.font_manager as fm
from cycler import cycler

from ._tokens import token
from .utils import to_pt, to_inches, parse_dash_pattern, palette_from_numeric_keys


_FONTS_REGISTERED = False


def _register_fonts_once() -> int:
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return 0

    fonts_dir = Path(__file__).parent / "fonts"
    if not fonts_dir.exists():
        return 0

    registered = 0
    for font_path in fonts_dir.glob("*.ttf"):
        try:
            fm.fontManager.addfont(str(font_path))
            registered += 1
        except Exception:
            continue

    if registered:
        fm._load_fontmanager(try_read_cache=False)
    _FONTS_REGISTERED = True
    return registered


def apply_matplotlib_theme():
    """Configura ``mpl.rcParams`` usando i token risolti."""

    _register_fonts_once()

    # Font stack (es. "Inter, sans-serif" -> ["Inter", "sans-serif"])
    font_stack = [f.strip() for f in token.font.family.sans.split(",")]

    palette = palette_from_numeric_keys(token.color.chart.categorical)
    
    # Calcola le dimensioni di default della figura dai token
    fig_width = to_inches(token.component.figure.default.width)
    fig_height = to_inches(token.component.figure.default.height)

    mpl.rcParams.update({
        "figure.figsize": [fig_width, fig_height],
        "figure.facecolor": token.color.background.default,
        "axes.facecolor": token.color.background.default,
        "savefig.facecolor": token.color.background.default,

        "font.family": "sans-serif",
        "font.sans-serif": font_stack,
        "text.color": token.color.text.primary,

        "axes.titlesize": to_pt(token.chart.typography.title.fontSize),
        "axes.titleweight": token.chart.typography.title.fontWeight,
        "axes.titlelocation": "left",
        "axes.titlecolor": token.chart.typography.title.color,

        "axes.labelsize": to_pt(token.chart.typography.label.fontSize),
        "axes.labelweight": token.chart.typography.label.fontWeight,
        "axes.labelcolor": token.chart.typography.label.color,
        "axes.labelpad": 8,

        "xtick.labelsize": to_pt(token.chart.typography.tickLabel.fontSize),
        "ytick.labelsize": to_pt(token.chart.typography.tickLabel.fontSize),
        "xtick.color": token.chart.element.tick.x.color,
        "ytick.color": token.chart.element.tick.color,
        "xtick.major.size": to_pt(token.chart.element.tick.x.length),
        "ytick.major.size": 0,  # Nasconde le tacchette sull'asse Y
        "xtick.major.width": to_pt(token.chart.element.tick.x.width),
        "ytick.major.width": to_pt(token.chart.element.tick.width),

        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,  # Nasconde l'asse Y
        "axes.linewidth": to_pt(token.chart.element.spine.width),
        "axes.edgecolor": token.chart.element.spine.color,

        "axes.grid": True,
        "axes.grid.axis": "y",  # Solo linee orizzontali (asse Y)
        "axes.axisbelow": True,
        "grid.color": token.chart.element.grid.color,
        "grid.linewidth": to_pt(token.chart.element.grid.width),
        "grid.linestyle": "-",  # Linea continua
        "grid.alpha": 1.0,

        "lines.linewidth": to_pt(token.chart.data.line.width),
        "lines.solid_capstyle": token.chart.data.line.joinStyle,
        "lines.markersize" : to_pt(token.chart.data.line.markerSize),
        "lines.color": token.color.brand.primary,
        "axes.prop_cycle": cycler(color=palette),

        "legend.fontsize": to_pt(token.chart.typography.annotation.fontSize),
        "legend.title_fontsize": to_pt(token.chart.typography.label.fontSize),
        "legend.frameon": False,
        "legend.loc": "upper right",
    })


def style_table(table, *, body_face: str | None = None, header_face: str | None = None):
    """Applica il tema tabellare ai ``Table`` di Matplotlib."""

    body_face = body_face or token.component.table.color.rowZebra
    header_face = header_face or token.component.table.color.headerBg

    header_border = token.component.table.color.border.spanner
    body_border = token.component.table.color.border.body

    header_size = to_pt(token.component.table.typography.header.fontSize)
    body_size = to_pt(token.component.table.typography.body.fontSize)
    text_color = token.color.text.primary
    font_stack = [f.strip() for f in token.font.family.sans.split(",")]

    for (row, _col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor(header_face)
            cell.set_edgecolor(header_border)
            cell.set_linewidth(0.8)
            cell.get_text().set_fontsize(header_size)
            cell.get_text().set_fontfamily(font_stack[0])
            cell.get_text().set_fontweight(token.font.weight.bold)
            cell.get_text().set_color(text_color)
        else:
            cell.set_facecolor(body_face)
            cell.set_edgecolor(body_border)
            cell.set_linewidth(0.5)
            cell.get_text().set_fontsize(body_size)
            cell.get_text().set_fontfamily(font_stack[0])
            cell.get_text().set_color(text_color)
