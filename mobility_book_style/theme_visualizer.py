"""
Theme Visualizer - Genera visualizzazioni HTML dei design token.

Questo modulo crea file HTML interattivi che visualizzano le palette,
i colori semantici e le sequenze definiti nei design token.
"""

from pathlib import Path
from typing import Dict, List
from . import theme


def generate_theme_html() -> str:
    """
    Genera HTML interattivo con visualizzazione di tutte le palette e colori.
    
    Returns:
        Stringa HTML completa
    
    Nota:
        Questo HTML usa le funzioni del modulo theme per ottenere i colori,
        quindi si aggiorna automaticamente se i token cambiano.
    """
    
    # Ottieni tutte le palette disponibili
    palettes = {}
    for palette_name in theme.list_palettes():
        try:
            palettes[palette_name] = theme.get_palette(palette_name)
        except Exception:
            pass  # Salta palette non disponibili
    
    # Ottieni tutti i colori semantici
    semantic_keys = theme.list_semantic_keys()
    semantics = {}
    for section, roles in semantic_keys.items():
        semantics[section] = {}
        for role in roles:
            try:
                color = theme.get_color(role, section=section)
                semantics[section][role] = color
            except Exception:
                pass  # Salta colori non disponibili
    
    # Ottieni tutte le sequenze
    chart_schemes = theme.list_chart_schemes()
    sequences = {}
    for scheme_type in ['sequential', 'divergent']:
        for name in chart_schemes.get(scheme_type, []):
            try:
                seq = theme.get_chart_sequence(name)
                sequences[f"{scheme_type}_{name}"] = seq
            except Exception:
                pass  # Salta sequenze non disponibili
    
    # Genera JavaScript con i dati
    palettes_js = _dict_to_js(palettes)
    semantics_js = _dict_to_js(semantics)
    sequences_js = _dict_to_js(sequences)
    
    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobility Book Design System - Color Theme</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #f9fafb 100%);
            padding: 40px 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 50px;
        }}
        
        h1 {{
            font-size: 32px;
            color: #262A33;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .subtitle {{
            font-size: 16px;
            color: #5d6b7a;
            margin-bottom: 5px;
        }}
        
        .updated {{
            font-size: 12px;
            color: #999;
            margin-top: 15px;
            font-style: italic;
        }}
        
        .theme-section {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            border-top: 4px solid #348b96;
        }}
        
        .section-title {{
            font-size: 20px;
            font-weight: 700;
            color: #262A33;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .palette-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
            gap: 12px;
            margin-bottom: 25px;
        }}
        
        .palette-section {{
            margin-bottom: 25px;
        }}
        
        .palette-name {{
            font-size: 13px;
            font-weight: 600;
            color: #262A33;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
            display: block;
        }}
        
        .color-item {{
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
        }}
        
        .color-item:hover {{
            transform: translateY(-4px);
        }}
        
        .color-box {{
            width: 100%;
            height: 70px;
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            transition: all 0.2s;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        }}
        
        .color-item:hover .color-box {{
            border-color: #348b96;
            box-shadow: 0 4px 12px rgba(52, 139, 150, 0.2);
        }}
        
        .color-code {{
            font-size: 11px;
            color: #666;
            font-family: 'Courier New', monospace;
            margin-top: 8px;
            font-weight: 500;
            letter-spacing: 0.3px;
        }}
        
        .semantic-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .semantic-section {{
            background: #f9f9f9;
            border-radius: 8px;
            padding: 15px;
        }}
        
        .semantic-section-title {{
            font-size: 12px;
            font-weight: 700;
            color: #348b96;
            text-transform: uppercase;
            margin-bottom: 12px;
            letter-spacing: 0.5px;
        }}
        
        .semantic-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }}
        
        .semantic-item:last-child {{
            margin-bottom: 0;
        }}
        
        .semantic-color-box {{
            width: 40px;
            height: 40px;
            border-radius: 6px;
            border: 1px solid #ddd;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            flex-shrink: 0;
        }}
        
        .semantic-info {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}
        
        .semantic-name {{
            font-size: 13px;
            font-weight: 500;
            color: #262A33;
        }}
        
        .semantic-code {{
            font-size: 11px;
            color: #999;
            font-family: 'Courier New', monospace;
        }}
        
        .sequence-container {{
            margin-bottom: 20px;
        }}
        
        .sequence-title {{
            font-size: 13px;
            font-weight: 600;
            color: #262A33;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .sequence-bar {{
            display: flex;
            height: 50px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border: 1px solid #e0e0e0;
        }}
        
        .sequence-segment {{
            flex: 1;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }}
        
        .sequence-segment:hover {{
            flex: 1.5;
            box-shadow: inset 0 0 0 2px rgba(255, 255, 255, 0.5);
        }}
        
        .sequence-segment::after {{
            content: attr(data-hex);
            position: absolute;
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 10px;
            color: #666;
            white-space: nowrap;
            font-family: 'Courier New', monospace;
            opacity: 0;
            transition: opacity 0.2s;
            pointer-events: none;
        }}
        
        .sequence-segment:hover::after {{
            opacity: 1;
        }}
        
        footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 1px solid #e0e0e0;
            color: #999;
            font-size: 12px;
        }}
        
        .footer-text {{
            margin-bottom: 5px;
        }}
        
        @media (max-width: 768px) {{
            h1 {{
                font-size: 24px;
            }}
            
            .theme-section {{
                padding: 20px;
            }}
            
            .palette-grid {{
                grid-template-columns: repeat(auto-fit, minmax(60px, 1fr));
            }}
            
            .semantic-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎨 Mobility Book Design System</h1>
            <p class="subtitle">Color Theme - Interactive Visualization</p>
            <p class="updated">Last updated: <span id="update-time"></span></p>
        </header>
        
        <!-- PALETTE BASE -->
        <div class="theme-section">
            <div class="section-title">
                <span>🎨</span>
                Color Palettes
            </div>
            <div id="palettes-container"></div>
        </div>
        
        <!-- COLORI SEMANTICI -->
        <div class="theme-section">
            <div class="section-title">
                <span>🎯</span>
                Semantic Colors
            </div>
            <div id="semantics-container"></div>
        </div>
        
        <!-- SEQUENZE GRAFICI -->
        <div class="theme-section">
            <div class="section-title">
                <span>📊</span>
                Chart Sequences
            </div>
            <div id="sequences-container"></div>
        </div>
        
        <footer>
            <p class="footer-text">Mobility Book Graphic Style Guide</p>
            <p class="footer-text">Generated from design tokens • Auto-updates on token changes</p>
        </footer>
    </div>
    
    <script>
        const palettes = {palettes_js};
        const semantics = {semantics_js};
        const sequences = {sequences_js};
        
        // Renderizza palette
        function renderPalettes() {{
            let html = '';
            for (const [name, colors] of Object.entries(palettes)) {{
                html += `<div class="palette-section">
                    <span class="palette-name">${{name}}</span>
                    <div class="palette-grid">`;
                colors.forEach(color => {{
                    html += `
                        <div class="color-item" title="Click to copy">
                            <div class="color-box" style="background-color: ${{color}};"></div>
                            <div class="color-code">${{color}}</div>
                        </div>`;
                }});
                html += `</div></div>`;
            }}
            document.getElementById('palettes-container').innerHTML = html;
        }}
        
        // Renderizza colori semantici
        function renderSemantics() {{
            let html = '<div class="semantic-grid">';
            for (const [section, colors] of Object.entries(semantics)) {{
                html += `<div class="semantic-section">
                    <div class="semantic-section-title">${{section}}</div>`;
                for (const [role, color] of Object.entries(colors)) {{
                    html += `
                        <div class="semantic-item">
                            <div class="semantic-color-box" style="background-color: ${{color}};"></div>
                            <div class="semantic-info">
                                <div class="semantic-name">${{role}}</div>
                                <div class="semantic-code">${{color}}</div>
                            </div>
                        </div>`;
                }}
                html += `</div>`;
            }}
            html += '</div>';
            document.getElementById('semantics-container').innerHTML = html;
        }}
        
        // Renderizza sequenze
        function renderSequences() {{
            let html = '';
            for (const [name, colors] of Object.entries(sequences)) {{
                const displayName = name.replace(/_/g, ' ').toUpperCase();
                html += `<div class="sequence-container">
                    <div class="sequence-title">${{displayName}}</div>
                    <div class="sequence-bar">`;
                colors.forEach(color => {{
                    html += `<div class="sequence-segment" style="background-color: ${{color}};" data-hex="${{color}}"></div>`;
                }});
                html += `</div></div>`;
            }}
            document.getElementById('sequences-container').innerHTML = html;
        }}
        
        // Imposta timestamp
        function updateTimestamp() {{
            const now = new Date();
            const formatted = now.toLocaleString('it-IT', {{
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            }});
            document.getElementById('update-time').textContent = formatted;
        }}
        
        // Inizializza
        renderPalettes();
        renderSemantics();
        renderSequences();
        updateTimestamp();
    </script>
</body>
</html>"""
    
    return html


def _dict_to_js(data: dict) -> str:
    """
    Converte un dizionario Python in oggetto JavaScript.
    
    Args:
        data: Dizionario da convertire
    
    Returns:
        Stringa con sintassi JavaScript object
    """
    import json
    return json.dumps(data, ensure_ascii=False)


def save_theme_html(output_path: str | Path = None) -> Path:
    """
    Genera e salva l'HTML di visualizzazione del tema.
    
    Args:
        output_path: Percorso dove salvare l'HTML.
                     Default: docs/theme-visualization.html
    
    Returns:
        Path dell'HTML salvato
    
    Esempio:
        >>> from mobility_book_style.theme_visualizer import save_theme_html
        >>> path = save_theme_html()
        >>> print(f"HTML salvato in {path}")
    """
    if output_path is None:
        output_path = Path(__file__).parent.parent / "docs" / "theme-visualization.html"
    else:
        output_path = Path(output_path)
    
    # Crea directory se non esiste
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Genera e salva HTML
    html_content = generate_theme_html()
    output_path.write_text(html_content, encoding='utf-8')
    
    return output_path
