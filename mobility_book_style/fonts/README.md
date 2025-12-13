# Font Inter per Mobility Book Style

Questa cartella contiene i font **Inter** utilizzati dalla libreria Mobility Book Style.

## Font Inclusi

Solo variante `Inter_18pt-*.ttf` (tutti i pesi e stili), più `OFL.txt`.

## Caratteristiche

I font Inter statici garantiscono piena compatibilità con Matplotlib e rendono
correttamente i pesi (es. Bold) senza problemi legati ai Variable Fonts.

La libreria usa **Inter 18pt** come font family predefinito, ottimale per grafici
e visualizzazioni a dimensioni standard.

## Registrazione Automatica

I font vengono **registrati automaticamente** in Matplotlib quando importi la libreria (solo statici):

```python
import mobility_book_style as mbs
	# I font Inter sono ora disponibili in Matplotlib!

	mbs.apply_matplotlib_theme()
	# Il tema usa automaticamente "Inter 18pt"
```

## Licenza

Inter è rilasciato sotto **SIL Open Font License 1.1** (vedi `OFL.txt`).

Puoi:
- ✅ Usare i font commercialmente
- ✅ Modificare i font
- ✅ Distribuire i font

**Autore**: Rasmus Andersson (https://rsms.me/inter/)

## Font Fallback

Se Inter 18pt non è disponibile, il tema usa automaticamente il font stack:

```
Inter 18pt → sans-serif
```

## Verifica Disponibilità

Per verificare che Inter sia stato registrato:

```python
import matplotlib.font_manager as fm

inter_fonts = [f.name for f in fm.fontManager.ttflist if 'Inter' in f.name]
print(f"Font Inter disponibili: {len(inter_fonts)}")
# Dovresti vedere ~54 font (Inter 18pt, 24pt, 28pt con tutti i pesi)
```

## Dimensioni File

- 54 font statici totali (18pt, 24pt, 28pt × 9 pesi × 2 stili)
- **Totale**: ~9-10 MB

Nota: Più pesante dei variable fonts (~1.7 MB), ma garantisce compatibilità
con Matplotlib e rendering corretto dei pesi.

## Supporto Browser/Software

- ✅ Matplotlib (tramite FreeType)
- ✅ Tutti i browser moderni (con CSS @font-face)
- ✅ Adobe Creative Suite (CC 2018+)
- ✅ Microsoft Office (2016+)
- ✅ Figma, Sketch, XD

## Link Utili

- [Sito ufficiale Inter](https://rsms.me/inter/)
- [Repository GitHub](https://github.com/rsms/inter)
- [Google Fonts](https://fonts.google.com/specimen/Inter)
