import os
import subprocess

def run_scanned_to_searchable():
    num=input("Enter 0 to skip scanned_to_scearchable.py or 1 to run: ")

    """
    Runs the scanned_to_scearchable.py script to convert scanned PDFs to searchable PDFs.
    """
    if num!="0":
        print("Running scanned_to_scearchable.py...")
        try:
            subprocess.run(["python", "scanned_to_scearchable.py"], check=True)
            print("scanned_to_scearchable.py completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running scanned_to_scearchable.py: {e}")
            exit(1)

def run_table_extraction():
    """
    Runs the table_extraction.py script to extract tables from searchable PDFs.
    """
    print("Running table_extraction.py...")
    try:
        subprocess.run(["python", "table_extraction.py"], check=True)
        print("table_extraction.py completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running table_extraction.py: {e}")
        exit(1)

if __name__ == "__main__":
    # Step 1: Run scanned_to_scearchable.py
    run_scanned_to_searchable()

    # Step 2: Run table_extraction.py
    run_table_extraction()