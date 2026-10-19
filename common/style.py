"""Paleta y fondo del taller. Cada scene.py llama a `apply()` justo después de los imports."""

import manimgx as m

BG = "#0B0B14"  # fondo casi negro
CYAN = "#3FD7E8"
MAGENTA = "#E04FB6"
AMBER = "#F5B342"
INK = "#D9DCE8"  # texto
DIM = "#5A6078"  # líneas y elementos secundarios

TITLE_SIZE = 32
TEXT_SIZE = 24


def apply() -> None:
    """Pone el fondo del taller."""
    m.config.background_color = BG
