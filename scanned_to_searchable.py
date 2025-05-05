import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageOps
import os
import glob

def preprocess_image(image_path):
    """
    Preprocesses the image to improve OCR accuracy.
    """
    # Open the image
    image = Image.open(image_path)

    # Convert to grayscale
    image = image.convert("L")

    # Apply thresholding (binarization)
    image = ImageOps.autocontrast(image)

    # Resize the image to improve clarity
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.LANCZOS)

    return image

def convert_to_searchable_pdf(input_pdf_path, output_pdf_path):
    """
    Converts a scanned PDF to a searchable PDF using Tesseract OCR.

    Args:
        input_pdf_path (str): Path to the input scanned PDF file.
        output_pdf_path (str): Path to save the searchable output PDF file.
    """
    try:
        pdf_document = fitz.open(input_pdf_path)
        pdf_writer = fitz.open()  # Create a new PDF writer object

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            
            # Render the page as an image
            pix = page.get_pixmap(dpi=300)
            image_path = f"page_{page_number + 1}.png"
            pix.save(image_path)

            # Preprocess the image
            preprocessed_image = preprocess_image(image_path)

            # Perform OCR on the preprocessed image
            custom_config = r'--oem 3 --psm 6'
            pdf_bytes = pytesseract.image_to_pdf_or_hocr(preprocessed_image, extension='pdf', config=custom_config)
            pdf_page = fitz.open("pdf", pdf_bytes)

            # Append the OCR-processed page to the new PDF
            pdf_writer.insert_pdf(pdf_page)

            # Remove the temporary image file
            os.remove(image_path)

        # Save the new searchable PDF
        pdf_writer.save(output_pdf_path)
        pdf_writer.close()
        print(f"Successfully converted '{input_pdf_path}' to searchable PDF '{output_pdf_path}'")
        return output_pdf_path
    except Exception as e:
        print(f"An error occurred while converting the PDF: {e}")
        return None

if __name__ == "__main__":
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
            output_pdf_path = f"searchable_{os.path.basename(pdf_file)}"
            convert_to_searchable_pdf(pdf_file, output_pdf_path)