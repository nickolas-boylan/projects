#############################################################################
# sanofi_scraper.py
# 
# This module implements the MainScraper for Sanofi's website. It only
# implements the scraping_implementation() function from the original parent
# class.
#
#############################################################################

from bs4 import BeautifulSoup
from .main_scraper import MainScraper

class SanofiScraper(MainScraper):
    def __init__(self):
        super().__init__(
            company="Sanofi",
            url="https://www.sanofi.com/en/our-science/our-pipeline"
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
        
        grid_sorted = bf_soup.select("div.MuiGrid2-root.MuiGrid2-container."\
            "MuiGrid2-direction-xs-row.MuiGrid2-spacing-mobile-6."\
            "MuiGrid2-spacing-tablet-6.MuiGrid2-spacing-desktop-6."\
            "css-tl9keh")
        
        # Go through all divs where each div is one treatment
        for div in grid_sorted:
            contents = div.contents
            
            therapeutic_block = contents[0].contents[0].contents[1]
            found_therapeutic_area = therapeutic_block.get_text(strip=True)
        
            phase = contents[1]
            phase_num = phase.select("div.MuiTypography-root."\
                "MuiTypography-body1.css-1kcf5u9")[0]
            phase_num = phase_num.get_text(strip=True)
            
            found_phase = "Phase " + phase_num
            found_phase = self.clean_phase(found_phase)
            
            name_block = contents[2].contents[0].contents[1]
            found_treatment_name = name_block.get_text(strip=True)
            
            indication_block = contents[6].contents[0].contents[0]
            found_indication = indication_block.get_text(strip=True)
            
            final_treatments.append({
                "company": "Sanofi",
                "therapeutic_area": found_therapeutic_area, # Therapeutic Area
                "indication": found_indication,
                "treatment_name": found_treatment_name,
                "phase": found_phase
            })
                
        return final_treatments