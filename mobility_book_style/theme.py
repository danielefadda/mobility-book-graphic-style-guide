from typing import List, Dict, Literal, Union, Any
from ._tokens import token

"""
Modulo Theme: Helper per accedere ai design tokens in modo semplice e intuitivo.

Fornisce funzioni per:
- Ottenere palette di colori (reversed, sequenziali, categorici)
- Accedere a colori semantici
- Configurazioni font pronte all'uso
- Liste di introspezione per scoprire le opzioni disponibili
"""

PaletteName = Literal["teal", "burgundy", "purple", "olive", "gold", "slate", "rust", "neutral"]
SemanticRole = Literal["primary", "secondary", "link", "exercise", "warning", "definition", "curiosity"]
FontType = Literal["sans", "mono"]

def get_palette(name: PaletteName, reverse: bool = False) -> List[str]:
    """
    Restituisce una lista ordinata di codici esadecimali per una scala colore base.
    Gestisce l'ordinamento numerico delle chiavi (50, 100, ... 900) che nel JSON sono stringhe.
    
    Args:
        name: Nome della palette (teal, burgundy, purple, olive, gold, slate, rust, neutral)
        reverse: Se True, inverte l'ordine della palette
    
    Returns:
        Lista di colori hex ordinati dal più chiaro al più scuro (o viceversa se reverse=True)
    
    Esempio:
        >>> colors = get_palette('teal')
        >>> # ['#a4f8ff', '#8ee2ed', ..., '#002a34']
    """
    try:
        # Accediamo al nodo del colore (es. token.color.base.teal)
        color_node = getattr(token.color.base, name)
        
        # Convertiamo in dizionario per manipolarlo
        if hasattr(color_node, 'to_dict'):
            raw_dict = color_node.to_dict()
        else:
            raw_dict = dict(color_node) if not isinstance(color_node, dict) else color_node
        
        sorted_keys = sorted(
            [k for k in raw_dict.keys() if k.isdigit()],
            key=lambda x: int(x)
        )
        
        # Estrai i valori hex gestendo sia TokenNode che dict semplici
        hex_values = []
        for k in sorted_keys:
            val = raw_dict[k]
            if isinstance(val, dict) and "value" in val:
                hex_values.append(val["value"])
            elif hasattr(val, 'value'):
                hex_values.append(val.value)
            else:
                hex_values.append(str(val))
        
        if reverse:
            return hex_values[::-1]
        return hex_values
        
    except (AttributeError, KeyError) as e:
        raise ValueError(f"Palette '{name}' non trovata in token.color.base: {e}")

def get_color(role: SemanticRole, section: str = "brand") -> str:
    """
    Recupera rapidamente un singolo colore semantico senza navigare tutto l'albero.
    
    Args:
        role: Ruolo semantico (primary, secondary, link, exercise, warning, definition, curiosity)
        section: Sezione del token (brand, intent, text, background)
    
    Returns:
        Stringa hex del colore
    
    Esempi:
        >>> primary = get_color('primary')  # Shortcut per primary del brand
        >>> exercise = get_color('exercise', section='intent')
    """
    # Mapping rapido per i casi d'uso più comuni
    shortcuts = {
        "primary": token.color.brand.primary,
        "accent": token.color.brand.accent,
        "text_primary": token.color.text.primary,
        "text_secondary": token.color.text.secondary,
        "link": token.color.text.link,
        "exercise": token.color.intent.exercise,
        "warning": token.color.intent.warning,
        "definition": token.color.intent.definition,
        "curiosity": token.color.intent.curiosity,
    }
    
    # Se il ruolo è nelle scorciatoie, lo ritorniamo, altrimenti proviamo a navigare
    if role in shortcuts:
        val = shortcuts[role]
        return val.value if hasattr(val, 'value') else val
    
    # Fallback generico
    try:
        section_node = getattr(token.color, section)
        role_node = getattr(section_node, role)
        val = role_node.value if hasattr(role_node, 'value') else role_node
        return val
    except AttributeError:
        raise ValueError(f"Colore semantico {section}.{role} non trovato.")

def get_font_props(family: FontType = "sans", size: str = "m", weight: str = "regular") -> Dict[str, Union[str, int]]:
    """
    Restituisce un dizionario di proprietà font pronto per essere passato a matplotlib
    o usato come kwargs.
    
    Args:
        family: Famiglia di font (sans, mono)
        size: Dimensione (xs, s, m, l, xl, xxl)
        weight: Peso (regular, medium, bold)
    
    Returns:
        Dizionario con chiavi 'family', 'size', 'weight'.
        La chiave 'size' contiene un numero intero (punti), adatto per matplotlib.
    
    Esempio:
        >>> title_font = get_font_props(size='xl', weight='bold')
        >>> # {'family': 'Inter...', 'size': 12, 'weight': '700'}
    """
    try:
        family_val = getattr(token.font.family, family)
        size_val = getattr(token.font.size, size)
        weight_val = getattr(token.font.weight, weight)
        
        # Estrai i valori raw
        family_str = family_val.value if hasattr(family_val, 'value') else family_val
        size_str = size_val.value if hasattr(size_val, 'value') else size_val
        weight_str = weight_val.value if hasattr(weight_val, 'value') else weight_val
        
        # Converti size da "12pt" a numero intero
        if isinstance(size_str, str) and size_str.endswith('pt'):
            size_num = int(size_str[:-2])  # rimuovi "pt" e converti a int
        else:
            size_num = int(size_str) if size_str else 10
        
        return {
            "family": family_str,
            "size": size_num,
            "weight": weight_str,
        }
    except AttributeError as e:
        raise ValueError(f"Font prop non trovato (family={family}, size={size}, weight={weight}): {e}")

def get_chart_sequence(name: str = "teal") -> List[str]:
    """
    Restituisce la sequenza specifica definita per i grafici (token.chart.sequential).
    Utile perché questa potrebbe differire dalla palette base in futuro.
    
    Args:
        name: Nome della scala sequenziale (teal, burgundy, neutral, ecc.)
    
    Returns:
        Lista di colori hex ordinati per il grafico
    
    Esempio:
        >>> colors = get_chart_sequence('rust')
    """
    try:
        seq_node = getattr(token.color.chart.sequential, name)
        
        # Ordiniamo per chiave numerica 1..11
        if hasattr(seq_node, 'to_dict'):
            raw_dict = seq_node.to_dict()
        else:
            raw_dict = dict(seq_node) if not isinstance(seq_node, dict) else seq_node
        
        sorted_keys = sorted(
            [k for k in raw_dict.keys() if k.isdigit()],
            key=lambda x: int(x)
        )
        
        result = []
        for k in sorted_keys:
            val = raw_dict[k]
            hex_color = val["value"] if isinstance(val, dict) and "value" in val else (val.value if hasattr(val, 'value') else str(val))
            result.append(hex_color)
        return result
    except (AttributeError, KeyError) as e:
        raise ValueError(f"Sequenza grafico '{name}' non trovata: {e}")

# --- HELPERS DI INTROSPEZIONE (Liste complete) ---

def list_palettes() -> List[str]:
    """
    Restituisce la lista dei nomi delle scale di colore disponibili.
    Esempio: ['neutral', 'teal', 'burgundy', 'purple', ...]
    """
    # token.color.base è un TokenNode, usiamo .keys() per ottenere i nomi
    return list(token.color.base.keys())

def list_semantic_keys() -> Dict[str, List[str]]:
    """
    Restituisce un dizionario con tutte le chiavi semantiche disponibili,
    raggruppate per sezione (brand, intent, text).
    """
    return {
        "brand": list(token.color.brand.keys()),
        "intent": list(token.color.intent.keys()),
        "text": list(token.color.text.keys()),
        "background": list(token.color.background.keys())
    }

def list_chart_schemes() -> Dict[str, List[str]]:
    """
    Restituisce le opzioni disponibili per i grafici:
    sequenziali, categorici e divergenti.
    """
    return {
        "sequential": list(token.color.chart.sequential.keys()),
        "categorical": list(token.color.chart.categorical.keys()) if hasattr(token.color.chart, 'categorical') else [],
        "divergent": list(token.color.chart.divergent.keys())
    }

def list_font_sizes() -> List[str]:
    """
    Restituisce i nomi delle dimensioni di font disponibili.
    """
    return list(token.font.size.keys())

def list_font_weights() -> List[str]:
    """
    Restituisce i nomi dei pesi di font disponibili.
    """
    return list(token.font.weight.keys())

def list_fonts() -> List[str]:
    """
    Restituisce i nomi delle famiglie di font disponibili.
    """
    return list(token.font.family.keys())

def print_theme_summary():
    """
    Stampa un riepilogo leggibile di tutto il tema disponibile.
    Molto utile nei Notebook per avere un riferimento rapido.
    """
    print(f"--- MOBILITY BOOK DESIGN SYSTEM ---\n")
    
    palettes = list_palettes()
    print(f"🎨 PALETTE BASE ({len(palettes)}):")
    print(f"   {', '.join(palettes)}")
    print(f"   💡 Uso: get_palette('teal') → lista di colori hex")
    print(f"   💡 Uso: get_palette('teal', reverse=True) → invertita")
    
    print(f"\n🎯 SEMANTICA:")
    semantics = list_semantic_keys()
    for section, keys in semantics.items():
        print(f"   • {section.capitalize()}: {', '.join(keys)}")
    print(f"   💡 Uso: get_color('primary') oppure get_color('exercise', section='intent')")
        
    print(f"\n📊 GRAFICI:")
    charts = list_chart_schemes()
    print(f"   • Sequenziali: {', '.join(charts['sequential'])}")
    print(f"   • Divergenti: {', '.join(charts['divergent'])}")
    print(f"   💡 Uso: get_chart_sequence('rust')")
    
    print(f"\n🔤 FONT:")
    fonts = list_fonts()
    sizes = list_font_sizes()
    weights = list_font_weights()
    print(f"   • Famiglie: {', '.join(fonts)}")
    print(f"   • Dimensioni: {', '.join(sizes)}")
    print(f"   • Pesi: {', '.join(weights)}")
    print(f"   💡 Uso: get_font_props(size='xl', weight='bold')")

def get_icon_grid() -> Dict[str, List[str]]:
    """
    Restituisce una griglia leggibile di tutte le opzioni disponibili
    nel tema, organizzate per categoria.
    """
    return {
        "palettes": list_palettes(),
        "semantics": list_semantic_keys(),
        "charts": list_chart_schemes(),
        "fonts": list_fonts(),
        "sizes": list_font_sizes(),
        "weights": list_font_weights(),
    }