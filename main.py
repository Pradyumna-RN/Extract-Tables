import os
import subprocess
import fitz  # PyMuPDF
import camelot.io as camelot
import json
import requests  # pip install requests
import warnings
from cryptography.utils import CryptographyDeprecationWarning
import config
# Suppress CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

# The authentication key (API Key).
# Get your own by registering at https://app.pdf.co
API_KEY = config.API_KEY

# Base URL for PDF.co Web API requests
BASE_URL = "https://api.pdf.co/v1"

# Comma-separated list of page indices (or ranges) to process. Leave empty for all pages. Example: '0,2-5,7-'.
Pages = ""
# PDF document password. Leave empty for unprotected documents.
Password = ""
# OCR language. "eng", "fra", "deu", "spa" supported currently. Let us know if you need more.
Language = "eng"


def is_scanned_pdf(file_path):
    """
    Determines if a PDF file is scanned by checking for text content.
    Returns True if the PDF is scanned, otherwise False.
    """
    try:
        with fitz.open(file_path) as pdf_document:
            for page in pdf_document:
                if page.get_text().strip():
                    return False
            return True

        
        
        # pdf_document = fitz.open(file_path)
        # for page in pdf_document:
        #     if page.get_text().strip():  # Check if the page contains text
        #         return False
        # return True  # No text found, it's a scanned PDF
    
    
    
    except Exception as e:
        print(f"An error occurred while checking if the PDF is scanned: {e}")
        return False


def make_searchable_pdf(source_file, destination_file):
    """
    Converts a scanned PDF to a searchable PDF using PDF.co API.
    """
    try:
        # Upload the file
        uploaded_file_url = upload_file(source_file)
        if uploaded_file_url is not None:
            # Prepare request parameters
            parameters = {
                "name": os.path.basename(destination_file),
                "password": Password,
                "pages": Pages,
                "lang": Language,
                "url": uploaded_file_url,
            }

            # Make the PDF searchable
            url = f"{BASE_URL}/pdf/makesearchable"
            response = requests.post(url, data=parameters, headers={"x-api-key": API_KEY})
            if response.status_code == 200:
                json_response = response.json()
                if not json_response["error"]:
                    result_file_url = json_response["url"]
                    # Download the result file
                    download_file(result_file_url, destination_file)
                    print(f"Searchable PDF saved as: {destination_file}")
                else:
                    print(f"Error: {json_response['message']}")
            else:
                print(f"Request failed: {response.status_code} {response.reason}")
    except Exception as e:
        print(f"An error occurred while making the PDF searchable: {e}")


def upload_file(file_name):
    """
    Uploads a file to PDF.co and returns the file URL.
    """
    try:
        url = f"{BASE_URL}/file/upload/get-presigned-url?contenttype=application/octet-stream&name={os.path.basename(file_name)}"
        response = requests.get(url, headers={"x-api-key": API_KEY})
        if response.status_code == 200:
            json_response = response.json()
            if not json_response["error"]:
                upload_url = json_response["presignedUrl"]
                uploaded_file_url = json_response["url"]
                with open(file_name, "rb") as file:
                    requests.put(upload_url, data=file, headers={"content-type": "application/octet-stream"})
                return uploaded_file_url
            else:
                print(f"Error: {json_response['message']}")
        else:
            print(f"Request failed: {response.status_code} {response.reason}")
    except Exception as e:
        print(f"An error occurred while uploading the file: {e}")
    return None


def download_file(url, destination_file):
    """
    Downloads a file from a given URL.
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destination_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        print(f"Failed to download file: {response.status_code} {response.reason}")


def extract_pdf_metadata(file_path):
    """
    Extracts metadata from a PDF file.
    """
    try:
        pdf_document = fitz.open(file_path)
        metadata = pdf_document.metadata
        return {key: value for key, value in metadata.items() if value} if metadata else {}
    except Exception as e:
        print(f"An error occurred while extracting metadata from {file_path}: {e}")
        return {}


def extract_table_rows_from_pdf(file_path, pages, output_json_path):
    """
    Extracts tables from a PDF file and saves the data to a JSON file.
    """
    try:
        pdf_document = fitz.open(file_path)  # Open the PDF file
        tables = camelot.read_pdf(file_path, pages=pages)
        output_data = {"Tables": {}}

        if tables.n > 0:
            for i, table in enumerate(tables):
                page_number = table.parsing_report["page"]
                header = table.df.iloc[0].tolist()
                header = [item.replace("\n", ",").strip() for item in header if item.strip()]
                rows = table.df.iloc[1:].values.tolist()
                flattened_rows = [[cell.replace("\n", ",").strip() for cell in row if cell.strip()] for row in rows]
                output_data["Tables"][f"Page {page_number}"] = {"Header": header, "Rows": flattened_rows}

            with open(output_json_path, "w", encoding="utf-8") as json_file:
                json.dump(output_data, json_file, indent=4)
            print(f"Extracted table data saved to {output_json_path}")
        else:
            print(f"No tables found on the specified pages: {pages} in {file_path}.")
    except Exception as e:
        print(f"An error occurred while extracting table rows from {file_path}: {e}")
    finally:
        pdf_document.close()  # Ensure the file is closed


if __name__ == "__main__":
    # Set the working directory to the 'input' folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, "input")
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    # List all PDF files in the input folder
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]
    if not pdf_files:
        print("No PDF files found in the 'input' folder.")
        exit(1)

    # Display the list of PDF files
    print("Available PDF files:")
    for idx, pdf_file in enumerate(pdf_files, start=1):
        print(f"{idx}. {pdf_file}")

    # Prompt the user to select specific files or a range of files
# Prompt the user to select specific files or a range of files
    try:
        selection = input(
            f"Enter the file numbers to process ('1-3' for a range, or '1,3,5' for multiple files): "
        ).strip()

        # Parse the selection
        selected_files = []
        if "-" in selection:
            start, end = map(int, selection.split("-"))
            if start < 1 or end > len(pdf_files) or start > end:
                print("Invalid range of files selected.")
                exit(1)
            selected_files.extend(pdf_files[start - 1 : end])
        elif "," in selection:
            file_numbers = map(int, selection.split(","))
            for file_number in file_numbers:
                if file_number < 1 or file_number > len(pdf_files):
                    print(f"Invalid file number selected: {file_number}")
                    exit(1)
                selected_files.append(pdf_files[file_number - 1])
        else:
            file_number = int(selection)
            if file_number < 1 or file_number > len(pdf_files):
                print("Invalid file number selected.")
                exit(1)
            selected_files.append(pdf_files[file_number - 1])
    except ValueError:
        print("Invalid input. Please enter a valid file number, range, or list of numbers.")
        exit(1)

    # Process the selected files
    for pdf_file in selected_files:
        selected_file_path = os.path.join(input_dir, pdf_file)
        print(f"\nProcessing file: {selected_file_path}")

        # Check if the selected file is scanned
        if is_scanned_pdf(selected_file_path):
            print(f"The file '{pdf_file}' is scanned. Converting to searchable PDF...")
            searchable_file_path = os.path.join(input_dir, f"{os.path.splitext(pdf_file)[0]}_searchable.pdf")
            make_searchable_pdf(selected_file_path, searchable_file_path)
            selected_file_path = searchable_file_path  # Update the path to the searchable file

        # Extract tables from the PDF
        print(f"Extracting tables from '{selected_file_path}'...")
        pages = input(f"Enter the page ranges to extract tables for '{pdf_file}' (e.g., '1-3' or '1,2,3'): ").strip()
        output_json_path = os.path.join(output_dir, f"{os.path.splitext(pdf_file)[0]}_tables.json")
        metadata = extract_pdf_metadata(selected_file_path)
        extract_table_rows_from_pdf(selected_file_path, pages, output_json_path)

        # Add metadata to the JSON file
        if os.path.exists(output_json_path):
            with open(output_json_path, "r+", encoding="utf-8") as json_file:
                data = json.load(json_file)
                data["Metadata"] = metadata
                json_file.seek(0)
                json.dump(data, json_file, indent=4)
                json_file.truncate()
            print(f"Metadata added to {output_json_path}")