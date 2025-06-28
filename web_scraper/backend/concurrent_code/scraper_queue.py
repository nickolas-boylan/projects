#############################################################################
# scraper_queue.py
# 
# This module is provides a concurrency safe queue to store both the scraped
# treatments and partial responses to send to the frontend. This queue is
# expected to be used by both the ScraperManger and all producer threads.
#
#############################################################################

import threading

class ScraperQueue:

    """
    A concurrency safe queue for stroing scraped treatments that are
    eventually returned to the frontend.

    Attributes:
        treatment_queue: List of all treatments found by producer threads.
                         Each treatment is a dictionary
        response_queue: Stores textual status updates from the scrapers
        treatment_lock: A mutex lock used in combination with Condition to
                        manage concurrency with treatment_queue
        is_occupied: Condition variable used to notify any waiting threads
                     when new treatments are added. Created from
                     treatment_lock
        response_lock: A mutex used with response_read Condition to
                       synchronize access to response_queue
        response_ready: Condition variable to signal and wait when new
                        response data is added to response queue. Created from
                        response_lock
        final_ready: Thread event used to prevent any consumer from accessing
                     the treatment_queue until all producers have finished
    """

    def __init__(self):
        """
        Initialize the data structures and locks for concurrency
        """
        self.treatment_queue = []
        self.response_queue = []
        self.treatment_lock = threading.Lock()
        self.response_lock = threading.Lock()
        self.is_occupied = threading.Condition(self.treatment_lock)
        self.response_ready = threading.Condition(self.response_lock)
        self.final_ready = threading.Event()


    def insert_next_list(self, next_treatments):
        """
        Arguments:
            next_treatments: A list of treatments (dicts). Returned from a
                             scraper's scraping_implementation method
        
        Notes:
            - Appends the list of new treatments into self.treatment_queue
            - Notifies any waiting threads via self.is_occupied.notify()
        """
        with self.is_occupied:
            self.treatment_queue.extend(next_treatments)
            self.is_occupied.notify()

    def add_response(self, response):
        """
        Store a response item (e.g., partial or intermediate data)
        in response_queue, then notify any waiting thread

        Arguments:
            response: The response data to store
        """
        with self.response_ready:
            self.response_queue.append(response)
            self.response_ready.notify()
    
    def grab_response(self):
        """
        Block until there is at least one response item in response_queue,
        then pop and return it

        Returns:
            The oldest response item in the queue

        Notes:
            - If no response is available, this method will wait until one is
              appended (via add_response)
        """
        with self.response_ready:
            while len(self.response_queue) == 0:
                self.response_ready.wait()
            
            return self.response_queue.pop(0)

    def set_done(self):
        """
        Set the event that forces threads to wait for the final list to
        completed
        """
        self.final_ready.set()
    
    def get_final_list(self):
        """
        Retrieve the entire list of treatments

        Returns:
            the entirety of the treatment_queue
        
        Notes:
            - The thread that calls this will wait until all producers are
              finished (signaled by self.set_done())
        """
        self.final_ready.wait()
        return self.treatment_queue