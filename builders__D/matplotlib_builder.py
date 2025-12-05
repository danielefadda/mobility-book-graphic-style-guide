import matplotlib as mpl
from design_tokens.design_tokens import TOKENS, TOKENS_PT

def apply_mpl_theme():
    mpl.rcParams.update({
        "figure.facecolor": TOKENS["color"]["background"],
        "axes.facecolor": TOKENS["color"]["background"],
        "axes.edgecolor": TOKENS["color"]["domain"],
        "axes.labelcolor": TOKENS["color"]["text"],
        "text.color":       TOKENS["color"]["text"],
        "axes.grid": True,
        "grid.color": TOKENS["color"]["grid"],
        "grid.alpha": 0.7,
        "axes.titlesize": TOKENS_PT["chart"]["title_pt"],
        "axes.labelsize": TOKENS_PT["chart"]["label_pt"],
        "xtick.labelsize": TOKENS_PT["chart"]["tick_pt"],
        "ytick.labelsize": TOKENS_PT["chart"]["tick_pt"],
        "legend.fontsize": TOKENS_PT["chart"]["legend_pt"],
        "lines.linewidth": TOKENS["chart"]["line_width"],
        "font.family": "sans-serif",
        "font.sans-serif": [f.strip() for f in TOKENS["font"]["base_stack"].split(",")],
        "axes.prop_cycle": mpl.cycler(color=TOKENS["chart"]["category10"]),
        "axes.spines.top": False,
        "axes.spines.right": False,
        "savefig.facecolor": TOKENS["color"]["background"],
        "savefig.edgecolor": TOKENS["color"]["background"],
    })

# Utility minimale per tabelle Matplotlib con stile Urban-like (Inter)
def style_table(table, *, body_face=None, header_face=None):
    """
    Applica colori/linee/font Inter alle tabelle create con matplotlib.table.Table.
    - table: oggetto ritornato da plt.table(...)
    """
    body_face = body_face or "white"
    header_face = header_face or TOKENS["color"]["cell_shade"]

    for (row, col), cell in table.get_celld().items():
        # header: row == 0
        if row == 0:
            cell.set_facecolor(header_face)
            cell.set_edgecolor(TOKENS["color"]["body_border"])
            cell.set_linewidth(0.8)
            cell.get_text().set_fontsize(TOKENS_PT["table"]["header_pt"])
            cell.get_text().set_fontfamily("Inter")
            cell.get_text().set_fontweight(TOKENS["font"]["weight_bold"])
            cell.get_text().set_color(TOKENS["color"]["text"])
        else:
            cell.set_facecolor(body_face)
            cell.set_edgecolor(TOKENS["color"]["body_border"])
            cell.set_linewidth(0.5)
            cell.get_text().set_fontsize(TOKENS_PT["table"]["body_pt"])
            cell.get_text().set_fontfamily("Inter")
            cell.get_text().set_color(TOKENS["color"]["text"])
