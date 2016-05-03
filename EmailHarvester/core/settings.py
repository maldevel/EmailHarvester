import os
import os.path
import configparser
from EmailHarvester.core.splash import DOOM


__author__ = "Hervé Beraud"
__copyright__ = "Copyright (c) 2016 @Hervé Beraud"
__credits__ = ["maldevel", "PaulSec", "cclauss", "Christian Martorella"]
__license__ = "GPLv3"
__version__ = "2.0.1"
__maintainer__ = "Hervé Beraud"

config = configparser.ConfigParser()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_FILE = os.path.join(BASE_DIR, '..', 'settings.cfg')
if os.path.isfile(CONFIG_FILE):
    config.read(CONFIG_FILE)

#SPLASH_SCREEN = (config['DEFAULT']['SPLASH_SCREEN'] or DOOM)
SPLASH_SCREEN = DOOM

DFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"

