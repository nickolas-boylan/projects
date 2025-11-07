#############################################################################
# mitsubishi_scraper.py
# 
# This module implements the MainScraper for Mitsubishi's website. It only
# implements the scraping_implementation() function from the original parent
# class.
#
#############################################################################

from bs4 import BeautifulSoup
from .main_scraper import MainScraper

class MitsubishiScraper(MainScraper):
    '''
    Scraper for Mitsubishi
    '''
    def __init__(self):
        super().__init__(
            company="Mitsubishi",
            url="https://www.mt-pharma.co.jp/e/develop/pipeline.html"
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
        
        table = bf_soup.select("div.pipeline-body__item." +
                               "pipeline-body__item--toggle")
        
        # Go through the table parse the treatments one by one
        for div in table:
            contents = div.contents
            main_info = contents[1].contents
            
            found_therapeutic_area = main_info[1].get_text(strip=True)
            found_indication = main_info[5].get_text(strip=True)
            
            # Get the phase from the name of the field's class
            phase = main_info[7].contents[1].contents[1].contents[1]['class'][1]
            phase_id = int(phase[-1])
            if phase_id == 1:
                found_phase = "Phase 1"
            elif phase_id == 2 or phase_id == 3:
                found_phase = "Phase 2"
            elif phase_id == 4 or phase_id == 5:
                found_phase = "Phase 3"
            elif phase_id == 6:
                found_phase = "Filed"
            else:
                found_phase = None
            
            found_phase = self.clean_phase(found_phase)
            
            name_block = contents[3].contents[1].contents[1].contents[3]
            found_treatment_name = name_block.get_text(strip=True)
    
            final_treatments.append({
                "company": "Mitsubishi",
                "therapeutic_area": found_therapeutic_area, # Therapeutic Area
                "indication": found_indication,
                "treatment_name": found_treatment_name,
                "phase": found_phase
            })
                
        return final_treatments