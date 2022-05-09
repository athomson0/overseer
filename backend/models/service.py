import datetime
from .mixins import Serializer
from sqlalchemy import Column, DateTime, Integer, String, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Boolean, Float

ServiceBase = declarative_base()

class Service(ServiceBase, Serializer):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    connection_string = Column(String)
    timeout = Column(Integer, default=5)
    expected_http_status = Column(Integer, default=200)
    poll = Column(Integer, default=30)
    online = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)
    last_checked = Column(DateTime, default=datetime.datetime.utcnow)
    response_time = Column(Integer)
    stype = Column(String, default="Website")
    
    def __repr__(self):
        return str(vars(self))
    
    def __init__(self, name, connection_string, stype="Website", expected_http_status=200, enabled=True, online=True, poll=30, timeout=10, response_time=0):
        self.name = name
        self.connection_string = connection_string
        self.online = online
        self.poll = poll
        self.timeout = timeout
        self.enabled = enabled
        self.expected_http_status = expected_http_status
        self.response_time = response_time
        self.stype = stype
    
    def serialize(self):
        d = Serializer.serialize(self)
        
        return d
    
