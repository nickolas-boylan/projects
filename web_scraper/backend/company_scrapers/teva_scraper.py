#############################################################################
# Teva_scraper.py
# 
# This module implements the MainScraper for Teva's website. It only
# implements the scraping_implementation() function from the original parent
# class.
#
#############################################################################

from bs4 import BeautifulSoup
from .main_scraper import MainScraper

class TevaScraper(MainScraper):
    def __init__(self):
        super().__init__(
            company="Teva",
            url="https://www.tevapharm.com/product-focus/research/pipeline"
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
        found_html = self.fetch_with_zyte()
        if not found_html:
            return []

        bf_soup = BeautifulSoup(found_html, "html.parser")
        final_treatments = []
        
        phases_sorted = bf_soup.select("h3.mt-60")
        
        # Go through all the treatment for each of the phase groups
        for phase_heading in phases_sorted:
            found_indication = ""
            
            found_phase = phase_heading.get_text(strip=True)
            found_phase = self.clean_phase(found_phase)
            
            treatments = phase_heading.find_next_sibling("div").select("div."\
                "vi-accordion-pipeline__header.vi-accordion__header")
            
            # Go through all treatments in the current phase
            for treatment in treatments:
                contents = treatment.contents
                
                name_block = contents[1].contents[1]
                found_treatment_name = name_block.get_text(strip=True)
                
                tags = contents[3].contents
                found_therapeutic_area = tags[1].get_text(strip=True)
                
                if (len(tags) > 3):
                    found_indication = tags[3].get_text(strip=True)
                else:
                    found_indication = "N/A"
    
                final_treatments.append({
                    "company": "Teva",
                    "therapeutic_area": found_therapeutic_area, # Color tag
                    "indication": found_indication,
                    "treatment_name": found_treatment_name,
                    "phase": found_phase
                })
                
        return final_treatments