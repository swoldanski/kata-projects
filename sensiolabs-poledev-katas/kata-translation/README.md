# Kata 5: Manage Translations

Source: https://github.com/devdrops/Katas/tree/kata-translation

## Problem

Build a translation management system for multi-language applications.

## Goals

- Store translations by locale and key
- Support pluralization
- Fallback chains (fr_CA → fr → en)
- Variable interpolation
- Date/number formatting per locale
- Import/export (XLIFF, JSON, CSV, PO)

## Features

1. **Message catalog**: locale → key → translation
2. **Plural forms**: ICU MessageFormat or custom
3. **Fallback**: hierarchical locale fallback
4. **Interpolation**: {name}, {count, plural, ...}
5. **Formatters**: date, time, number, currency per locale
6. **Extraction**: scan code for translation keys
7. **Management UI**: add/edit/delete translations

## Examples

```python
# Translation management
tm = TranslationManager()
tm.set_translation("en", "greeting", "Hello {name}!")
tm.set_translation("fr", "greeting", "Bonjour {name}!")
tm.set_translation("es", "greeting", "¡Hola {name}!")

tm.translate("greeting", "fr", name="Marie")  # => "Bonjour Marie!"
tm.translate("greeting", "de", name="Hans")   # => "Hello Hans!" (fallback to en)
```

## Exercises

1. Basic key/locale lookup
2. Pluralization rules (CLDR)
3. Fallback chain
4. Variable interpolation
5. Date/number formatting
6. XLIFF import/export
7. Translation extraction from source
8. Missing key detection
9. Context/notes for translators