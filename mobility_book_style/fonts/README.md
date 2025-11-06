# Font Inter per Mobility Book Style

Questa cartella contiene i font **Inter** utilizzati dalla libreria Mobility Book Style.

## Font Inclusi

- `Inter-VariableFont_opsz,wght.ttf` - Font variabile (Regular, tutti i pesi)
- `Inter-Italic-VariableFont_opsz,wght.ttf` - Font variabile Italic
- `OFL.txt` - Open Font License

## Caratteristiche

I font Inter sono **font variabili** moderni che supportano:
- **Peso variabile**: da Thin (100) a Black (900)
- **Optical sizing**: ottimizzazione automatica per diverse dimensioni
- Dimensione ridotta (2 file invece di 18)
- Rendering ottimale su tutti i dispositivi

## Registrazione Automatica

I font vengono **registrati automaticamente** in Matplotlib quando importi la libreria:

```python
import mobility_book_style as mbs
# I font Inter sono ora disponibili in Matplotlib!

mbs.apply_matplotlib_theme()
# Il tema usa automaticamente Inter
```

## Licenza

Inter è rilasciato sotto **SIL Open Font License 1.1** (vedi `OFL.txt`).

Puoi:
- ✅ Usare i font commercialmente
- ✅ Modificare i font
- ✅ Distribuire i font

**Autore**: Rasmus Andersson (https://rsms.me/inter/)

## Font Fallback

Se Inter non è disponibile, il tema usa automaticamente il font stack:

```
Inter → IBM Plex Sans → DejaVu Sans → Arial → sans-serif
```

## Verifica Disponibilità

Per verificare che Inter sia stato registrato:

```python
import matplotlib.font_manager as fm

inter_fonts = [f.name for f in fm.fontManager.ttflist if 'Inter' in f.name]
print(f"Font Inter disponibili: {len(inter_fonts)}")
```

## Dimensioni File

- `Inter-VariableFont_opsz,wght.ttf`: ~855 KB
- `Inter-Italic-VariableFont_opsz,wght.ttf`: ~884 KB
- **Totale**: ~1.7 MB

(Molto più leggero rispetto ai 18 file statici che occuperebbero ~5-6 MB)

## Supporto Browser/Software

I font variabili sono supportati da:
- ✅ Tutti i browser moderni (Chrome, Firefox, Safari, Edge)
- ✅ Matplotlib (tramite FreeType)
- ✅ Adobe Creative Suite (CC 2018+)
- ✅ Microsoft Office (2016+)
- ✅ Figma, Sketch, XD

## Link Utili

- [Sito ufficiale Inter](https://rsms.me/inter/)
- [Repository GitHub](https://github.com/rsms/inter)
- [Google Fonts](https://fonts.google.com/specimen/Inter)
