from colors.alias_colors import ALIAS_COLORS

# Conversion (Matplotlib uses pt)
def px_to_pt(px: float) -> float:
    # 1pt = 1/72 inch; 1px ~ 0.75pt (96dpi). Manteniamo 0.75 per coerenza editoriale.
    return px * 0.75

TOKENS = {
    "font": {
        "base_stack": "Inter, IBM Plex Sans, DejaVu Sans, Arial, sans-serif",
        "mono_stack": "IBM Plex Mono, Menlo, DejaVu Sans Mono, monospace",
        "weight_regular": 400,
        "weight_bold": 600,
    },

    "color": {
        "text":        ALIAS_COLORS["black"],
        "background":  ALIAS_COLORS["white"],
        "grid":        ALIAS_COLORS["gray-20"],
        "domain":      ALIAS_COLORS["gray-90"],
        "accent":      ALIAS_COLORS["blue-60"],
        "muted":       ALIAS_COLORS["gray-50"],
        "cell_shade":  ALIAS_COLORS["gray-10"],
        "logo_blue":   ALIAS_COLORS["blue-60"],
    },

    "chart": {
        "title_size_px": 16,
        "label_size_px": 12,
        "tick_size_px":  11,
        "legend_size_px": 11,
        "line_width": 2.0,
        "category10": [
            ALIAS_COLORS["blue-60"], ALIAS_COLORS["gray-70"], "#1A1A1A",
            ALIAS_COLORS["gray-50"], "#333333", ALIAS_COLORS["gray-30"],
            "#4D4D4D", "#C9C9C9", "#666666", "#DCDCDC"
        ],
    },

    # Stile TABELLE (Inter) – ispirato a Urban, adattato
    "table": {
        # tipografia (px)
        "title_px":    18,      # Inter Bold
        "subtitle_px": 14,      # Inter Regular
        "header_px":   14,      # Inter Bold
        "units_px":    14,      # Inter Regular (in parentesi)
        "body_px":     14,      # Inter Regular
        "logo_px":     14,      # Inter Bold (accent + black)
        "notes_px":    12,      # Inter Regular

        # allineamenti verticali
        "title_valign":  "top",
        "other_valign":  "middle",

        # altezze riga (px)
        "row_1line_px": 34,
        "row_2line_px": 51,
        "row_3line_px": 60,

        # linee e fondi
        "spanner_color": ALIAS_COLORS["black"],
        "body_border":   ALIAS_COLORS["gray-20"],
        "cell_shading":  ALIAS_COLORS["gray-10"],

        # colonne esterne (margini)
        "outer_col_padding_px": 15,
    },
}

# Derivati in pt per Matplotlib/LaTeX
TOKENS_PT = {
    "chart": {
        "title_pt": px_to_pt(TOKENS["chart"]["title_size_px"]),
        "label_pt": px_to_pt(TOKENS["chart"]["label_size_px"]),
        "tick_pt":  px_to_pt(TOKENS["chart"]["tick_size_px"]),
        "legend_pt": px_to_pt(TOKENS["chart"]["legend_size_px"]),
    },
    "table": {
        "title_pt":    px_to_pt(TOKENS["table"]["title_px"]),
        "subtitle_pt": px_to_pt(TOKENS["table"]["subtitle_px"]),
        "header_pt":   px_to_pt(TOKENS["table"]["header_px"]),
        "units_pt":    px_to_pt(TOKENS["table"]["units_px"]),
        "body_pt":     px_to_pt(TOKENS["table"]["body_px"]),
        "logo_pt":     px_to_pt(TOKENS["table"]["logo_px"]),
        "notes_pt":    px_to_pt(TOKENS["table"]["notes_px"]),
        "row_1line_pt": px_to_pt(TOKENS["table"]["row_1line_px"]),
        "row_2line_pt": px_to_pt(TOKENS["table"]["row_2line_px"]),
        "row_3line_pt": px_to_pt(TOKENS["table"]["row_3line_px"]),
    },
}
