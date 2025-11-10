"""Handlers package for file type processing."""

from .text_handler import TextHandler
from .pdf_handler import PDFHandler

__all__ = [
    'TextHandler',
    'PDFHandler',
]
