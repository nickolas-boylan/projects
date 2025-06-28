#############################################################################
# request_manager.py
# 
# This module defines the callback module that gets created and used whenever
# the http.server recieves a request. Because of this, the RequestManager class
# is a subclass of the BaseHTTPRequestHandler from http.server.
#
# When the request gets processed, it will call either do_GET or do_POST after
# which it parses the path and calls the corresponding function to process the
# request.
#
#############################################################################

import json
from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
import logging, os

from backend.concurrent_code.scraper_manager import ScraperManager
from backend.company_scrapers.moderna_scraper import ModernaScraper
from backend.company_scrapers.teva_scraper import TevaScraper
from backend.company_scrapers.sanofi_scraper import SanofiScraper
from backend.company_scrapers.roche_scraper import RocheScraper
from backend.company_scrapers.bayer_scraper import BayerScraper
from backend.company_scrapers.ucb_scraper import UcbScraper
from backend.company_scrapers.gilead_scraper import GileadScraper
from backend.company_scrapers.ucb_scraper import UcbScraper
from backend.company_scrapers.xbiotech_scraper import XBiotechScraper
from backend.company_scrapers.mitsubishi_scraper import MitsubishiScraper
from backend.company_scrapers.regeneron_scraper import RegeneronScraper
from backend.company_scrapers.amgen_scraper import AmgenScraper
from backend.company_scrapers.csl_scraper import Cslscraper


CSV_CLIENT_PATH = '/tmp/treatment_output.csv'

class RequestManager(BaseHTTPRequestHandler):
    '''
    Class to parse and process an http request. Should only be created and used
    to process requests recieved by an http.server HTTPServer
    '''
    def do_POST(self):
        '''
        Parse a POST request and run the corresponding process

        Notes:
            - There are four viable requests that can be made. If none of the
              four are matched, an error is sent back to the frontend
        '''
        path = self.path
        if path == "/scrape":
            self._scraping_route()
        elif path == "/download_csv":
            self._download_scraped_csv()
        elif path == "/get_response":
            self._get_response()
        elif path == "/get_final":
            self._get_final()
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Invalid path")
    
    def _scraping_route(self):
        '''
        Start up the scraping process by creating a ScraperManager and all the
        producers (and both queues).

        Notes:
            - All info that must be kept track of for later requests (like the
              final data) are put into the ScraperManager which is then added
              to the server's state.
            - Because of this, this function does not block on any threads and
              instead lets them run in the background
        '''
        # Get the companies to scrape from the body of the request
        content_length = int(self.headers.get("Content-Length"))
        body = self.rfile.read(content_length)
        requested_companies = body.decode()[1:-1].split(',')
        for i in range(len(requested_companies)):
            requested_companies[i] = requested_companies[i].strip('\"')
        
        if len(requested_companies) == 0:
            self.send_error(HTTPStatus.BAD_REQUEST, "No companies sent in body")
            return
        
        # Create the ScraperManager and all threads
        scraper_manager = ScraperManager()
        scrapers = {"teva": TevaScraper, "sanofi": SanofiScraper,
                    "moderna": ModernaScraper, "roche": RocheScraper,
                    "bayer": BayerScraper, "ucb": UcbScraper,
                    "gilead": GileadScraper, "mitsubishi": MitsubishiScraper,
                    "xbiotech": XBiotechScraper, "regeneron": RegeneronScraper,
                    "amgen": AmgenScraper, "csl": Cslscraper}
        
        for company in requested_companies:
            if company in scrapers:
                scraper_manager.add_producer(scrapers[company]())
        
        # Start all threads and send response
        scraper_manager.start()
        uid = self.server.register_scraper(scraper_manager)
        
        self.send_response(HTTPStatus.ACCEPTED)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(uid.encode('utf-8'))
    
    def _get_response(self):
        '''
        Get a partial response from an already started scrape request

        Notes:
            - If a request was not started, this responds with an error
            - This will block until there is a response in the queue
        '''
        content_length = int(self.headers.get("Content-Length"))
        uid = self.rfile.read(content_length).decode()
        
        res = self.server.grab_response(uid)
        if not res:
            self.send_error(HTTPStatus.BAD_REQUEST, "No request started")
            return
        
        self.send_response(HTTPStatus.PARTIAL_CONTENT)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(res.encode('utf-8'))

    def _get_final(self):
        '''
        Get the final combined data as a list of dictionaries where each
        dictionary is a single treatment and its info

        Notes:
            - If a request was not started, this responds with an error
            - This will block until all scrapers have finished adding their
              treatments found into the queue
        '''
        content_length = int(self.headers.get("Content-Length"))
        uid = self.rfile.read(content_length).decode()
        
        res = self.server.grab_final(uid)
        if not res:
            self.send_error(HTTPStatus.BAD_REQUEST, "No request started")
            return
        
        res_json = json.dumps(res)
        
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(res_json.encode('utf-8'))

    def _download_scraped_csv(self):
        '''
        Get the final data but in csv form

        Notes:
            - If a request was not started, this responds with an error
            - This will block until the csv consumer finishes writing
        '''
        content_length = int(self.headers.get("Content-Length"))
        uid = self.rfile.read(content_length).decode()
        
        try:
            self.send_response(HTTPStatus.OK)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-Disposition",
                             "attachment; filename=treatment_output.csv")
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.end_headers()

            data = self.server.grab_csv(uid)
            self.wfile.write(data.encode('utf-8'))
        except Exception as e:
            logging.error(f"Error occurred during CSV download: {e}")
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR,
                            "CSV file not found!")
    
    def do_GET(self):
        '''
        Parse a GET request and get the corresponding page
        '''
        self._get_webpage()
    
    def _get_webpage(self):
        '''
        Parse the path and see if a corresponding file exists in the frontend
        folder.

        Notes:
            - If the file doesn't exist, it returns a 404 error
        '''
        if self.path in ["/", ""]:
            self.path = "/index.html"
        
        if not os.path.exists("frontend" + self.path):
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return

        # Get correct content-type
        ext = os.path.splitext(self.path)[1]
        if ext == ".js":
            ct = "text/javascript; charset=utf-8"
        elif ext == ".css":
            ct = "text/css; charset=utf-8"
        elif ext == ".svg":
            ct = "image/svg+xml"
        elif ext == ".html":
            ct = "text/html; charset=utf-8"
        elif ext == ".ico":
            ct = "image/x-icon"
        else:
            ct = "text/plain"
        
        try:
            with open("frontend" + self.path, "rb") as f:
                fs = os.fstat(f.fileno())
                
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Length", str(fs[6]))
                self.send_header("Content-Type", ct)
                self.end_headers()
                self.wfile.write(f.read())
        except OSError:
            self.send_error(404)
        except:
            logging.error(f"couldn't send {self.path} to client")