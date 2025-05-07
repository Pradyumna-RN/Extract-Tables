# PDF Table Extraction Pipeline

This project is a two-step pipeline for converting scanned PDFs into searchable PDFs and extracting tables from them into JSON format using OCR and table recognition tools.

## Features

- Converts scanned PDFs into searchable PDFs using PDF.co API
- Extracts tables from searchable PDFs using Camelot
- Saves extracted tables and metadata to structured JSON files

---

## Requirements

- Python 3.7+
- PDF.co API Key (required for OCR)
- Required Python packages:
  - `requests`
  - `camelot-py[cv]`
  - `PyMuPDF` (fitz)
  - `cryptography`

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd <your-project-directory>
