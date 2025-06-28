#############################################################################
# producer.py
# 
# This module defines the producer_code function, which acts as the producer
# in a Producer-Consumer pattern. Each producer is responsible for scraping
# data from a particular source (e.g., a pharmaceutical company's development
# pipeline page) and inserting the results into two separate queues:
#
#     1. treatment_queue (ScraperQueue) for accumulating data to be returned to
#        the frontend
#     2. treatment_file_queue (TreatmentFileQueue) for accumulating data that
#        the CSV-writing consumer thread will then process
#
# Example Usage:
#    scraping_queue = ScraperQueue()
#    treatment_file_queue = TreatmentFileQueue()
#    company_scraper = SomeCompanyScraper()
#
#    next_producer = threading.Thread(
#        target=producer_code,
#        args(company_scraper, scraping_queue, treatment_file_queue),
#        name="SomeCompany-Producer"
#        )
#    
#    next_producer.start()
#    next_producer.join()
#############################################################################

import logging

def producer_code(next_scraper, treatment_queue, treatment_file_queue):
    """
    Perform scraping for a given scraper instance and store results in the
    corresponding queues.

    Arguments:
        next_scraper (object): An instance of a scraper class with attributes
        treatment_queue (ScraperQueue):
            If provided, the scraped treatments are inserted into this queue.
            This queue is used to return data to the frontend
        treatment_file_queue(TreatmentFileQueue):
            If provided, the scraped treatments are also inserted here so that
            a consumer thread can write the data to a CSV file
    
    Returns:
        None. (The results are placed into the provided queues)
    
    Notes:
        - Because this function is meant to be ran using a thread, it does
          not actually return any data directly. It instead pushes
          data into shared concurrency queues
    """
    logging.info(f"Scraping info for {next_scraper.company_name}...")

    found_treatments = next_scraper.scraping_implementation()

    logging.info(f"Finished scaping info for {next_scraper.company_name}." +
                 f" Found {len(found_treatments)} treatments.")
    
    # Inserts results into the queues
    treatment_queue.insert_next_list(found_treatments)
    treatment_file_queue.insert_next_batch(found_treatments)

    treatment_queue.add_response(f"Finished scaping info for "\
                                 f"{next_scraper.company_name}. Found "\
                                 f"{len(found_treatments)} treatments.")