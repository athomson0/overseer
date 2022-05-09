from dataclasses import dataclass
from string import Formatter


@dataclass
class OverseerError:
    message: str
    
    class UnseenFormatter(Formatter):
        def get_value(self, key, args, kwds):
            if isinstance(key, str):
                try:
                    return kwds[key]
                except KeyError:
                    return key
            else:
                return Formatter.get_value(key, args, kwds)

    def __init__(self, **kwargs):
        fmt = self.UnseenFormatter()
        self.message = fmt.format(self.message, **kwargs)
        
class MONITOR_UNKNOWN(OverseerError):
    message = "An unknown error occured"

class MONITOR_HTTP_UNEXPECTED_STATUS(OverseerError):
    message = "Expected HTTP Status ({expected}), got HTTP {got} instead"
    
class MONITOR_HTTP_TIMEOUT(OverseerError):
    message = "Request timed out (timeout={timeout})"
    
class MONITOR_HTTP_SSL_ERROR(OverseerError):
    message = "SSL error encountered when connecting to {connection_string}"