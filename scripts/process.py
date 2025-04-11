import requests
from zipfile import ZipFile
import os
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Base URL for the Land Matrix API
BASE_URL = "https://landmatrix.org/api/legacy_export/"

# Default parameters for the API request
DEFAULT_PARAMS = {
    "subset": "PUBLIC",
    "area_min": "200",
    "negotiation_status": ["ORAL_AGREEMENT", "CONTRACT_SIGNED", "CHANGE_OF_OWNERSHIP"],
    "nature": ["OUTRIGHT_PURCHASE", "LEASE", "CONCESSION", "EXPLOITATION_PERMIT"],
    "initiation_year_min": "2000",
    "initiation_year_null": "t",
    "intention_of_investment": [
        "BIOFUELS", "BIOMASS_ENERGY_GENERATION", "FODDER", "FOOD_CROPS", "LIVESTOCK",
        "NON_FOOD_AGRICULTURE", "AGRICULTURE_UNSPECIFIED", "BIOMASS_ENERGY_PRODUCTION",
        "CARBON", "FOREST_LOGGING", "TIMBER_PLANTATION", "FORESTRY_UNSPECIFIED",
        "SOLAR_PARK", "WIND_FARM", "RENEWABLE_ENERGY", "CONVERSATION", "INDUSTRY",
        "LAND_SPECULATION", "TOURISM", "OTHER"
    ],
    "transnational": "true",
    "forest_concession": "false",
    "format": "csv"
}

# Files to extract from the zip
TARGET_FILES = ["deals.csv", "investors.csv"]

# Function to build the URL with parameters
def build_url(params=None):
    """Build the URL with the given parameters."""
    if params is None:
        params = DEFAULT_PARAMS

    # Convert list parameters to multiple URL parameters with the same name
    encoded_params = []
    for key, value in params.items():
        if isinstance(value, list):
            for item in value:
                encoded_params.append((key, item))
        else:
            encoded_params.append((key, value))

    query_string = '&'.join(f"{k}={v}" for k, v in encoded_params)
    return f"{BASE_URL}?{query_string}"


def download_and_extract(url=None, target_dir="temp", target_files=None):
    """Download the zip file from the URL and extract only the target files."""
    if url is None:
        url = build_url()

    if target_files is None:
        target_files = TARGET_FILES

    # Create target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        logger.info(f"Created directory: {target_dir}")

    # Temporary file to store the downloaded zip
    zip_path = os.path.join(target_dir, "export.zip")

    try:
        # Download the file
        logger.info(f"Downloading from: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Save the zip file
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        logger.info(f"Downloaded zip file to: {zip_path}")

        # Extract only the target files
        with ZipFile(zip_path, 'r') as zip_ref:
            all_files = zip_ref.namelist()
            logger.info(f"Files in zip: {all_files}")

            for file in all_files:
                if file in target_files:
                    zip_ref.extract(file, target_dir)
                    logger.info(f"Extracted: {file} to {target_dir}")

        # Remove the zip file after extraction (optional)
        os.remove(zip_path)
        logger.info("Removed temporary zip file")

        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading file: {e}")
        return False
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return False


def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description='Download and extract files from Land Matrix API')
    parser.add_argument('--url', help='Custom URL to download from (optional)')
    parser.add_argument('--dir', default='temp', help='Directory to save extracted files (default: temp)')
    args = parser.parse_args()

    url = args.url if args.url else build_url()
    success = download_and_extract(url, args.dir)

    if success:
        logger.info(f"Successfully extracted target files to {args.dir}")
    else:
        logger.error("Failed to download and extract files")
        exit(1)


if __name__ == "__main__":
    main()