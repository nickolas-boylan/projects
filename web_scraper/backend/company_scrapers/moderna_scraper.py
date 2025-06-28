#############################################################################
# moderna_scraper.py
# 
# This module implements the MainScraper for Moderna's website. It only
# implements the scraping_implementation() function from the original parent
# class.
#
#############################################################################

from bs4 import BeautifulSoup
from .main_scraper import MainScraper

class ModernaScraper(MainScraper):
    '''
    Scraper for Moderna
    '''
    def __init__(self):
        super().__init__(
            company="Moderna",
            url="https://modernatx.com/en-US/research/product-pipeline"
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

        headings = ("h3.indexstyles__ModalityHeading-sc-1mk3wkl-11.iHVoBD")
        headings_sorted = bf_soup.select(headings)

        # Go through all the treatment cards found
        for heading in headings_sorted:
            found_therapeutic_area = heading.get_text(strip=True)
            total_pipeline = heading.find_next_sibling("div")
            if not total_pipeline:
                continue
        
            each_item = total_pipeline.select(
                "div.indexstyles__PipelineItemWrapper-sc-1mk3wkl-12.ISJjV"
            )

            # Get the treatment info from the div
            for item in each_item:
                next_div = item.select("div.indexstyles__PipelineItemData"\
                                       "-sc-1mk3wkl-13.csUwmo")
                next_phase = item.select_one("div.indexstyles__PipelineItem"\
                                             "PhaseMobile-sc-1mk3wkl-16.bFAxqP")

                if len(next_div) > 0:
                    found_indication = next_div[0].get_text(strip=True)
                else:
                    found_indication = ""
                
                if len(next_div) > 1:
                    found_treatment_name = next_div[1].get_text(strip=True)
                else:
                    found_treatment_name = ""
                
                if next_phase:
                    found_phase = next_phase.get_text(strip=True)
                else:
                    found_phase = ""

                found_phase = self.clean_phase(found_phase)

                final_treatments.append({
                    "company": "Moderna",
                    "therapeutic_area": found_therapeutic_area,
                    "indication": found_indication,
                    "treatment_name": found_treatment_name,
                    "phase": found_phase
                })
                
        return final_treatments