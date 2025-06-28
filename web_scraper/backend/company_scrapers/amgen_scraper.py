#############################################################################
# amgen_scraper.py
# 
# This module implements the MainScraper for Amgen's website. It only
# implements the scraping_implementation() function from the original parent
# class.
#
#############################################################################

from bs4 import BeautifulSoup
from .main_scraper import MainScraper

class AmgenScraper(MainScraper):
    def __init__(self):
        super().__init__(
            company="Amgen",
            url="https://www.amgenpipeline.com/"
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

        found_treatments = bf_soup.find_all("div",
                                            class_="row collapsibleContent")

        # Go through the list of all elements and parse them into treatments
        for next_treatment in found_treatments:
            name_element = next_treatment.select_one(".col-sm-3." +
                                                 "border-right .textContent")
            if name_element:
                found_treatment_name = name_element.get_text(strip=True)
            else:
                found_treatment_name = None

            found_col = next_treatment.select_one(".col-sm-9")
            if not found_col:
                continue
            
            # Some treatments with the same are given two rows.
            # Break up those rows and treat them as different treatments
            found_blocks = found_col.find_all("div", class_="wrapper row")
            for next_block in found_blocks:
                area_element = next_block.select_one(".first-column ." +
                                                     "tarea-text")
                if area_element:
                    found_therapeutic_area = area_element.get_text(strip=True) 
                else:
                    found_therapeutic_area = None

                phase_element = next_block.select_one(".fourth-column .badge")
                if phase_element:
                    found_phase = phase_element.get_text(strip=True)
                else:
                    found_phase = None
                found_phase = self.clean_phase(found_phase)

                indication_element = next_block.select_one(".second-column ." +
                                                           "card-block a")
                if indication_element:
                    found_indication = indication_element.get_text(strip=True)
                else:
                    found_indication = None 

                final_treatments.append({
                    "company": "Amgen",
                    "therapeutic_area": found_therapeutic_area,
                    "indication": found_indication,
                    "treatment_name": found_treatment_name,
                    "phase": found_phase
                })
                
        return final_treatments