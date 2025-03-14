# CBP CROSS Rulings Downloader

This Python script downloads data from the U.S. Customs and Border Protection (CBP) Customs Rulings Online Search System (CROSS) API and saves it to a CSV file.

## Purpose

The script is designed to overcome limitations with directly downloading large datasets from the CROSS website. It fetches data in smaller chunks using pagination and multithreading to efficiently collect rulings data.

## Requirements

*   Python 3.x
*   `requests` library: Install with `pip install requests`

## Usage

1.  **Save the script:** Save the Python code (e.g., `cbp_rulings_downloader.py`) to your local machine.
2.  **Run from the command line:**
    ```bash
    python cbp_rulings_downloader.py
    ```
3.  **Output:** The script will create a CSV file named `cbp_rulings_data.csv` (or `cbp_rulings_data_sorted.csv` if using the sorted version) in the same directory as the script. This file will contain the downloaded CROSS rulings data.

**Note:** You may need to adjust the `base_url` in the script to modify search parameters (term, date range, etc.) as needed.  Be mindful of the CBP server load and rate limits. 
