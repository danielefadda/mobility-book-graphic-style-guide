import altair as alt
from design_tokens.design_tokens import TOKENS

def altair_from_tokens():
    return {
        "config": {
            "background": TOKENS["color"]["background"],
            "font": TOKENS["font"]["base_stack"],
            "mark": {"color": TOKENS["color"]["text"]},
            "title": {
                "color": TOKENS["color"]["text"],
                "anchor": "start",
                "dy": -15,
                "fontSize": TOKENS["chart"]["title_size_px"],
                "font": TOKENS["font"]["base_stack"],
                "fontWeight": TOKENS["font"]["weight_bold"],
            },
            "axis": {
                "labelColor": TOKENS["color"]["text"],
                "labelFontSize": TOKENS["chart"]["tick_size_px"],
                "labelFont": TOKENS["font"]["base_stack"],
                "labelFontWeight": TOKENS["font"]["weight_regular"],
                "titleColor": TOKENS["color"]["text"],
                "titleFontSize": TOKENS["chart"]["label_size_px"],
                "titleFont": TOKENS["font"]["base_stack"],
                "titleFontWeight": TOKENS["font"]["weight_bold"],
                "grid": True,
                "gridColor": TOKENS["color"]["grid"],
                "labelAngle": 0,
                "domainWidth": 0.5,
                "labelPadding": 2,
                "tickSize": 5,
                "tickWidth": 0.5,
            },
            "axisX": {"gridDash": [6, 3], "gridWidth": 0.25, "gridColor": TOKENS["color"]["grid"]},
            "axisY": {"gridDash": [6, 3], "gridWidth": 0.25, "gridColor": TOKENS["color"]["grid"]},
            "legend": {
                "labelFontSize": TOKENS["chart"]["legend_size_px"],
                "padding": 1,
                "symbolType": "square",
                "labelFont": TOKENS["font"]["base_stack"],
                "titleFont": TOKENS["font"]["base_stack"],
            },
            "style": {
                "guide-label": {"font": TOKENS["font"]["base_stack"], "fill": TOKENS["color"]["text"]},
                "guide-title": {"font": TOKENS["font"]["base_stack"], "fill": TOKENS["color"]["text"]},
            },
            "range": {"category": TOKENS["chart"]["category10"]},
            "point": {"filled": True},
            "line": {"strokeWidth": TOKENS["chart"]["line_width"]},
            "view": {"stroke": "transparent"},
        }
    }