##############################################################################
# treatment_file_queue.py
#
# Defines TreatmentFileQueue, a thread-safe queue that producer threads use
# to enqueue treatments destined for CSV writing, and a consumer thread
# (treatment_file_consumer) uses to dequeue them one at at a time
#    
# treatment_file_queue.all_done() must be used to signal to the consumer that
# all producers have finished
#
##############################################################################

import threading

class TreatmentFileQueue:

    """
    A concurrency-safe queue for treatments that the CSV-writing consumer
    will process. Producers insert treatments in batches, and the consumer
    fetches them one by one.

    Attributes:
        treatments_found: A list holding all the queued treatments. Each
                          element is a dictionary representing a treatment and
                          it's corresponding information
        lock: A mutex lock used to syncronize access to treatments_found
        batches_found: A condition variable used to signal the consumer that
                       new treatments have arrived or that a sentinel value
                       (None) has been inserted to signal completion
        final: A string that will hold the entire finished csv file as a string
        thread_finished: A thread Event that is used to block threads from
                         accessing final before the csv if finished writing
    """

    def __init__(self):
        """
        Initialize an empty list for treatments, a threading lock, and
        a Condition for synchronization
        """
        self.treatments_found = []
        self.final = ""
        self.lock = threading.Lock()
        self.batches_found = threading.Condition(self.lock)
        self.thread_finished = threading.Event()

    def insert_next_batch(self, next_batch):
        """
        Insert an entire batch of new treatments into the queue,
        then notify any waiting consumer that items are available

        Arguments:
            next_batch: A list of treatment dictionaries to add
        
        Notes:
            - treatments_found is accessed concurrently so it must be accessed
              with mutual exclusion
            - The batches_found condition is signaled after adding
        """
        with self.batches_found:
            self.treatments_found.extend(next_batch)
            self.batches_found.notify()
    
    def grab_next_treatment(self):
        """
        Wait until there is a treatment available, then remove and return
        a single treatment from the front of the queue.

        Returns:
            - A treatment dictionary if one is available
            - If the sentinel value None is popped, it signals the end
              of the queue (all_done() function was called)

        Notes:
            - The consumer blocks on this method until a treatment is available
            - Only one treatment at a time is popped in this implementation
        """
        with self.batches_found:
            while not self.treatments_found:
                self.batches_found.wait()

            next_treatment = self.treatments_found.pop(0)
            return next_treatment
    
    def set_final(self, final_csv):
        """
        Set the final csv and notify the threads that it is finished
        
        Arguments:
            final_csv: The final csv with all treatments as a string
        
        Notes:
            - Threads will be blocked until the file is finished writing
        """
        self.final = final_csv
        self.thread_finished.set()
    
    def get_final(self):
        """
        Get the final csv after it is finished being written
        
        Notes:
            - Threads will be blocked until the file is finished writing
        """
        self.thread_finished.wait()
        return self.final

    def all_done(self):
        """
        Signal that there are no more treatments to come by appending
        a None sentinel to the queue and notifying any waiting thread
        """
        with self.batches_found:
            self.treatments_found.append(None)
            self.batches_found.notify()