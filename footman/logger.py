__author__ = 'maxvitek'
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

lh = logging.FileHandler('footman.log')
lh.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')
lh.setFormatter(formatter)

logger.addHandler(lh)