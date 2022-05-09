import time
import threading
from worker import Worker
from helpers import get_logger
from common.database import Database
from models.service import Service

class Monitor:
    """The Monitor class keeps track of all worker threads."""
    
    def __init__(self):
        self.logger = get_logger()
        
        """The database instance variable will hold the connection to our database.
        It will be passed to all children worker threads so that a persistant
        connection is held.
        """
        self.database = Database()
        
        """The services instance variable is a dictionary which will hold all of our
        children worker threads. The key will be the service ID, and the value will
        be the threading.Thread object. Useful for checking to see whether a thread
        is alive or not.
        """
        self.services = {}
        
        self.run()
        
    def _add_service(self, service):
        """Will be called whenever a service is added via the web frontend."""
        self.logger.info(f"Adding service: {service.name} (id: {service.id})")
        
        worker = Worker(service, self.database.session)
        thread = threading.Thread(target=worker.run)
        thread.name = service.name
        thread.daemon = True
        self.services[service.id] = thread
        
        thread.start()
        
    def _remove_service(self, service):
        """Will be called whenever a service is disabled via the web frontend."""
        self.logger.info(f"Removing service (name: {service.name}, id: {service.id})")
        
        """Make sure the thread isn't still alive - we don't want AWOL idle threads"""
        if self.services[service.id].is_alive():
            self.logger.error(f"Attempted to remove a thread which is still alive? ({service})")
            return
        
        del self.services[service.id]
        
    def _service_is_loaded(self, service):
        """Returns true if the service ID already exists in self.services, else returns false."""
        return service.id in self.services
        
    def run(self):
        """The main application loop."""
        while True: 
            all_services = self.database.session.query(Service).all()
            
            for service in all_services:                
                if service.enabled and not self._service_is_loaded(service):
                    self._add_service(service)
                    
                if self._service_is_loaded(service):
                    if not self.services[service.id].is_alive():
                        self._remove_service(service)
                
            time.sleep(5)