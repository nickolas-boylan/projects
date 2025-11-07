#############################################################################
# ucb_scraper.py
# 
# This module implements the MainScraper for UCB's website. It only
# implements the scraping_implementation() function from the original parent
# class.
#
#############################################################################

from bs4 import BeautifulSoup
from .main_scraper import MainScraper
import re


class UcbScraper(MainScraper):
    '''
    Scraper for UCB
    '''
    def __init__(self):
        super().__init__(
            company="UCB",
            url="https://www.ucb.com/innovation/pipeline"
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

        pipeline_segments = bf_soup.find_all("div",
                                             class_="block medical-preparation")

        # Go through the pipeline segments and create the treatments
        for next_segment in pipeline_segments:
            molecule_block = next_segment.find("div",
                                class_="molecule--medical-preparation")
            
            if molecule_block:
                name_of_molecule = molecule_block.get_text(strip=True)
            else:
                name_of_molecule = ""

            more_info = next_segment.find_all("div",
                                              class_="medical-preparation-item")

            # Go through the info and create the treatment
            for info in more_info:
                therapeutic_block = info.find("div",
                                class_="therapeutic-area--medical-preparation")
                if therapeutic_block:
                    found_therapeutic = therapeutic_block.get_text(strip=True)
                else:
                    found_therapeutic = ""

                indication_block = info.find("div",
                                    class_="indication--medical-preparation")
                if indication_block:
                    found_indication = indication_block.get_text(strip=True)
                else:
                    found_indication = ""

                phase_block = info.find("div",
                    class_=re.compile(r"phases--medical-preparation phase-\d+"))
                found_phase = ""
                
                # Get the correct phase depending on class of phase block
                if phase_block:
                    if "phase-52" in phase_block.get("class", []):
                        found_phase = "Phase 2"
                    elif "phase-78" in phase_block.get("class", []):
                        found_phase = "Phase 3"
                    elif "phase-91" in phase_block.get("class", []):
                        found_phase = "Phase 4"
                    
                    found_phase = self.clean_phase(found_phase)

                final_treatments.append({
                    "company": "UCB",
                    "therapeutic_area": found_therapeutic,
                    "indication": found_indication,
                    "treatment_name": name_of_molecule,
                    "phase": found_phase
                })

        return final_treatments
            