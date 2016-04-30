__author__ = 'herve.beraud'

import argparse
from argparse import RawTextHelpFormatter
import sys
from core.settings import SPLASH_SCREEN
from core import colors
from core import checks
from core import credits


def limit_type(x):
    x = int(x)
    if x > 0:
        return x
    raise argparse.ArgumentTypeError("Minimum results limit is 1.")


def setup():
    splash_screen = SPLASH_SCREEN.format(colors.red('Version'), colors.yellow(credits.__version__))

    parser = argparse.ArgumentParser(description=splash_screen,
                                     formatter_class=RawTextHelpFormatter)

    parser.add_argument("-d", '--domain', action="store", metavar='DOMAIN', dest='domain',
                        default=None, type=checks.checkDomain, help="Domain to search.")

    parser.add_argument("-s", '--save', action="store", metavar='FILE', dest='filename',
                        default=None, type=str, help="Save the results into a TXT and XML file (both).")

    parser.add_argument("-e", '--engine', action="store", metavar='ENGINE', dest='engine',
                        default="all", type=str, help="Select search engine plugin(eg. '-e google').")

    parser.add_argument("-l", '--limit', action="store", metavar='LIMIT', dest='limit',
                        type=limit_type, default=100, help="Limit the number of results.")

    parser.add_argument('-u', '--user-agent', action="store", metavar='USER-AGENT', dest='uagent',
                        type=str, help="Set the User-Agent request header.")

    parser.add_argument('-x', '--proxy', action="store", metavar='PROXY', dest='proxy',
                        default=None, type=checks.checkProxyUrl, help="Setup proxy server (eg. '-x http://127.0.0.1:8080')")

    parser.add_argument('--noprint', action='store_true', default=False,
                        help='EmailHarvester will print discovered emails to terminal. It is possible to tell EmailHarvester not to print results to terminal with this option.')

    parser.add_argument('-r', '--exclude', action="store", metavar='EXCLUDED_PLUGINS', dest="exclude",
                        type=str, default=None, help="Plugins to exclude when you choose 'all' for search engine (eg. '-r google,twitter')")

    parser.add_argument('-p', '--list-plugins', action='store_true', dest='listplugins',
                        default=False, help='List all available plugins.')

    if len(sys.argv) is 1:
        parser.print_help()
        sys.exit()

    return parser