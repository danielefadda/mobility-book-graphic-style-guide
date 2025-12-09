"""Loader dei design token con accesso dot-notation.

Questo modulo è l'unica fonte di verità per i token. Legge il file
``design_tokens.json``, risolve i riferimenti (es. ``{color.base.teal.500}``)
e restituisce:

- ``token``: oggetto navigabile via dot-notation, che restituisce i valori.
- ``token_dict``: dizionario Python con i soli valori risolti.
- ``token_raw``: dizionario con il contenuto originale del JSON (inclusi type/description).

I token sono dati puri: nessuna logica di applicazione o trasformazione viene
esposta qui. La logica di consumo resta nei moduli ``matplotlib.py`` e
``altair.py``.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping

TOKEN_JSON_PATH = Path(__file__).parent / "data" / "design_tokens.json"


class TokenNode:
    """Nodo navigabile che restituisce valori con dot-notation."""

    def __init__(self, data: Any, path: tuple[str, ...] | None = None):
        self._data = data
        self._path = path or ()

    def __getattr__(self, name: str) -> Any:
        if isinstance(self._data, Mapping) and name in self._data:
            child = self._data[name]
            return child if _is_leaf(child) else TokenNode(child, (*self._path, name))
        raise AttributeError(f"Token '{'.'.join(self._path)}' non contiene '{name}'")

    def __getitem__(self, key: Any) -> Any:
        if isinstance(self._data, Mapping):
            child = self._data[key]
            return child if _is_leaf(child) else TokenNode(child, (*self._path, str(key)))
        if isinstance(self._data, list):
            child = self._data[key]
            return child if _is_leaf(child) else TokenNode(child, (*self._path, str(key)))
        raise TypeError("Token leaf non indicizzabile")

    def __iter__(self):
        if isinstance(self._data, Mapping):
            return iter(self._data)
        if isinstance(self._data, list):
            return iter(self._data)
        raise TypeError("Token leaf non iterabile")

    def __len__(self) -> int:
        if isinstance(self._data, Mapping):
            return len(self._data)
        if isinstance(self._data, list):
            return len(self._data)
        raise TypeError("Token leaf non ha lunghezza")

    def keys(self):
        if isinstance(self._data, Mapping):
            return self._data.keys()
        raise TypeError("Token leaf non ha chiavi")

    def values(self):
        if isinstance(self._data, Mapping):
            return self._data.values()
        raise TypeError("Token leaf non ha valori")

    def items(self):
        if isinstance(self._data, Mapping):
            return self._data.items()
        raise TypeError("Token leaf non ha coppie")

    def __repr__(self) -> str:  # pragma: no cover - solo per debug
        return f"TokenNode({self._path or 'root'}={self._data!r})"

    def to_dict(self) -> Any:
        """Restituisce i dati Python sottostanti (primitives, dict, list)."""
        return self._data


def _is_leaf(value: Any) -> bool:
    return not isinstance(value, (Mapping, list))


def _load_raw_tokens() -> dict:
    if not TOKEN_JSON_PATH.exists():
        raise FileNotFoundError(
            f"File design_tokens.json non trovato: {TOKEN_JSON_PATH}\n"
            "Assicurati che il file esista in mobility_book_style/data/"
        )

    try:
        return json.loads(TOKEN_JSON_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover - error path
        raise json.JSONDecodeError(
            f"File design_tokens.json malformato: {exc.msg} (linea {exc.lineno}, colonna {exc.colno})",
            exc.doc,
            exc.pos,
        )


def _resolve_reference(path_str: str, raw_tree: dict, cache: dict[str, Any]) -> Any:
    """Risolvi una stringa nel formato {a.b.c}."""
    ref_match = re.fullmatch(r"\{([^}]+)\}", path_str)
    if not ref_match:
        return path_str

    path_parts = ref_match.group(1).split(".")
    cache_key = "::".join(path_parts)
    if cache_key in cache:
        return cache[cache_key]

    current: Any = raw_tree
    for part in path_parts:
        current = current[part]

    resolved = _resolve_node(current, raw_tree, cache)
    cache[cache_key] = resolved
    return resolved


def _resolve_node(node: Any, raw_tree: dict, cache: dict[str, Any]) -> Any:
    if isinstance(node, Mapping):
        if "value" in node and len(node) >= 1:
            return _resolve_reference(node["value"], raw_tree, cache)
        return {k: _resolve_node(v, raw_tree, cache) for k, v in node.items()}
    if isinstance(node, list):
        return [_resolve_node(item, raw_tree, cache) for item in node]
    if isinstance(node, str):
        return _resolve_reference(node, raw_tree, cache)
    return node


def _extract_values(raw_tree: dict) -> dict:
    cache: dict[str, Any] = {}
    return _resolve_node(raw_tree, raw_tree, cache)


# Carica e prepara i token
token_raw: dict = _load_raw_tokens()
token_dict: dict = _extract_values(token_raw)
token = TokenNode(token_dict)

__all__ = ["token", "token_dict", "token_raw", "TokenNode"]
