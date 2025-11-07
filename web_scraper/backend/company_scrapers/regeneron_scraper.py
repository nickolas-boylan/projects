#############################################################################
# regeneron_scraper.py
# 
# This module implements the MainScraper for Regenerons's website. It only
# implements the scraping_implementation() function from the original parent
# class.
#
#############################################################################

from bs4 import BeautifulSoup
from .main_scraper import MainScraper

class RegeneronScraper(MainScraper):
    def __init__(self):
        super().__init__(
            company="Regeneron",
            url="https://www.regeneron.com/science/investigational-pipeline"
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

        # Treatments are grouped by phase. Grab all groups and go through them
        grabbed_phases = bf_soup.find_all("button",
                                          {"data-bs-toggle": "collapse"})
        for next_phase in grabbed_phases:
            phase_element = next_phase.find("span")
            if not phase_element:
                continue
            found_phase = self.clean_phase(phase_element.get_text(strip=True))
            
            target = next_phase.get("data-bs-target", "")
            if not target.startswith(""):
                continue
            official_target = target[1:]

            sec_of_phase = bf_soup.find("div", id=official_target)
            if not sec_of_phase:
                continue
            
            # Go through all treatments found in the phase group
            found_treatments = sec_of_phase.find_all("div",
                                                class_="pipeline-table-entry")
            for treatment in found_treatments:
                name_class = "pipeline-table-entry-name"
                found_treatment_name = treatment.find("div",
                                               class_=name_class).text.strip()

                thera_class = "pipeline-table-entry-therapeuticArea-text"
                found_therapeutic_area = treatment.find("div",
                                               class_=thera_class).text.strip()

                indic_class = "pipeline-table-entry-indication"
                found_indication = treatment.find("div",
                                               class_=indic_class).text.strip()
            
                final_treatments.append({
                    "company": "Regeneron",
                    "therapeutic_area": found_therapeutic_area,
                    "indication": found_indication,
                    "treatment_name": found_treatment_name,
                    "phase": found_phase
                })
                
        return final_treatments