__author__ = 'maxvitek'
import logging

logger = logging.getLogger('footman')
logger.setLevel(logging.DEBUG)

lh = logging.FileHandler('footman.log')
lh.setLevel(logging.INFO)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')
lh.setFormatter(formatter)
sh.setFormatter(formatter)

logger.addHandler(lh)
logger.addHandler(sh)