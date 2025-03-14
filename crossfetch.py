import requests
import csv
import time
import threading
import concurrent.futures
import json 

def fetch_page_data(url, page_num, all_data, lock):
    """Fetches data for a single page from the API and handles JSON response."""
    page_url = url.replace("&page=1", f"&page={page_num}")  # Dynamically set page number
    print(f"Fetching page {page_num} from: {page_url}")
    try:
        response = requests.get(page_url)
        response.raise_for_status()  
        json_data = response.json() # Parse JSON response

        if not json_data or 'rulings' not in json_data or not json_data['rulings']:
            print(f"Page {page_num} is empty or 'rulings' key not found. Stopping page fetching.")
            return False
        rulings = json_data['rulings']
        page_data = []
        for ruling in rulings:
            # Flatten the ruling data and handle lists like 'tariffs'
            row = {
                'id': ruling.get('id'),
                'rulingNumber': ruling.get('rulingNumber'),
                'subject': ruling.get('subject'),
                'categories': ruling.get('categories'),
                'rulingDate': ruling.get('rulingDate'),
                'isUsmca': ruling.get('isUsmca'),
                'isNafta': ruling.get('isNafta'),
                'collection': ruling.get('collection'),
                'relatedRulings': ', '.join(ruling.get('relatedRulings', [])),
                'modifiedBy': ', '.join(ruling.get('modifiedBy', [])),
                'modifies': ', '.join(ruling.get('modifies', [])),
                'revokedBy': ', '.join(ruling.get('revokedBy', [])),
                'revokes': ', '.join(ruling.get('revokes', [])),  
                'tariffs': ', '.join(ruling.get('tariffs', [])), 
            }
            page_data.append(row)


        with lock:
            if not all_data: 
                if page_data: 
                    all_data.append(list(page_data[0].keys()))
            for row_dict in page_data:
                all_data.append(list(row_dict.values())) 
        print(f"Page {page_num} fetched and {len(page_data)} rulings added.")
        return True 

    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_num}: {e}")
        return False 
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from page {page_num}: {e}")
        print(f"Response text was: {response.text}") # Print response text for debugging
        return False 


def main():
    base_url = "https://rulings.cbp.gov/api/search?term=a*&collection=ALL&fromDate=1980-01-01&toDate=2025-03-14&pageSize=100&page=1&sortBy=DATE_DESC&format=json" # Correct format=json

    all_data = [] # List to store all data rows (will include header)
    lock = threading.Lock() # Lock for thread-safe access to all_data
    page_num = 1
    pages_to_fetch = 2162 # value for full data set (216170//10 + 1)
    fetched_pages = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor: # Adjust max_workers as needed
        futures = []
        continue_fetching = True

        while continue_fetching and (pages_to_fetch is None or fetched_pages < pages_to_fetch):
            future = executor.submit(fetch_page_data, base_url, page_num, all_data, lock)
            futures.append(future)
            page_num += 1
            fetched_pages += 1

        # Wait for all futures to complete and check if any page returned empty to stop overall fetching
        for future in concurrent.futures.as_completed(futures):
            if future.result() == False: 
                continue_fetching = False
                break 

    # Write all data to a CSV file
    if all_data and len(all_data) > 1: 
        output_filename = "cbp_rulings_data.csv"
        print(f"Writing data to {output_filename}...")
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(all_data)
        print(f"Data saved to {output_filename}")
    else:
        print("No data fetched or no rulings found.")


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Script execution time: {end_time - start_time:.2f} seconds")
