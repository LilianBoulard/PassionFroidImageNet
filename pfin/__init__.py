import sys
import logging

from .utils import *
from .config import *
from .user import User
from .image import Image
from .filter import Filter
from .database import ImageDatabase, UserDatabase

__all__ = ['User', 'Image', 'Filter', 'ImageDatabase', 'UserDatabase']


###########
# LOGGING #
###########


logging_level = logging.DEBUG

logger = logging.getLogger()
logger.setLevel(logging_level)

formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s')
formatter.datefmt = '%m/%d/%Y %H:%M:%S'

# fh = logging.FileHandler(filename='C:/Temp/pfin.log', mode='w')
# fh.setLevel(logging_level)
# h.setFormatter(formatter)

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging_level)
sh.setFormatter(formatter)

# logger.addHandler(fh)
logger.addHandler(sh)
