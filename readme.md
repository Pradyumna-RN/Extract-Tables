Scanned PDF to Searchable PDF and Table Extraction
This project provides a solution to convert scanned PDFs into searchable PDFs using Tesseract OCR and extract table headers and rows from the searchable PDFs using Camelot.

Features
Convert Scanned PDFs to Searchable PDFs:

Uses Tesseract OCR to add searchable text to scanned PDFs.
Includes advanced preprocessing for improved OCR accuracy.
Extract Table Data:

Extracts table headers and rows from searchable PDFs using Camelot.
Extract Metadata:
Extracts metadata from the PDF file.
Make sure you have the following installed:

Python 3.x

Required Python packages:

bash
Copy
Edit
pip install requests camelot-py[cv] PyMuPDF cryptography
A PDF.co API key, which you'll need to set in a file called config.py:

python
Copy
Edit
# config.py
API_KEY = "your_pdfco_api_key"

## How to Build and Test

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd detect-tables-pdf
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   - You may need to install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and [poppler](http://blog.alivate.com.au/poppler-windows/) for pdf2image.
3. **Add your PDFs:**
   - Place all PDFs to process in the `input/` folder.
4. **Run the script:**
   ```bash
   python main.py
   ```
5. **Check results:**
   - Results will be in `output/results.csv` and `output/results.json`.

## Security
- No hardcoded credentials or PII.
- Use of `.gitignore` to exclude sensitive/config files.
- Apache 2.0 License included.

## Acceptance Criteria
- Working code, robust to both digital and scanned PDFs.
- Accurate table and title extraction with fallback logic.
- Output in both CSV and JSON formats.
- Clear documentation and licensing.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/detect-tables-pdf.git
cd detect-tables-pdf
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

The tool can be used through a command-line interface with the following options:
