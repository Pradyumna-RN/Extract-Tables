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

Steps to Run the Project
Place PDF Files
Put the scanned PDF files you want to process into the same folder as the Python scripts.

Run the main script

python main.py

When prompted:
Type 1 to convert a scanned PDF to a searchable one.

Choose a PDF file number from the list that appears.

Once conversion is done, the script will proceed to extract tables from PDFs.

Select the files and page ranges as prompted.

Output
Searchable PDFs are saved in the same directory with _searchable.pdf suffix.

Extracted tables + metadata are saved as JSON files in the output folder.
