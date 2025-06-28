#############################################################################
# bayer_scraper.py
# 
# This module implements the MainScraper for Bayer's website. It only
# implements the scraping_implementation() function from the original parent
# class.
#
#############################################################################

from bs4 import BeautifulSoup
from .main_scraper import MainScraper
import re

class BayerScraper(MainScraper):
    '''
    Scraper for Bayer
    '''
    def __init__(self):
        super().__init__(
            company="Bayer",
            url="https://www.bayer.com/en/pharma/development-pipeline"
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

        ta_dict = {}

        # Parse through the html code to find the table of treatments
        mydiv = bf_soup.find("div", {"class": "field field--name-field-left"\
            "-sidebar-contents field--type-entity-reference-revisions"\
            " field--label-hidden field__items"})

        myrows = mydiv.find_all("tr")
        for row in myrows:
            initial_row = row.text
            ta_dict[initial_row] = initial_row
        
        found_treatments = bf_soup.find_all("tr")

        # Go through each treatment in the html code and create the treatment
        # dictionary for it
        for next_row in found_treatments:
            found_cells = next_row.find_all('td')

            # ignore rows that don't have the right number of cells
            if len(found_cells) >= 4:
                phase = found_cells[0].get_text(strip=True)
                therapeutic_area = found_cells[1].get_text(strip=True)
                treatment_name = found_cells[2].get_text(strip=True)
                indication = found_cells[3].get_text()

                phase = self.update_phase(phase)
                indication = self.update_indication(indication)
                therapeutic_area = self.update_therapeutic(therapeutic_area,
                                                           ta_dict)
                treatment_name = self.update_treatment_name(treatment_name)

                phase = self.clean_phase(phase)

                final_treatments.append({
                    "company": "Bayer",
                    "therapeutic_area": therapeutic_area,
                    "indication": indication,
                    "treatment_name": treatment_name,
                    "phase": phase
                })

        return final_treatments

    def update_treatment_name(self, treatment_name):
        '''
        Clean up the treatment_name
        
        Arguments:
            treatment_name: The original string containing the treatment name
        '''
        return treatment_name.split('\n')[0]
                
    def update_phase(self, phase):
        '''
        Connect the phase id found to the corresponding phase
        
        Arguments:
            phase: The original phase
        '''
        phase = phase.lower()
        if "iii" in phase:
            return "Phase 3"

        if "ii" in phase:
            return "Phase 2"

        if "i" in phase:
            return "Phase 1"

    def update_indication(self, indication):
        '''
        Clean up the indication field
        
        Arguments:
            indication: The original string containing the indication
        '''
        indication = indication.replace("\n", " ")
        indication = indication.split("(")
        return indication[0]

    def update_therapeutic(self, therapeutic_area, made_dict):
        '''
        Match the code found for the therapeutic_area with the correct
        actual therapeutic area
        
        Arguments:
            therapeutic_area: The original string containing the therapeutic
                              area
            made_dict: A dictionary of the therapetuic area headers found on
                       the page
        '''
        for key in made_dict:
            if therapeutic_area in key:
                updated_ta = made_dict[key].split("(")[0]
                final_ta = re.sub(r'[^a-zA-Z0-9& ]','', updated_ta)
                return final_ta