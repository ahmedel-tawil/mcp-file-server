"""Handlers package for file type processing."""

from .pdf_handler import PDFHandler
from .text_handler import TextHandler

__all__ = [
    "PDFHandler",
    "TextHandler",
]
