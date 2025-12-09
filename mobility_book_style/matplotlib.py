"""Applicazione del tema Matplotlib basato sui design token."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib as mpl
import matplotlib.font_manager as fm
from cycler import cycler

from ._tokens import token


def _px_to_pt(px: float | int) -> float:
    return float(px) * 0.75


def _as_pt(value: str | float | int) -> float:
    if isinstance(value, (float, int)):
        return float(value)
    if isinstance(value, str) and value.endswith("pt"):
        return float(value[:-2])
    if isinstance(value, str) and value.endswith("px"):
        return _px_to_pt(float(value[:-2]))
    return float(value)


def _as_dash(spec: str) -> tuple[int, Iterable[float]]:
    parts = [p for p in spec.replace("pt", "").split() if p]
    nums = tuple(float(p) for p in parts)
    return (0, nums)


def _palette_from_numeric_keys(mapping: dict) -> list:
    try:
        return [mapping[k] for k in sorted(mapping, key=lambda v: int(v))]
    except Exception:
        return list(mapping.values())


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

    palette = _palette_from_numeric_keys(token.color.chart.categorical)
    grid_dash = _as_dash(token.chart.element.grid.dash)

    mpl.rcParams.update({
        "figure.facecolor": token.color.background.default,
        "axes.facecolor": token.color.background.default,
        "savefig.facecolor": token.color.background.default,

        "font.family": "sans-serif",
        "font.sans-serif": font_stack,
        "text.color": token.color.text.primary,

        "axes.titlesize": _as_pt(token.chart.typography.title.fontSize),
        "axes.titleweight": token.chart.typography.title.fontWeight,
        "axes.titlelocation": "left",
        "axes.titlecolor": token.chart.typography.title.color,

        "axes.labelsize": _as_pt(token.chart.typography.label.fontSize),
        "axes.labelweight": token.chart.typography.label.fontWeight,
        "axes.labelcolor": token.chart.typography.label.color,
        "axes.labelpad": 8,

        "xtick.labelsize": _as_pt(token.chart.typography.label.fontSize),
        "ytick.labelsize": _as_pt(token.chart.typography.label.fontSize),
        "xtick.color": token.chart.element.tick.color,
        "ytick.color": token.chart.element.tick.color,
        "xtick.major.size": _as_pt(token.chart.element.tick.length),
        "ytick.major.size": _as_pt(token.chart.element.tick.length),
        "xtick.major.width": _as_pt(token.chart.element.tick.width),
        "ytick.major.width": _as_pt(token.chart.element.tick.width),

        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": _as_pt(token.chart.element.spine.width),
        "axes.edgecolor": token.chart.element.spine.color,

        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": token.chart.element.grid.color,
        "grid.linewidth": _as_pt(token.chart.element.grid.width),
        "grid.linestyle": grid_dash,
        "grid.alpha": 1.0,

        "lines.linewidth": max(1.5, _as_pt(token.chart.element.axis.width) * 2.0),
        "lines.solid_capstyle": "round",
        "axes.prop_cycle": cycler(color=palette),

        "legend.fontsize": _as_pt(token.chart.typography.annotation.fontSize),
        "legend.title_fontsize": _as_pt(token.chart.typography.label.fontSize),
        "legend.frameon": False,
        "legend.loc": "upper right",
    })


def style_table(table, *, body_face: str | None = None, header_face: str | None = None):
    """Applica il tema tabellare ai ``Table`` di Matplotlib."""

    body_face = body_face or token.component.table.color.rowZebra
    header_face = header_face or token.component.table.color.headerBg

    header_border = token.component.table.color.border.spanner
    body_border = token.component.table.color.border.body

    header_size = _as_pt(token.component.table.typography.header.fontSize)
    body_size = _as_pt(token.component.table.typography.body.fontSize)
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
