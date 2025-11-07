#############################################################################
# xbiotech_scraper.py
# 
# This module implements the MainScraper for XBiotech's website. It only
# implements the scraping_implementation() function from the original parent
# class.
#
#############################################################################

from bs4 import BeautifulSoup
from .main_scraper import MainScraper

class XBiotechScraper(MainScraper):
    '''
    Scraper for XBiotech
    '''
    def __init__(self):
        super().__init__(
            company="XBiotech",
            url="https://www.xbiotech.com/clinical-research"
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
        
        table = bf_soup.select("div._4-column-schedule-wrapper")
        
        # Go through the table and create the treatments one by one
        for div in table:
            contents = div.contents
            
            info = contents[0].contents
            
            found_therapeutic_area = info[0].get_text(strip=True)
            found_treatment_name = info[1].get_text(strip=True)
            found_indication = info[2].get_text(strip=True)
            
            # Extract phase from the three part status bar
            phase_status_bar = contents[1].contents[0].contents[3].contents
            if len(phase_status_bar) == 1:
                phase_status_bar_block = phase_status_bar[0].contents[0].div
                phase_status_class = phase_status_bar_block['class'][0]
            else:
                phase_status_class = phase_status_bar[1]['class'][0]
            
            # Extract progress of status bar and match it to corresponding phase
            progress = phase_status_class[-3:]
            progress = progress[-2:] if progress[0] == "-" else progress
            progress = int(progress)
            
            if progress <= 33:
                found_phase = "Phase 1"
            elif progress <= 66:
                found_phase = "Phase 2"
            elif progress <= 100:
                found_phase = "Phase 3"
            else:
                found_phase = None
            found_phase = self.clean_phase(found_phase)
    
            final_treatments.append({
                "company": "XBiotech",
                "therapeutic_area": found_therapeutic_area, # Therapeutic Area
                "indication": found_indication,
                "treatment_name": found_treatment_name,
                "phase": found_phase
            })
                
        return final_treatments