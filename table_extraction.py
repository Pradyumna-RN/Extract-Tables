import camelot.io as camelot
import json
import fitz
import glob
import warnings
import os
from cryptography.utils import CryptographyDeprecationWarning

# Suppress CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

def extract_pdf_metadata(file_path):
    try:
        pdf_document = fitz.open(file_path)
        metadata = pdf_document.metadata

        if metadata:
            metadata = {"Metadata": {key: value for key, value in metadata.items() if value}}
            metadata = json.dumps(metadata, indent=4)
            print(f"Metadata for {file_path}:\n{metadata}")
        else:
            print(f"No metadata found in the PDF: {file_path}")
    except Exception as e:
        print(f"An error occurred while extracting metadata from {file_path}: {e}")

def extract_table_rows_from_pdf(file_path, pages):
    try:
        tables = camelot.read_pdf(file_path, pages=pages)
        if tables.n > 0:
            tables_data = {}
            for i, table in enumerate(tables):
                page_number = table.parsing_report['page']
                
                # Extract header
                header = table.df.iloc[0].tolist()
                header = [item.replace('\n', ',').strip() for item in header]  # Flatten header cells
                
                # Extract rows (excluding the header row) and replace '\n' with a comma
                rows = table.df.iloc[1:].values.tolist()
                flattened_rows = [cell.replace('\n', ',').strip() for row in rows for cell in row]
                
                # Store page number, header, and rows in a dictionary
                tables_data[f"Page {page_number}"] = {
                    "Header": header,
                    "Rows": flattened_rows
                }

            # Convert tables data to JSON
            tables_json = json.dumps(tables_data, indent=4)
            print(f"Extracted Table Data for {file_path}:\n{tables_json}")
            return tables_json
        else:
            print(f"No tables found on the specified pages: {pages} in {file_path}.")
            return None
    except Exception as e:
        print(f"An error occurred while extracting table rows from {file_path}: {e}")
        return None

if __name__ == "__main__":
    # Set the working directory to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # List all PDF files in the current directory
    pdf_files = glob.glob("*.pdf")
    if not pdf_files:
        print("No PDF files found in the current directory.")
    else:
        print("Available PDF files:")
        for idx, pdf_file in enumerate(pdf_files, start=1):
            print(f"{idx}. {pdf_file}")

        # Get user input for processing multiple files
        selected_files = input("Enter the numbers of the PDF files to process (comma-separated, e.g., '1,2,3'): ").strip()
        selected_files = [pdf_files[int(idx) - 1] for idx in selected_files.split(",")]

        for pdf_file in selected_files:
            print(f"\nProcessing file: {pdf_file}")
            pages = input(f"Enter the page ranges to extract tables for '{pdf_file}' (e.g., '1-3' or '1,2,3'): ").strip()
            extract_pdf_metadata(pdf_file)
            extract_table_rows_from_pdf(pdf_file, pages)