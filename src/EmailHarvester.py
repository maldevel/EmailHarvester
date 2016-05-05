import importlib
import sys

import validators

import argparse
from argparse import RawTextHelpFormatter

from urllib.parse import urlparse

from com.plugins.SocialNetworks import SocialNetworks
from com.utils.ColorPrint import ColorPrint

from com.core.EmailHarvester import EmailHarvester
from com.core.OptionManager import OptionManager
from com.utils.exceptions.EmailHarvesterException import EmailHarvesterException
import com.plugins.searchEngines as SE


def check_proxy_url(url):
    """
    Check if the proxy given by the user is correctly formated. Throw an ArgumentTypeError esception if not.

    Mean that it contains a correct scheme (http or https) and a correct network location
    :param url: the url that should be used by the user as a String
    :return: ParsedResult from urlib.parse package
    """
    url_checked = urlparse(url)
    if (url_checked.scheme not in ('http', 'https')) | (url_checked.netloc == ''):
        raise argparse.ArgumentTypeError('Invalid {} Proxy URL (example: http://127.0.0.1:8080).'.format(url))
    return url_checked


def limit_result_type(x):
    """
    Check if the limit of results providen by the user is correct. Throw an ArgumentTypeError esception if not.

    :param x: the limit of results that should be returned by EmailHarvester
    :return: int, the actual limit
    """
    x = int(x)
    if x > 0:
        return x
    raise argparse.ArgumentTypeError("Minimum results limit is 1.")


def exlude_type(exclude_option_string):
    """
    Check if all entries in the excluded list providen by the user is correct.

    :param exclude_option_string: the total string with coma separated search engines
    :return: the set of plugins ready-to-use
    """
    excludeds = set([])
    for plugin in exclude_option_string.split(","):
        cap_plugin = plugin.lower().capitalize()
        if cap_plugin in SE.__all__ or SocialNetworks.get_all():
            excludeds.add(cap_plugin)
        else:
            raise argparse.ArgumentTypeError("The excluded plugin " + str(plugin) + " is unknown.")
    return excludeds


def engine_type(selected_engine):
    """
    Check if the selected engine is "all" or exists.

    :param selected_engine: String containing the selected engine
    :return: the selected engine
    """
    lowercase_engine = selected_engine.lower()
    engines = set([])
    if lowercase_engine == "all":
        return set(SE.__all__)
    else:
        for engine in lowercase_engine.split(","):
            cap_engine = engine.capitalize()
            if cap_engine in SE.__all__:
                engines.add(cap_engine)
            else:
                raise argparse.ArgumentTypeError("The chosen search engine " + str(cap_engine) + " is unknown.")
    return engines

def network_type(selected_network):
    """
    Check if the selected network is "all" or exists.

    :param selected_network: String containing the selected networkjava qt
    :return: the selected network
    """
    lowercase_engine = selected_network.lower()
    networks = set([])
    if lowercase_engine == "all":
        return set(SocialNetworks().get_all())
    else:
        for engine in lowercase_engine.split(","):
            cap_network = engine.capitalize()
            if cap_network in SocialNetworks().get_all():
                networks.add(cap_network)
            else:
                raise argparse.ArgumentTypeError("The chosen search engine " + str(cap_network) + " is unknown.")
    return networks


def checkDomain(value):
   domain_checked = validators.domain(value)
   if not domain_checked:
       raise argparse.ArgumentTypeError('Invalid {} domain.'.format(value))
   return value

__version__ = "1.3.0"

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""

 _____                   _  _   _   _                                _
|  ___|                 (_)| | | | | |                              | |
| |__  _ __ ___    __ _  _ | | | |_| |  __ _  _ __ __   __ ___  ___ | |_  ___  _ __
|  __|| '_ ` _ \  / _` || || | |  _  | / _` || '__|\ \ / // _ \/ __|| __|/ _ \| '__|
| |___| | | | | || (_| || || | | | | || (_| || |    \ V /|  __/\__ \| |_|  __/| |
\____/|_| |_| |_| \__,_||_||_| \_| |_/ \__,_||_|     \_/  \___||___/ \__|\___||_|

    A tool to retrieve Domain email addresses from Search Engines | @maldevel
                                {}: {}
""".format(ColorPrint.red('Version'), ColorPrint.yellow(__version__)),
                                     formatter_class=RawTextHelpFormatter)

    parser.add_argument("-d", '--domain', action="store", metavar='DOMAIN', dest='domain',
                        default=None, type=checkDomain, help="Domain to search.")
    parser.add_argument("-s", '--save', action="store", metavar='FILE', dest='filename',
                        default=None, type=str, help="Save the results into a TXT and XML file (both).")

    parser.add_argument("-e", '--engine', action="store", metavar='ENGINE', dest='engine',
                        default="all", type=engine_type, help="Select search engine plugin(eg. '-e google').")

    parser.add_argument("-n", '--network', action="store", metavar='NETWORK', dest='network',
                        default="all", type=network_type, help="Select the network to search in (eg. '-n linkedin').")

    parser.add_argument("-l", '--limit', action="store", metavar='LIMIT', dest='limit',
                        type=limit_result_type, default=100, help="Limit the number of results. By default, this " +
                                                                  "value is fixed to 100.")
    parser.add_argument('-u', '--user-agent', action="store", metavar='USER-AGENT', dest='uagent',
                        type=str, help="Set the User-Agent request header.")
    parser.add_argument('-x', '--proxy', action="store", metavar='PROXY', dest='proxy',
                        default=None, type=check_proxy_url, help="Setup proxy server (eg. '-x http://127.0.0.1:8080')")
    parser.add_argument('--noprint', action='store_true', default=False,
                        help='EmailHarvester will print discovered emails to terminal. It is possible to tell ' +
                             'EmailHarvester not to print results to terminal with this option.')
    parser.add_argument('-r', '--exclude', action="store", metavar='EXCLUDED_PLUGINS', dest="exclude",
                        type=exlude_type, default=None, help="Plugins to exclude when you choose 'all' for search " +
                                                             "engine or social network (eg. '-r google,twitter')")
    parser.add_argument('-p', '--list-plugins', action='store_true', dest='listplugins',
                        default=False, help='List all available plugins.')

    if len(sys.argv) is 1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()

    # First set of OptionManager
    option_manager = OptionManager()
    option_manager.set_options(args)

    email_harvester = EmailHarvester()
    try:
        email_harvester.run()
    except EmailHarvesterException as e:
        print(e)
        sys.exit()

    # TODO Commentaries
