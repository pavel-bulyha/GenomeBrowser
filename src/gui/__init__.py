"""
GenomeBrowser gui пакет.
Содержит диалоги выбора файла и виджеты для интерфейса.
"""

from .dialogs import ask_open_filename
from .widgets import create_controls, create_canvas, create_sequence_text

__all__ = [
    "ask_open_filename",
    "create_controls",
    "create_canvas",
    "create_sequence_text",
]
