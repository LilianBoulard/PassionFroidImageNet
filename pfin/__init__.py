import sys
import logging

from .image import Image
from .filter import Filter
from .user import User, DummyUser
from .config import PFIN_SERVER, PFIN_SECRET
from .database import ImageDatabase, UserDatabase

__all__ = ['Image', 'Filter', 'User', 'DummyUser', 'PFIN_SERVER', 'PFIN_SECRET', 'ImageDatabase', 'UserDatabase']


###########
# LOGGING #
###########


logging_level = logging.DEBUG

logger = logging.getLogger()
logger.setLevel(logging_level)

formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s')
formatter.datefmt = '%m/%d/%Y %H:%M:%S'

# fh = logging.FileHandler(filename='C:/Temp/qfap.log', mode='w')
# fh.setLevel(logging_level)
# h.setFormatter(formatter)

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging_level)
sh.setFormatter(formatter)

# logger.addHandler(fh)
logger.addHandler(sh)
