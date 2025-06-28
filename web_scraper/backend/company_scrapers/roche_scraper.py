#############################################################################
# roche_scraper.py
# 
# This module implements the MainScraper for Roche's website. It only
# implements the scraping_implementation() function from the original parent
# class.
#
#############################################################################

from bs4 import BeautifulSoup
from .main_scraper import MainScraper
import json

class RocheScraper(MainScraper):
    '''
    Scraper for Roche
    '''
    def __init__(self):
        super().__init__(
            company="Roche",
            url="https://www.roche.com/solutions/pipeline"
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
        
        # Get the whole table and get the json from it
        roche_pipeline_table = bf_soup.find("roche-pipeline-table")
        if not roche_pipeline_table:
            return []

        found_content = roche_pipeline_table.get('content')
        if not found_content:
            return []

        all_treatments = json.loads(found_content)

        # Parse the json created from the table found
        for treatment in all_treatments:
            treaatment_name = treatment.get('name', '')
            indication = treatment.get('indicationShort', '')
            phase = treatment.get('phase', '')
            therapeutic_area = treatment.get('therapeuticArea', '')

            phase = self.clean_phase(phase)

            final_treatments.append({
                "company": "Roche",
                "therapeutic_area": therapeutic_area,
                "indication": indication,
                "treatment_name": treaatment_name,
                "phase": phase
            })
                
        return final_treatments