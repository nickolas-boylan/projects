#############################################################################
# scraper_manager.py
# 
# This module is what contains all relevant information and data for managing
# a single scraping request. It contains all threads and both output queues.
# It also helps facilitate communication between frontend and backend by
# having functions to grab the messages/data.
#
#############################################################################

import threading

from backend.concurrent_code.producer import producer_code
from backend.concurrent_code.scraper_queue import ScraperQueue
from backend.concurrent_code.treatment_file_queue import TreatmentFileQueue
from backend.concurrent_code.file_consumer import file_consumer

class ScraperManager:
    '''
    Class to server as a manager for all the scraping threads and the consumers
    that transform that data.
    
    Attributes:
        producers: A list of all scraping producers
        scraping_queue: The ScraperQueue connecting all producers and this
        treatment_file_queue: The TreatmentFileQueue responsible for providing
                              treatments to the csv consumer
        treatment_file_consumer_thread: The consumer writing the csv
        completion_thread: A thread to run in the background to keep track of
                           when all producers finish and then notify consumers
    '''
    def __init__(self):
        '''
        default constructor

        Notes:
            - The consumer threads are all created but the producers are not
              created here.
            - No threads are started either. Call manager.start() to start them
        '''
        self.producers = []
        self.scraping_queue = ScraperQueue()
        self.treatment_file_queue = TreatmentFileQueue()
        self.treatment_file_consumer_thread = threading.Thread(
            target=file_consumer,
            args=[self.treatment_file_queue],
            name="Treatment-File-Consumer"
        )

        self.completion_thread = threading.Thread(
            target=self.wait_for_total_completion,
            daemon=True
        )

    def add_producer(self, scraper):
        '''
        Add a producer running the given scraper to the list of producers
        
        Arguments:
            scraper: An instance of one of the scraper classes to use for the
                     producer
        '''
        next_scraper = threading.Thread(
            target=producer_code,
            args=(scraper, self.scraping_queue, self.treatment_file_queue),
            name=f"{scraper.company_name}-Producer"
        )
        self.producers.append(next_scraper)
    
    def grab_response(self):
        '''
        Grab a response from the scraper queue's response queue

        Notes:
            - This will block if the queue is currently empty
        '''
        return self.scraping_queue.grab_response()
    
    def grab_final(self):
        '''
        Grab the full list of all treatments found

        Notes:
            - This will block if the producers are still not finished
        '''
        return self.scraping_queue.get_final_list()

    def grab_csv(self):
        '''
        Grab the full list of all treatments found in csv form

        Notes:
            - This will block if the csv is still being created
        '''
        return self.treatment_file_queue.get_final()
    
    def start(self):
        '''
        Starts all producers, all consumers, and the completion thread
        '''
        self.treatment_file_consumer_thread.start()
        
        for thread in self.producers:
            thread.start()
        
        self.completion_thread.start()

    def wait_for_total_completion(self):
        '''
        Wait for all producers to finish then signal to both queues that the
        producers are done. Wraps up all the threads

        Notes:
            - This thread is meant to be running in the background as a daemon
              simply to be able to notify all consumers to finish up 
        '''
        for next_thread in self.producers:
            next_thread.join()

        self.scraping_queue.set_done()
        self.treatment_file_queue.all_done()

        self.treatment_file_consumer_thread.join()
