import os
import requests  # pip install requests

# The authentication key (API Key).
# Get your own by registering at https://app.pdf.co
API_KEY = "jamesmay2663@gmail.com_ovvnFpdr6zq3xtmY6EPlqRWbV9WXtVvGB9JIBF3AwfIKtZIbX1jHEwUv0rakxYlM"

# Base URL for PDF.co Web API requests
BASE_URL = "https://api.pdf.co/v1"

# Comma-separated list of page indices (or ranges) to process. Leave empty for all pages. Example: '0,2-5,7-'.
Pages = ""
# PDF document password. Leave empty for unprotected documents.
Password = ""
# OCR language. "eng", "fra", "deu", "spa" supported currently. Let us know if you need more.
Language = "eng"
# Destination PDF file name
DestinationFile = ".\\digital.pdf"


def main(args=None):
    # List all PDF files in the current directory
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    if not pdf_files:
        print("No PDF files found in the current directory.")
        return

    print("Available PDF files:")
    for idx, pdf_file in enumerate(pdf_files, start=1):
        print(f"{idx}. {pdf_file}")

    # Prompt the user to select a file
    selected_idx = int(input("Enter the number of the PDF file to process: ")) - 1
    if selected_idx < 0 or selected_idx >= len(pdf_files):
        print("Invalid selection.")
        return

    # Get the selected file
    SourceFile = pdf_files[selected_idx]
    print(f"Selected file: {SourceFile}")

    # Upload the selected file and make it searchable
    uploadedFileUrl = uploadFile(SourceFile)
    if uploadedFileUrl is not None:
        makeSearchablePDF(uploadedFileUrl, DestinationFile)


def makeSearchablePDF(uploadedFileUrl, destinationFile):
    """Make Uploaded PDF file Searchable using PDF.co Web API"""

    # Prepare requests params as JSON
    # See documentation: https://apidocs.pdf.co
    parameters = {}
    parameters["name"] = os.path.basename(destinationFile)
    parameters["password"] = Password
    parameters["pages"] = Pages
    parameters["lang"] = Language
    parameters["url"] = uploadedFileUrl

    # Prepare URL for 'Make Searchable PDF' API request
    url = f"{BASE_URL}/pdf/makesearchable"

    # Execute request and get response as JSON
    response = requests.post(url, data=parameters, headers={"x-api-key": API_KEY})
    if response.status_code == 200:
        json = response.json()

        if not json["error"]:
            # Get URL of result file
            resultFileUrl = json["url"]
            # Download result file
            r = requests.get(resultFileUrl, stream=True)
            if r.status_code == 200:
                with open(destinationFile, 'wb') as file:
                    for chunk in r:
                        file.write(chunk)
                print(f"Result file saved as \"{destinationFile}\" file.")
            else:
                print(f"Request error: {response.status_code} {response.reason}")
        else:
            # Show service-reported error
            print(json["message"])
    else:
        print(f"Request error: {response.status_code} {response.reason}")


def uploadFile(fileName):
    """Uploads file to the cloud"""

    # 1. RETRIEVE PRESIGNED URL TO UPLOAD FILE.

    # Prepare URL for 'Get Presigned URL' API request
    url = f"{BASE_URL}/file/upload/get-presigned-url?contenttype=application/octet-stream&name={os.path.basename(fileName)}"

    # Execute request and get response as JSON
    response = requests.get(url, headers={"x-api-key": API_KEY})
    if response.status_code == 200:
        json = response.json()

        if not json["error"]:
            # URL to use for file upload
            uploadUrl = json["presignedUrl"]
            # URL for future reference
            uploadedFileUrl = json["url"]

            # 2. UPLOAD FILE TO CLOUD.
            with open(fileName, 'rb') as file:
                requests.put(uploadUrl, data=file, headers={"x-api-key": API_KEY, "content-type": "application/octet-stream"})

            return uploadedFileUrl
        else:
            # Show service-reported error
            print(json["message"])
    else:
        print(f"Request error: {response.status_code} {response.reason}")

    return None


if __name__ == '__main__':
    main()