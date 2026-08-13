"""
PDF file handler.

Handles reading PDF files using pypdf.
Single Responsibility: PDF file I/O only.
"""

from pathlib import Path

import pypdf


class PDFHandler:
    """
    Handler for PDF files.

    Uses pypdf to extract text content from PDF documents.
    """

    @classmethod
    def can_handle(cls, file_path: Path) -> bool:
        """
        Check if this handler can process the given file.

        Args:
            file_path: Path to check

        Returns:
            True if file is a PDF
        """
        return file_path.suffix.lower() == ".pdf"

    @staticmethod
    def read(file_path: Path) -> str:
        """
        Read PDF file content.

        Extracts text from all pages and concatenates with page markers.

        Args:
            file_path: Path to PDF file

        Returns:
            Extracted text content

        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file can't be read
            pypdf.errors.PdfReadError: If PDF is corrupted or encrypted
        """
        with open(file_path, "rb") as pdf_file:
            reader = pypdf.PdfReader(pdf_file)

            # Check if PDF is encrypted
            if reader.is_encrypted:
                raise PermissionError("PDF is encrypted and cannot be read")

            # Extract text from all pages
            text_content = []
            for page_num, page in enumerate(reader.pages, 1):
                text_content.append(f"--- Page {page_num} ---\n")
                page_text = page.extract_text()
                text_content.append(page_text)
                text_content.append("\n")

            return "".join(text_content)

    @staticmethod
    def get_info(file_path: Path) -> dict:
        """
        Get information about a PDF file.

        Args:
            file_path: Path to PDF file

        Returns:
            Dictionary with PDF information
        """
        stat = file_path.stat()

        try:
            with open(file_path, "rb") as pdf_file:
                reader = pypdf.PdfReader(pdf_file)
                page_count = len(reader.pages)
                is_encrypted = reader.is_encrypted

                # Try to get metadata
                metadata = reader.metadata
                if metadata:
                    title = metadata.get("/Title", "Unknown")
                    author = metadata.get("/Author", "Unknown")
                else:
                    title = author = "Unknown"
        except Exception:
            page_count = None
            is_encrypted = None
            title = author = "Unknown"

        return {
            "type": "pdf",
            "extension": ".pdf",
            "size_bytes": stat.st_size,
            "pages": page_count,
            "encrypted": is_encrypted,
            "title": title,
            "author": author,
        }

    @staticmethod
    def extract_page(file_path: Path, page_number: int) -> str:
        """
        Extract text from a specific page.

        Args:
            file_path: Path to PDF file
            page_number: Page number (1-indexed)

        Returns:
            Text from the specified page

        Raises:
            IndexError: If page number is out of range
        """
        with open(file_path, "rb") as pdf_file:
            reader = pypdf.PdfReader(pdf_file)

            if page_number < 1 or page_number > len(reader.pages):
                raise IndexError(f"Page {page_number} out of range (1-{len(reader.pages)})")

            page = reader.pages[page_number - 1]  # Convert to 0-indexed
            return page.extract_text()
