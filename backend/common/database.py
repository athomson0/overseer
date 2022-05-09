from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.service import Service, ServiceBase
from helpers import get_absolute_path, get_logger


class Database:
    def __init__(self, no_init=False):
        self.no_init = no_init
        self.logger = get_logger(name="Overseer - DATABASE")
        self.logger.info("Initialising database connection...")
        self._init_db()    
        
    def _init_db(self):
        """
        Initialise the database connection.
        
        If the database file doesn't currently exist, then create it along with the schema, and seed
        it with some dummy services.
        """
        _DB_PATH = get_absolute_path().parent / 'overseer.db'
        _ENGINE = f"sqlite:///{_DB_PATH}?thread_safe=false"
        self.logger.info(f"Engine: {_ENGINE}")
        self._engine = create_engine(_ENGINE, echo=False)
        self.session = scoped_session(sessionmaker(autoflush=True, autocommit=True, bind=self._engine)) 
                
        if not self.no_init and not _DB_PATH.is_file():
            self.logger.info(f"No database file found ({_DB_PATH}), initialising fresh database...")
            self._create_database_schema()
            self._seed_database()
            
    def _create_database_schema(self):
        """Create the database schema."""
        self.logger.info("Creating database schema...")
        ServiceBase.metadata.create_all(self._engine)
        
        
    def _seed_database(self):
        """Seed the database with some dummy websites. Useful for testing."""
        self.logger.info("Seeding database...")

        self.session.add(Service(
            name="Google",
            connection_string="https://google.com",
            enabled=True
        ))
        
        self.session.add(Service(
            name="reddit",
            connection_string="https://reddit.com",
        ))

        """This service has an expired SSL cert"""
        self.session.add(Service(
            name="Expired SSL Example",
            connection_string="https://expired.badssl.com/",
            enabled=True
        ))
        
        """This service will take 7.5 seconds to load"""
        self.session.add(Service(
            name="Timeout example",
            connection_string="https://httpstat.us/200?sleep=7500",
            timeout=5,
            enabled=True
        ))
        
        """This service will return a bad HTTP status (400)"""
        self.session.add(Service(
            name="Bad HTTP status",
            connection_string="https://httpstat.us/400",
        ))
        