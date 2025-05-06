import os
import subprocess

def run_scanned_to_searchable():
    """
    Runs the scanned_to_searchable.py script to convert scanned PDFs to searchable PDFs.
    """
    # Set the working directory to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print("Running scanned_to_searchable.py...")
    try:
        # Run scanned_to_searchable.py without listing files
        subprocess.run(
            ["python", "scanned_to_searchable.py"],
            cwd=script_dir,
            check=True
        )
        print("scanned_to_searchable.py completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running scanned_to_searchable.py: {e}")
        exit(1)

def run_table_extraction():
    """
    Runs the table_extraction.py script to extract tables from searchable PDFs.
    """
    print("Running table_extraction.py...")
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.run(["python", "table_extraction.py"], cwd=script_dir, check=True)
        print("table_extraction.py completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running table_extraction.py: {e}")
        exit(1)

if __name__ == "__main__":
    # Step 1: Run scanned_to_searchable.py
    num = input("Enter 0 to skip scanned_to_searchable.py or 1 to run: ").strip()
    if num == "1":
        run_scanned_to_searchable()
    elif num == "0":
        print("Skipping scanned_to_searchable.py...")
    else:
        print("Invalid input. Skipping scanned_to_searchable.py...")

    # Step 2: Run table_extraction.py
    run_table_extraction()