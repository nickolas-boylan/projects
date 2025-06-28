#############################################################################
# server.py
# 
# This module starts up the server then processes all requests that come in.
# The server is configured by default to run on port 5000 on localhost. It
# uses the HTTPServer for a lot of the background work like starting and
# ending the sockets.
#
# When the request gets recieved, it will create a separate thread to handle
# the request so that if the request is one that blocks, the server isn't tied
# down and unable to handle other requests.
#
# To start an instance of Server use s.serve_forever()
#
# To end an instance of Server use s.quit_serving()
#
#############################################################################

import threading
import logging
import uuid
from http.server import HTTPServer
from backend.concurrent_code.request_manager import RequestManager

logging.basicConfig(level=logging.INFO)

class Server(HTTPServer):
    '''
    Subclass of HTTPServer that runs endlessly to recieve and handle HTTP
    requests
    
    Attributes:
        id_to_manager: A dictionary mapping the ips of the requests to the
                       corresponding ScraperManager that is handling their
                       request
        lock: A lock providing thread-safe access to the dictionary
    
    Notes:
        - Requests are recieved sequentially but processed concurrently
    '''
    def __init__(self, server_address, RequestHandlerClass,
                 bind_and_activate = True):
        '''
        constructor
        
        Arguments:
            server_address: The address the server is running on
            RequestHandlerClass: The class that will be used to handle requests
            bind_and_activate: Whether to start the server upon construction
        '''
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.id_to_manager = {}
        self.lock = threading.Lock()
        self.set_lock = threading.Lock()
    
    def quit_serving(self):
        '''
        Stop the server gracefully
        '''
        logging.info("shutting down server")
        self.shutdown()
        self.server_close()
    
    def process_request(self, request, client_address):
        '''
        Overwrites the process_request in HTTPServer to have requests handled
        concurrently
        
        Arguments:
            request: The request to handle
            client_address: The address of the client as a tuple: (ip, port)
        '''
        t = threading.Thread(target=self.start_one_request,
                             args=[request, client_address],
                             daemon=True)
        t.start()
    
    def start_one_request(self, request, client_address):
        '''
        Function to run by the threads created in process_request. Uses the
        functions in HTTPServer to handle the requests
        
        Arguments:
            request: The request to handle
            client_address: The address of the client as a tuple: (ip, port)
        '''
        self.finish_request(request, client_address)
        self.shutdown_request(request)
    
    def register_scraper(self, manager):
        '''
        Add a scraper manager to the server's state. A unique ID is generated
        which can be supplied to get access to the scraper after for future
        requests.
        
        Arguments:
            manager: The manager to register
        
        Returns:
            The unique id tied to this specific scraping request
        
        Notes:
            - id_to_manager may be accessed concurrently by the request_managers
              so it must be given mutual exclusion
        '''
        # Create a new id and make sure it is unique
        new_uuid = uuid.uuid4()
        self.lock.acquire()
        while new_uuid.hex in self.id_to_manager:
            new_uuid = uuid.uuid4()
        self.lock.release()
        new_id = new_uuid.hex

        # Add manager to id tied to id manager
        with self.lock:
            self.id_to_manager[new_id] = manager
        
        return new_id

    def grab_response(self, req_id):
        '''
        Grabs a partial response from the manager
        
        Arguments:
            req_id: The id of the request
        
        Returns:
            The response to send back to the frontend in string form
        
        Notes:
            - id_to_manager may be accessed concurrently by the request_managers
              so it must be given mutual exclusion
            - If there is no registered manager, it returns None
            - Will block if the manager's response queue is empty
        '''
        with self.lock:
            if req_id not in self.id_to_manager:
                return None
            
            manager = self.id_to_manager[req_id]
        
        return manager.grab_response()
    
    def grab_final(self, req_id):
        '''
        Grabs the final data from the manager
        
        Arguments:
            req_id: The source id of the request
        
        Returns:
            The entire final data which is a list of dictionaries
        
        Notes:
            - id_to_manager may be accessed concurrently by the request_managers
              so it must be given mutual exclusion
            - If there is no registered manager, it returns None
            - Will block if the manager's response queue is empty
        '''
        with self.lock:
            if req_id not in self.id_to_manager:
                return None
            
            manager = self.id_to_manager[req_id]
        
        return manager.grab_final()

    def grab_csv(self, req_id):
        '''
        Grabs the final csv data from the manager
        
        Arguments:
            req_id: The source id of the request
        
        Returns:
            The entire csv as a string
        
        Notes:
            - id_to_manager may be accessed concurrently by the request_managers
              so it must be given mutual exclusion
            - If there is no registered manager, it returns None
            - Will block if the csv is still being created
            - This is expected to be the last function to use the given manager
              so it removes it from the dictionary
        '''
        with self.lock:
            if req_id not in self.id_to_manager:
                return None
            
            manager = self.id_to_manager.pop(req_id)
        return manager.grab_csv()

def main():
    address = ("localhost", 5000)
    server = Server(address, RequestManager)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.quit_serving()

if __name__ == "__main__":
    main()
