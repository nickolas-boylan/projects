#############################################################################
# main_scraper.py
# 
# This module defines an abstract class to be fully implemented by the actual
# company scraper classes. It uses an API request to Zyte to obtain the post
# javascript html code of the websites
#
#############################################################################

import requests
import logging
import os

from dotenv import load_dotenv
load_dotenv()

class MainScraper:
    '''
    Abstract class to use zyte to scrape a website and get treatments from the
    response
    
    Attributes:
        company_name: The name of the company being scraped
        url: The url of the site being scraped
        zyte_api_key: The API key to use for Zyte. Kept on the .env file
    '''
    def __init__(self, company, url):
        '''
        Constructor
        
        Arguments:
            company_name: The name of the company being scraped
            url: The url of the site being scraped
        '''
        self.company_name = company
        self.url = url
        self.zyte_api_key = os.getenv("ZYTE_API_KEY")

    
    def fetch_with_zyte(self):
        '''
        Run the fetch request with the zyte API
        
        Returns:
            The response to the request containing all the html code
        
        Notes:
            - If the request is not successful, the empty string is returned
        '''
        request_params = {
            "url": self.url,
            "browserHtml": True,
            "actions": [
                {"action": "scrollBottom"},
                {"action": "waitForTimeout", "timeout": 15}
            ]
        }

        # Send the request to zyte and wait for the response
        try:
            response = requests.post(
                url="https://api.zyte.com/v1/extract",
                auth=(self.zyte_api_key, ''),
                json=request_params
            )

            # Check for valid response
            if response.status_code == 200:
                found_code = response.json()
                logging.info(f"Got response from API for {self.company_name}.")
                return found_code.get("browserHtml", "")
            else:
                logging.error(f"Failed to grab {self.company_name}. Current "\
                              f"Status: {response.status_code}")
                return ""
        except Exception as e:
            logging.error(f"Error grabbing {self.company_name}: {str(e)}")
            return ""
    
    def scraping_implementation(self):
        """
        Each scraper needs to implement their own version
        """
        raise NotImplementedError
    
    def clean_phase(self, original_phase):
        '''
        Normalize the phases found by the scrapers to a set of chosen phases
        
        Arguments:
            original_phase: The original phase that was found by the scraper
        
        Returns:
            The normalized phase
        
        Notes:
            - If a phase that wasn't originally in the set is found, it logs
              an error and returns the original phase
        '''
        if original_phase is None:
            return "N/A"
    
        if original_phase.lower() == "null" or original_phase.lower() == "":
            return "N/A"

        if original_phase.lower() in ["commercial", "registration", 
                                "under regulatory review", "confirmatory study",
                                "phase 4", "filed", "phase r", "filed",
                                "registration / post-registration"]:
            return "Approved"
        
        if original_phase.lower() == "1":
            return "Phase 1"

        if original_phase.lower() == "2":
            return "Phase 2"

        if original_phase.lower() == "3":
            return "Phase 3"

        if original_phase.lower() == "phase i":
            return "Phase 1"

        if original_phase.lower() == "phase ii":
            return "Phase 2"

        if original_phase.lower() == "phase iii":
            return "Phase 3"
        
        if original_phase.lower() in ["phase 1", "phase 2", "phase 3"]:
            return original_phase

        if "clinical stage program" in original_phase.lower():
            return "N/A"
        
        if original_phase.lower() in ["pre-clinical", "preclinical", 
                                                    "preclinical development"]:
            return "Preclinical"

        logging.error("unregistered phase found: " + original_phase)
        return original_phase