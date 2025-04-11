import csv
import os
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# File paths
DEALS_FILE = "temp/deals.csv"
INVESTORS_FILE = "temp/investors.csv"
OUTPUT_FILE = "data/database.csv"

# Region mapping (country to region)
REGION_MAPPING = {
    # Africa
    "Algeria": "Northern Africa",
    "Angola": "Sub-Saharan Africa",
    "Benin": "Sub-Saharan Africa",
    "Botswana": "Sub-Saharan Africa",
    "Burkina Faso": "Sub-Saharan Africa",
    "Burundi": "Sub-Saharan Africa",
    "Cabo Verde": "Sub-Saharan Africa",
    "Cameroon": "Sub-Saharan Africa",
    "Central African Republic": "Sub-Saharan Africa",
    "Chad": "Sub-Saharan Africa",
    "Comoros": "Sub-Saharan Africa",
    "Congo": "Sub-Saharan Africa",
    "Côte d'Ivoire": "Sub-Saharan Africa",
    "Democratic Republic of the Congo": "Sub-Saharan Africa",
    "Djibouti": "Sub-Saharan Africa",
    "Egypt": "Northern Africa",
    "Equatorial Guinea": "Sub-Saharan Africa",
    "Eritrea": "Sub-Saharan Africa",
    "Eswatini": "Sub-Saharan Africa",
    "Ethiopia": "Sub-Saharan Africa",
    "Gabon": "Sub-Saharan Africa",
    "Gambia": "Sub-Saharan Africa",
    "Ghana": "Sub-Saharan Africa",
    "Guinea": "Sub-Saharan Africa",
    "Guinea-Bissau": "Sub-Saharan Africa",
    "Kenya": "Sub-Saharan Africa",
    "Lesotho": "Sub-Saharan Africa",
    "Liberia": "Sub-Saharan Africa",
    "Libya": "Northern Africa",
    "Madagascar": "Sub-Saharan Africa",
    "Malawi": "Sub-Saharan Africa",
    "Mali": "Sub-Saharan Africa",
    "Mauritania": "Sub-Saharan Africa",
    "Mauritius": "Sub-Saharan Africa",
    "Morocco": "Northern Africa",
    "Mozambique": "Sub-Saharan Africa",
    "Namibia": "Sub-Saharan Africa",
    "Niger": "Sub-Saharan Africa",
    "Nigeria": "Sub-Saharan Africa",
    "Rwanda": "Sub-Saharan Africa",
    "Sao Tome and Principe": "Sub-Saharan Africa",
    "Senegal": "Sub-Saharan Africa",
    "Seychelles": "Sub-Saharan Africa",
    "Sierra Leone": "Sub-Saharan Africa",
    "Somalia": "Sub-Saharan Africa",
    "South Africa": "Sub-Saharan Africa",
    "South Sudan": "Sub-Saharan Africa",
    "Sudan": "Sub-Saharan Africa",
    "Tanzania": "Sub-Saharan Africa",
    "Togo": "Sub-Saharan Africa",
    "Tunisia": "Northern Africa",
    "Uganda": "Sub-Saharan Africa",
    "Zambia": "Sub-Saharan Africa",
    "Zimbabwe": "Sub-Saharan Africa",
    
    # Asia
    "Afghanistan": "Southern Asia",
    "Armenia": "Western Asia",
    "Azerbaijan": "Western Asia",
    "Bahrain": "Western Asia",
    "Bangladesh": "Southern Asia",
    "Bhutan": "Southern Asia",
    "Brunei": "South-East Asia",
    "Cambodia": "South-East Asia",
    "China": "Eastern Asia",
    "Cyprus": "Western Asia",
    "Georgia": "Western Asia",
    "India": "Southern Asia",
    "Indonesia": "South-East Asia",
    "Iran": "Southern Asia",
    "Iraq": "Western Asia",
    "Israel": "Western Asia",
    "Japan": "Eastern Asia",
    "Jordan": "Western Asia",
    "Kazakhstan": "Central Asia",
    "Kuwait": "Western Asia",
    "Kyrgyzstan": "Central Asia",
    "Laos": "South-East Asia",
    "Lebanon": "Western Asia",
    "Malaysia": "South-East Asia",
    "Maldives": "Southern Asia",
    "Mongolia": "Eastern Asia",
    "Myanmar": "South-East Asia",
    "Nepal": "Southern Asia",
    "North Korea": "Eastern Asia",
    "Oman": "Western Asia",
    "Pakistan": "Southern Asia",
    "Palestine": "Western Asia",
    "Philippines": "South-East Asia",
    "Qatar": "Western Asia",
    "Saudi Arabia": "Western Asia",
    "Singapore": "South-East Asia",
    "South Korea": "Eastern Asia",
    "Sri Lanka": "Southern Asia",
    "Syria": "Western Asia",
    "Taiwan": "Eastern Asia",
    "Tajikistan": "Central Asia",
    "Thailand": "South-East Asia",
    "Timor-Leste": "South-East Asia",
    "Turkey": "Western Asia",
    "Turkmenistan": "Central Asia",
    "United Arab Emirates": "Western Asia",
    "Uzbekistan": "Central Asia",
    "Vietnam": "South-East Asia",
    "Yemen": "Western Asia",
    
    # Europe
    "Albania": "Southern Europe",
    "Andorra": "Southern Europe",
    "Austria": "Western Europe",
    "Belarus": "Eastern Europe",
    "Belgium": "Western Europe",
    "Bosnia and Herzegovina": "Southern Europe",
    "Bulgaria": "Eastern Europe",
    "Croatia": "Southern Europe",
    "Czech Republic": "Eastern Europe",
    "Denmark": "Northern Europe",
    "Estonia": "Northern Europe",
    "Finland": "Northern Europe",
    "France": "Western Europe",
    "Germany": "Western Europe",
    "Greece": "Southern Europe",
    "Hungary": "Eastern Europe",
    "Iceland": "Northern Europe",
    "Ireland": "Northern Europe",
    "Italy": "Southern Europe",
    "Latvia": "Northern Europe",
    "Liechtenstein": "Western Europe",
    "Lithuania": "Northern Europe",
    "Luxembourg": "Western Europe",
    "Malta": "Southern Europe",
    "Moldova": "Eastern Europe",
    "Monaco": "Western Europe",
    "Montenegro": "Southern Europe",
    "Netherlands": "Western Europe",
    "North Macedonia": "Southern Europe",
    "Norway": "Northern Europe",
    "Poland": "Eastern Europe",
    "Portugal": "Southern Europe",
    "Romania": "Eastern Europe",
    "Russia": "Eastern Europe",
    "San Marino": "Southern Europe",
    "Serbia": "Southern Europe",
    "Slovakia": "Eastern Europe",
    "Slovenia": "Southern Europe",
    "Spain": "Southern Europe",
    "Sweden": "Northern Europe",
    "Switzerland": "Western Europe",
    "Ukraine": "Eastern Europe",
    "United Kingdom": "Northern Europe",
    "Vatican City": "Southern Europe",
    
    # Americas
    "Antigua and Barbuda": "Caribbean",
    "Argentina": "South America",
    "Bahamas": "Caribbean",
    "Barbados": "Caribbean",
    "Belize": "Central America",
    "Bolivia": "South America",
    "Brazil": "South America",
    "Canada": "Northern America",
    "Chile": "South America",
    "Colombia": "South America",
    "Costa Rica": "Central America",
    "Cuba": "Caribbean",
    "Dominica": "Caribbean",
    "Dominican Republic": "Caribbean",
    "Ecuador": "South America",
    "El Salvador": "Central America",
    "Grenada": "Caribbean",
    "Guatemala": "Central America",
    "Guyana": "South America",
    "Haiti": "Caribbean",
    "Honduras": "Central America",
    "Jamaica": "Caribbean",
    "Mexico": "Central America",
    "Nicaragua": "Central America",
    "Panama": "Central America",
    "Paraguay": "South America",
    "Peru": "South America",
    "Saint Kitts and Nevis": "Caribbean",
    "Saint Lucia": "Caribbean",
    "Saint Vincent and the Grenadines": "Caribbean",
    "Suriname": "South America",
    "Trinidad and Tobago": "Caribbean",
    "United States": "Northern America",
    "Uruguay": "South America",
    "Venezuela": "South America",
    
    # Oceania
    "Australia": "Oceania",
    "Fiji": "Oceania",
    "Kiribati": "Oceania",
    "Marshall Islands": "Oceania",
    "Micronesia": "Oceania",
    "Nauru": "Oceania",
    "New Zealand": "Oceania",
    "Palau": "Oceania",
    "Papua New Guinea": "Oceania",
    "Samoa": "Oceania",
    "Solomon Islands": "Oceania",
    "Tonga": "Oceania",
    "Tuvalu": "Oceania",
    "Vanuatu": "Oceania"
}

def extract_year(text):
    """Extract the year from a text string."""
    if not text:
        return None
    
    # Look for a 4-digit year
    year_match = re.search(r'\b(19\d{2}|20\d{2})\b', text)
    if year_match:
        return year_match.group(1)
    
    return None

def extract_crops(text):
    """Extract crop information from text."""
    if not text:
        return []
    
    # Common crops to look for
    common_crops = [
        "Rice", "Wheat", "Corn", "Maize", "Soybean", "Sugarcane", "Cotton", 
        "Coffee", "Tea", "Cocoa", "Palm oil", "Rubber", "Jatropha", "Cassava",
        "Potato", "Sweet potato", "Banana", "Plantain", "Mango", "Pineapple",
        "Orange", "Lemon", "Lime", "Grapefruit", "Apple", "Grape", "Strawberry",
        "Blueberry", "Raspberry", "Blackberry", "Watermelon", "Melon", "Papaya",
        "Avocado", "Coconut", "Olive", "Sunflower", "Rapeseed", "Canola", "Sesame",
        "Peanut", "Groundnut", "Cashew", "Almond", "Walnut", "Pecan", "Pistachio",
        "Hazelnut", "Macadamia", "Chestnut", "Tomato", "Pepper", "Chili", "Eggplant",
        "Cucumber", "Zucchini", "Squash", "Pumpkin", "Carrot", "Onion", "Garlic",
        "Leek", "Cabbage", "Lettuce", "Spinach", "Kale", "Broccoli", "Cauliflower",
        "Asparagus", "Celery", "Radish", "Turnip", "Beet", "Pea", "Bean", "Lentil",
        "Chickpea", "Sorghum", "Millet", "Barley", "Oat", "Rye", "Quinoa", "Teff",
        "Flax", "Hemp", "Tobacco", "Vanilla", "Cinnamon", "Clove", "Nutmeg", "Ginger",
        "Turmeric", "Cardamom", "Cumin", "Coriander", "Fennel", "Anise", "Basil",
        "Oregano", "Rosemary", "Thyme", "Sage", "Mint", "Lavender", "Rose", "Jasmine",
        "Chrysanthemum", "Tulip", "Lily", "Orchid", "Carnation", "Sunflower", "Daisy",
        "Poppy", "Bamboo", "Teak", "Mahogany", "Eucalyptus", "Pine", "Spruce", "Fir",
        "Cedar", "Oak", "Maple", "Birch", "Willow", "Poplar", "Acacia", "Baobab",
        "Pulses", "Legumes"
    ]
    
    found_crops = []
    for crop in common_crops:
        if re.search(r'\b' + re.escape(crop) + r'\b', text, re.IGNORECASE):
            found_crops.append(crop)
    
    return found_crops[:3]  # Return up to 3 crops

def get_investor_details(investor_id, investors_data):
    """Get investor details from the investors data."""
    if not investor_id or investor_id not in investors_data:
        return None, None, None
    
    investor = investors_data[investor_id]
    name = investor.get('Name', '')
    country = investor.get('Country', '')
    classification = investor.get('Classification', '')
    
    # Get region from country
    region = REGION_MAPPING.get(country, '')
    
    # Determine sector based on classification
    sector = "Unknown"
    if classification:
        if any(term in classification.lower() for term in ['agriculture', 'farm', 'food']):
            sector = "Agriculture"
        elif any(term in classification.lower() for term in ['energy', 'power', 'electricity']):
            sector = "Energy"
        elif any(term in classification.lower() for term in ['finance', 'bank', 'investment']):
            sector = "Finance"
        elif any(term in classification.lower() for term in ['mining', 'mineral']):
            sector = "Mining"
        elif any(term in classification.lower() for term in ['state', 'government']):
            sector = "Government"
        else:
            sector = "Private"
    
    return name, country, region, sector

def process_data():
    """Process the deals and investors data to create the database file."""
    try:
        # Check if input files exist
        if not os.path.exists(DEALS_FILE):
            logger.error(f"Deals file not found: {DEALS_FILE}")
            return False
        
        if not os.path.exists(INVESTORS_FILE):
            logger.error(f"Investors file not found: {INVESTORS_FILE}")
            return False
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        
        logger.info("Reading investors data...")
        # Read investors data into a dictionary
        investors_data = {}
        with open(INVESTORS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            headers = next(reader)  # Skip header row
            
            for row in reader:
                if len(row) >= 3:  # Ensure we have at least ID, Name, and Country
                    investor_id = row[0].strip()
                    investors_data[investor_id] = {
                        'Name': row[1].strip() if len(row) > 1 else '',
                        'Country': row[2].strip() if len(row) > 2 else '',
                        'Classification': row[3].strip() if len(row) > 3 else ''
                    }
        
        logger.info(f"Loaded {len(investors_data)} investors")
        
        logger.info("Reading deals data...")
        # Process deals data
        output_data = []
        with open(DEALS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            headers = next(reader)  # Get header row
            
            # Find indices of relevant columns
            try:
                deal_id_idx = headers.index('Deal ID')
                target_country_idx = headers.index('Target country')
                size_idx = headers.index('Deal size')
                intention_idx = headers.index('Intention of investment')
                operating_company_id_idx = headers.index('Operating company: Investor ID')
                year_info_idx = headers.index('Current size under contract')  # This might contain year info
                
                # These might not exist in all files
                investor_chain_idx = -1
                if 'Top parent companies' in headers:
                    investor_chain_idx = headers.index('Top parent companies')
                
                crops_idx = -1
                if 'Crops area/yield/export' in headers:
                    crops_idx = headers.index('Crops area/yield/export')
                
            except ValueError as e:
                logger.error(f"Error finding required columns: {e}")
                return False
            
            for row in reader:
                if len(row) <= max(deal_id_idx, target_country_idx, size_idx, intention_idx, operating_company_id_idx):
                    continue  # Skip incomplete rows
                
                deal_id = row[deal_id_idx].strip()
                target_country = row[target_country_idx].strip()
                
                # Get target region from country
                target_region = REGION_MAPPING.get(target_country, '')
                
                # Extract size (hectares)
                hectares = ''
                if row[size_idx]:
                    try:
                        hectares = float(row[size_idx].replace(',', '.'))
                    except ValueError:
                        pass
                
                # Extract year
                year = ''
                if year_info_idx >= 0 and year_info_idx < len(row):
                    year = extract_year(row[year_info_idx])
                
                # Extract crops
                crops = []
                if crops_idx >= 0 and crops_idx < len(row):
                    crops = extract_crops(row[crops_idx])
                
                # Get investor information
                investor_ids = []
                
                # Primary investor (operating company)
                if operating_company_id_idx < len(row) and row[operating_company_id_idx]:
                    investor_ids.append(row[operating_company_id_idx].strip())
                
                # Additional investors from the chain
                if investor_chain_idx >= 0 and investor_chain_idx < len(row) and row[investor_chain_idx]:
                    # Parse investor chain (format might be like "Company1#ID1#Country1,Company2#ID2#Country2")
                    investor_chain = row[investor_chain_idx].strip()
                    for investor_info in investor_chain.split(','):
                        parts = investor_info.split('#')
                        if len(parts) >= 2 and parts[1].strip():
                            investor_id = parts[1].strip()
                            if investor_id not in investor_ids:
                                investor_ids.append(investor_id)
                
                # Get details for up to 3 investors
                investors = []
                investor_countries = []
                investor_regions = []
                investor_sectors = []
                
                for i, inv_id in enumerate(investor_ids[:3]):
                    name, country, region, sector = get_investor_details(inv_id, investors_data)
                    investors.append(name or '')
                    investor_countries.append(country or '')
                    investor_regions.append(region or '')
                    investor_sectors.append(sector or '')
                
                # Pad lists to ensure 3 elements
                investors.extend([''] * (3 - len(investors)))
                investor_countries.extend([''] * (3 - len(investor_countries)))
                investor_regions.extend([''] * (3 - len(investor_regions)))
                investor_sectors.extend([''] * (3 - len(investor_sectors)))
                crops.extend([''] * (3 - len(crops)))
                
                # Create output row
                output_row = {
                    'Deal Number': deal_id,
                    'Target Country': target_country,
                    'Target Region': target_region,
                    'Investor 1': investors[0],
                    'Investor 2': investors[1],
                    'Investor 3': investors[2],
                    'Investor Country 1': investor_countries[0],
                    'Investor Country 2': investor_countries[1],
                    'Investor Country 3': investor_countries[2],
                    'Investor Region 1': investor_regions[0],
                    'Investor Region 2': investor_regions[1],
                    'Investor Region 3': investor_regions[2],
                    'Inv. Sector 1': investor_sectors[0],
                    'Inv. Sector 2': investor_sectors[1],
                    'Inv. Sector 3': investor_sectors[2],
                    'Crop 1': crops[0],
                    'Crop 2': crops[1],
                    'Crop 3': crops[2],
                    'Year': year or '',
                    'Hectares': hectares
                }
                
                output_data.append(output_row)
        
        logger.info(f"Processed {len(output_data)} deals")
        
        # Write to output file
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Write header
            header = [
                'Deal Number', 'Target Country', 'Target Region',
                'Investor 1', 'Investor 2', 'Investor 3',
                'Investor Country 1', 'Investor Country 2', 'Investor Country 3',
                'Investor Region 1', 'Investor Region 2', 'Investor Region 3',
                'Inv. Sector 1', 'Inv. Sector 2', 'Inv. Sector 3',
                'Crop 1', 'Crop 2', 'Crop 3', 'Year', 'Hectares'
            ]
            writer.writerow(header)
            
            # Write data rows
            for row in output_data:
                writer.writerow([row[col] for col in header])
        
        logger.info(f"Successfully created database file: {OUTPUT_FILE}")
        return True
    
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        return False

if __name__ == "__main__":
    process_data()
