import requests
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Any

locations = [
    "ASUCLA",
    "Berkeley",
    "Davis",
    "UC SF Law",
    "Irvine",
    "Los Angeles",
    "Merced",
    "Riverside",
    "San Diego",
    "San Francisco",
    "Santa Barbara",
    "Santa Cruz",
    "UCOP",
]

years = [
    2024,
    2023,
    2022,
    2021,
    2020,
    2019,
    2018,
    2017,
    2016,
    2015,
    2014,
    2013,
    2012,
    2011,
    2010,
]

SCRAPE_LINK = "https://ucannualwage.ucop.edu/wage/search"


class UCWageScraper:
    def __init__(self, delay: float = 0.5):
        """
        Initialize the UC Wage Scraper

        Args:
            delay: Delay between requests in seconds to avoid overwhelming the server
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            }
        )

    def create_search_payload(
        self, location: str, year: int, page: int = 1, rows: int = 100
    ) -> Dict[str, Any]:
        """
        Create the search payload for the API request

        Args:
            location: UC campus location
            year: Year to search
            page: Page number for pagination
            rows: Number of rows per page (max seems to be 100)

        Returns:
            Dictionary payload for the API request
        """
        return {
            "op": "search",
            "page": page,
            "rows": rows,
            "sidx": "lastname",
            "sord": "asc",
            "count": 0,
            "year": str(year),
            "firstname": "",
            "location": location,
            "lastname": "",
            "title": "",
            "startSal": "",
            "endSal": "",
        }

    def fetch_page(self, location: str, year: int, page: int = 1) -> Dict[str, Any]:
        """
        Fetch a single page of wage data

        Args:
            location: UC campus location
            year: Year to search
            page: Page number

        Returns:
            API response as dictionary
        """
        payload = self.create_search_payload(location, year, page)

        try:
            response = self.session.post(SCRAPE_LINK, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {location} {year} page {page}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for {location} {year} page {page}: {e}")
            return None

    def fetch_all_pages(self, location: str, year: int) -> List[Dict[str, Any]]:
        """
        Fetch all pages of wage data for a specific location and year

        Args:
            location: UC campus location
            year: Year to search

        Returns:
            List of all employee records
        """
        all_records = []
        page = 1

        while True:
            print(f"  Fetching page {page} for {location} {year}...")
            data = self.fetch_page(location, year, page)

            if not data:
                break

            # Check if we have records
            if "rows" not in data or not data["rows"]:
                break

            records = data["rows"]
            all_records.extend(records)

            # Check if we've fetched all records
            total_records = data.get("records", 0)
            if len(all_records) >= total_records or len(records) == 0:
                break

            page += 1
            time.sleep(self.delay)  # Rate limiting

        return all_records

    def save_data(self, location: str, year: int, data: List[Dict[str, Any]]) -> None:
        """
        Save scraped data to JSON file in location-specific directory

        Args:
            location: UC campus location
            year: Year of the data
            data: List of employee records
        """
        # Create directory for the location if it doesn't exist
        location_dir = location.replace(" ", "_").replace("/", "_")
        os.makedirs(location_dir, exist_ok=True)

        # Create filename
        filename = f"{location_dir}/wages_{year}.json"

        # Save data with metadata
        output_data = {
            "location": location,
            "year": year,
            "scraped_at": datetime.now().isoformat(),
            "total_records": len(data),
            "records": data,
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"  Saved {len(data)} records to {filename}")

    def scrape_location_year(self, location: str, year: int) -> bool:
        """
        Scrape wage data for a specific location and year

        Args:
            location: UC campus location
            year: Year to scrape

        Returns:
            True if successful, False otherwise
        """
        print(f"Scraping {location} for year {year}...")

        try:
            data = self.fetch_all_pages(location, year)

            if data:
                self.save_data(location, year, data)
                print(
                    f"  Successfully scraped {len(data)} records for {location} {year}"
                )
                return True
            else:
                print(f"  No data found for {location} {year}")
                return False

        except Exception as e:
            print(f"  Error scraping {location} {year}: {e}")
            return False

    def scrape_all(
        self, locations_to_scrape: List[str] = None, years_to_scrape: List[int] = None
    ) -> None:
        """
        Scrape all wage data for specified locations and years

        Args:
            locations_to_scrape: List of locations to scrape (default: all locations)
            years_to_scrape: List of years to scrape (default: all years)
        """
        if locations_to_scrape is None:
            locations_to_scrape = locations
        if years_to_scrape is None:
            years_to_scrape = years

        total_combinations = len(locations_to_scrape) * len(years_to_scrape)
        current = 0
        successful = 0
        failed = 0

        print(f"Starting scrape of {total_combinations} location-year combinations")
        print("=" * 60)

        for location in locations_to_scrape:
            for year in years_to_scrape:
                current += 1
                print(f"\n[{current}/{total_combinations}] ", end="")

                if self.scrape_location_year(location, year):
                    successful += 1
                else:
                    failed += 1

                # Longer delay between different requests
                time.sleep(self.delay * 2)

        print("\n" + "=" * 60)
        print(f"Scraping complete!")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")
        print(f"  Total: {total_combinations}")


def main():
    """Main function to run the scraper"""
    print("UC Wage Data Scraper")
    print("=" * 60)

    # Initialize scraper with 1 second delay between requests
    scraper = UCWageScraper(delay=1.0)

    # Option to scrape specific locations or years
    # Uncomment and modify as needed:
    # scraper.scrape_all(locations_to_scrape=["Berkeley", "Los Angeles"], years_to_scrape=[2024, 2023])

    # Scrape all locations and years
    scraper.scrape_all()


if __name__ == "__main__":
    main()
