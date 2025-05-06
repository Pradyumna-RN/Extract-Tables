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
    """
    Extracts metadata from a PDF file.
    """
    try:
        pdf_document = fitz.open(file_path)
        metadata = pdf_document.metadata

        if metadata:
            metadata = {key: value for key, value in metadata.items() if value}
            #print(f"Metadata for {file_path}:\n{json.dumps(metadata, indent=4)}")
            return metadata
        else:
            print(f"No metadata found in the PDF: {file_path}")
            return {}
    except Exception as e:
        print(f"An error occurred while extracting metadata from {file_path}: {e}")
        return {}

def extract_table_rows_from_pdf(file_path, pages, output_json_path):
    """
    Extracts tables from a PDF file and saves the data to a JSON file.
    """
    try:
        tables = camelot.read_pdf(file_path, pages=pages)
        output_data = {}

        if tables.n > 0:
            tables_data = {}
            for i, table in enumerate(tables):
                page_number = table.parsing_report['page']

                # Extract header and remove blank values
                header = table.df.iloc[0].tolist()
                header = [item.replace('\n', ',').strip() for item in header if item.strip()]  # Remove blank values

                # Extract rows (excluding the header row), replace '\n' with a comma, and remove blank values
                rows = table.df.iloc[1:].values.tolist()
                flattened_rows = [
                    [cell.replace('\n', ',').strip() for cell in row if cell.strip()] for row in rows
                ]

                # Store page number, header, and rows in a dictionary
                tables_data[f"Page {page_number}"] = {
                    "Header": header,
                    "Rows": flattened_rows
                }

            # Add tables data to the output JSON
            output_data["Tables"] = tables_data
        else:
            print(f"No tables found on the specified pages: {pages} in {file_path}.")
            output_data["Tables"] = {}

        # Save tables data and metadata to a JSON file
        with open(output_json_path, "w", encoding="utf-8") as json_file:
            json.dump(output_data, json_file, indent=4)
        print(f"Extracted table data saved to {output_json_path}")
        return output_data
    except Exception as e:
        print(f"An error occurred while extracting table rows from {file_path}: {e}")
        return None

if __name__ == "__main__":
    # Set the working directory to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Ensure the output folder exists
    output_folder = os.path.join(script_dir, "output")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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

            # Extract metadata
            metadata = extract_pdf_metadata(pdf_file)

            # Extract table rows and save to JSON
            output_json_path = os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}_tables.json")
            output_data = extract_table_rows_from_pdf(pdf_file, pages, output_json_path)

            # Add metadata to the JSON file
            if output_data is not None:
                output_data["Metadata"] = metadata
                with open(output_json_path, "w", encoding="utf-8") as json_file:
                    json.dump(output_data, json_file, indent=4)
                print(f"Metadata added to {output_json_path}")