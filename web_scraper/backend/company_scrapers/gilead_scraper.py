#############################################################################
# gilead_scraper.py
# 
# This module implements the MainScraper for Gilead's website. It only
# implements the scraping_implementation() function from the original parent
# class.
#
#############################################################################

from bs4 import BeautifulSoup
from .main_scraper import MainScraper

class GileadScraper(MainScraper):
    '''
    Scraper for Gilead
    '''
    def __init__(self):
        super().__init__(
            company="Gilead",
            url="https://www.gilead.com/science/pipeline"
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

        # Find the table of treatments and go through them one by one
        found_pipeline = bf_soup.select("li.list-pipeline-wrapper")
        for next_item in found_pipeline:
            therapeutic = next_item.get("data-category", "")
            found_therapeutic_area = therapeutic.strip() if therapeutic else ""

            treatment = next_item.select_one(".field-headbrandname")
            found_treatment_name = treatment.text.strip() if treatment else ""

            indication = next_item.select_one(".field-"\
                                                      "potentialindication")
            found_indication = indication.text.strip() if indication else ""

            phase_element = next_item.select_one(".phase-name")
            found_phase = phase_element.text.strip() if phase_element else ""
            found_phase = self.clean_phase(found_phase)

            final_treatments.append({
            "company": "Gilead",
            "therapeutic_area": found_therapeutic_area,
            "indication": found_indication,
            "treatment_name": found_treatment_name,
            "phase": found_phase
        })


        return final_treatments
            