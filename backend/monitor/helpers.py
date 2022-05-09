import logging
import pathlib

def get_logger(name='Overseer - MAIN', level=logging.INFO):
    logging.basicConfig(
        format='[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
        level=level,
        datefmt='%H:%M:%S',
    )

    logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)
    logging.getLogger('requests').setLevel(logging.WARNING)
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    
    return logging.getLogger(name)

def get_absolute_path() -> pathlib.Path:
    path = pathlib.Path(__file__).parent.absolute()
    return path
