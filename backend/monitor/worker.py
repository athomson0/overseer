import time
import requests
import common.errors as errors
from datetime import datetime
from hashlib import sha1
from helpers import get_logger

class RequestError:
    """TOOD: Represents an error encountered whilst trying to make a request to a service.
    Used to create an "incident" which will be stored in the database."""
    
    def __repr__(self):
        return f"Request Exception(message={self.message})"
    
    def __init__(self, service_name, error):
        self.service_name = service_name
        self.created = datetime.utcnow()
        self.message = error.message
        
        """TODO
        A hash is created and then should be stored in the database to stop "duplicate" incidents from being created.
        Currently, this just checks to make sure that another error of the same type hasn't occured on the
        service today. I think there's probably a better way to do this, but I'm not sure right now.
        """
        self.hash = sha1((service_name + self.message + datetime.today().strftime("%A")).encode('utf8')).hexdigest()


class Worker:
    def __init__(self, service, session):
        self.service = service
        self.session = session
        self.alive = True
        self.logger = get_logger(name=f"{service.name}")
        
    def __del__(self):
        """Called whenever the thread is exiting (e.g. the service has been disabled)
        TODO: Graceful thread exiting? Is there more cleanup we should be doing?
        """
        if self.service.enabled == False:
            self.logger.info(f"{self.service.name}.enabled = False. Exiting thread...")
        else:
            self.logger.error("Unknown error encountered...")

    def _process_alive(self):
        """This method is called when a service is reachable. If the service is already marked
        as being live in the database, it should just return. If the service is marked as being
        down in the database, then switch it to being live.
        """
        if self.service.online:
            return
        
        self.service.online = True
        
        self.logger.info(f"{self.service.name} is live once again!")
        
    def _process_error(self, error):
        """This method is called when a service is not reachable. If the service is already marked
        as being not live in the database, it should just return. If the service is marked as being
        live, then it should be switched to not being live. A new IncidentHandler instance should
        be created, which will then handle both creating incidents in the database and  alerting.
        """
        if not self.service.online:
            return
        
        self.logger.warn(error)
        
        self.service.online = False
        
    def fetch(self):
        """Simply returns a requests.get object. 
        Maybe it'd be faster to use plain old urrllib or sockets?
        """
        return requests.get(self.service.connection_string, timeout=self.service.timeout)
      
    def check_is_alive(self):
        """Checks to see whether a service is live or not, and then forwards information to 
        either _process_alive() or _process_error().
        """
        self.service.last_checked = datetime.utcnow()
        
        try:
            response = self.fetch()
            
            if response.status_code != self.service.expected_http_status:
                self._process_error(RequestError(
                    service_name=self.service.name,
                    error=errors.MONITOR_UNEXPECTED_HTTP_STATUS(
                        expected=self.service.expected_http_status,
                        got=response.status_code
                    )))
                    
                return
            
            self.service.response_time = round(response.elapsed.total_seconds() * 1000) # secs > ms
            self._process_alive()
            
        except requests.exceptions.Timeout as e:
            self._process_error(RequestError(
                service_name=self.service.name,
                error=errors.MONITOR_HTTP_TIMEOUT(
                    timeout=self.service.timeout
                )))
            
        except requests.exceptions.SSLError as e:
            self._process_error(RequestError(
                service_name=self.service.name,
                error=errors.MONITOR_HTTP_SSL_ERROR(
                    connection_string=self.service.connection_string
                )))
            
        except Exception as e:
            self._process_error(RequestError(
                service_name=self.service.name,
                error=errors.MONITOR_UNKNOWN()
            ))
        
    def run(self):
        """The main worker loop. Should sleep for the amount of time defined in the database."""
        while self.service.enabled:
            self.check_is_alive()
            
            """Sleep for the amount of time specified by the user (default: 30s)"""
            time.sleep(5)
            # time.sleep(self.service.poll)