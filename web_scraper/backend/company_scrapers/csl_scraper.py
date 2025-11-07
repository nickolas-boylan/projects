#############################################################################
# csl_scraper.py
# 
# This module implements the MainScraper for CSL's website. It only
# implements the scraping_implementation() function from the original parent
# class.
#
#############################################################################

from bs4 import BeautifulSoup
from .main_scraper import MainScraper

class Cslscraper(MainScraper):
    def __init__(self):
        super().__init__(
            company="CSL",
            url="https://www.csl.com/research-and-development/product-pipeline"
        )
    
    def scraping_implementation(self):
        '''
        Function to scrape the website and parse through the response and get
        a list of treatments found
        
        Returns:
            The final list of treatments. Each treatment is a dictionary with
            the keys: 'phase', 'treatment_name', 'indication', 'company', and
            'therapeutic_area'
        '''
        found_html = self.fetch_from_file()
        self.simulate_response_delay()
        if not found_html:
            return []

        bf_soup = BeautifulSoup(found_html, "html.parser")
        final_treatments = []

        # Map for the of elements to the therapeutic area they represent
        ta_map = {
            "#03b3be": "Immunology",
            "#ce2052": "Hematology",
            "#97a81f": "Cardiovascular and Metabolic",
            "#0e56a5": "Nephrology and Transplant",
            "#f06125": "Respiratory",
            "#7030a0": "Vaccines",
            "#00a28a": "CSL Vifor",
            "#cccccc": "Outlicensed Programs",
        }

        # Page is sorted into columns of treatments at the same phase.
        # Go through each of those columns one at a time
        phase_blocks = bf_soup.find_all("div", class_="category-phase")
        for phase_block in phase_blocks:
            found_phase = phase_block.select_one("div.phase").text.strip()
            found_phase = self.clean_phase(found_phase)

            treatment_blocks = phase_block.find_all('a', class_="p-item")

            # Go through each of the treatments in the column one at a time
            for next_treatment in treatment_blocks:
                name_element = next_treatment.select_one("p.p-name")
                found_treatment_name = name_element.text.strip()
                if not found_treatment_name:
                    found_treatment_name = "N/A"

                indication_element = next_treatment.select_one("p.p-content")
                found_indication = indication_element.text.strip()
                if not found_indication:
                    found_indication = "N/A"

                found_color = next_treatment.get("data-color", 'N/A')
                found_therapeutic_area = ta_map.get(found_color, "N/A")
                if not found_therapeutic_area:
                    found_therapeutic_area = "N/A"
            
                final_treatments.append({
                    "company": "CSL",
                    "therapeutic_area": found_therapeutic_area,
                    "indication": found_indication,
                    "treatment_name": found_treatment_name,
                    "phase": found_phase
                })
                
        return final_treatments