#!/usr/bin/env python3
# encoding: UTF-8

"""
    This file is part of EmailHarvester
    Copyright (C) 2016 @maldevel
    https://github.com/maldevel/EmailHarvester
    
    EmailHarvester - A tool to retrieve Domain email addresses from Search Engines.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    For more see the file 'LICENSE' for copying permission.
"""

__author__ = "maldevel"
__copyright__ = "Copyright (c) 2016 @maldevel"
__credits__ = ["maldevel", "Christian Martorella"]
__license__ = "GPLv3"
__version__ = "1.1.2"
__maintainer__ = "maldevel"


################################
import argparse
import sys
import time
import requests
import re

from termcolor import colored
from argparse import RawTextHelpFormatter
from sys import platform as _platform
from urllib.parse import urlparse
################################


if _platform == 'win32':
    import colorama
    colorama.init()


class myparser:
    def __init__(self, results, word):
            self.results = results
            self.word = word
            self.temp = []
            
    def genericClean(self):
        self.results = re.sub('<KW>', '', self.results)
        self.results = re.sub('</KW>', '', self.results)
        self.results = re.sub('<title>', '', self.results)
        self.results = re.sub('</div>', '', self.results)
        self.results = re.sub('<p>', '', self.results)
        self.results = re.sub('</span>', '', self.results)
        self.results = re.sub('</a>', '', self.results)
        self.results = re.sub('<em>', '', self.results)
        self.results = re.sub('<b>', '', self.results)
        self.results = re.sub('</b>', '', self.results)
        self.results = re.sub('</em>', '', self.results)
        self.results = re.sub('%2f', ' ', self.results)
        self.results = re.sub('%3a', ' ', self.results)
        self.results = re.sub('<strong>', '', self.results)
        self.results = re.sub('</strong>', '', self.results)
        self.results = re.sub('<wbr>', '', self.results)
        self.results = re.sub('</wbr>','', self.results)
        
        for e in ('>', ':', '=', '<', '/', '\\', ';', '&', '%3A', '%3D', '%3C'):
            self.results = str.replace(self.results, e, ' ')
        
    def emails(self):
        self.genericClean()
        reg_emails = re.compile(
            '[a-zA-Z0-9.\-_+#~!$&\',;=:]+' +
            '@' +
            '[a-zA-Z0-9.-]*' +
            self.word)
        self.temp = reg_emails.findall(self.results)
        emails = self.unique()
        return emails
    
    def unique(self):
        self.new = list(set(self.temp))
        return self.new
    
    
###################################################################

class SearchEngine:
    def __init__(self, urlPattern, word, limit, counterInit, counterStep, userAgent, proxy):
        self.results = ""
        self.totalresults = ""
        self.userAgent = userAgent
        self.limit = int(limit)
        self.counter = int(counterInit)
        self.urlPattern = urlPattern
        self.step = int(counterStep)
        self.word = word
        self.proxy = proxy
        
    def do_search(self):
        try:
            urly = self.urlPattern.format(counter=str(self.counter), word=self.word)
            headers = {
                'User-Agent': self.userAgent,
            }

            if(self.proxy):
                proxies = {
                  self.proxy.scheme: "http://" + self.proxy.netloc
                }
                r=requests.get(urly, headers=headers, proxies=proxies)
            else:
                r=requests.get(urly, headers=headers)
                
        except Exception as e:
            print(e)
            sys.exit(4)
        
        self.results = r.content.decode(r.encoding)
        self.totalresults += self.results
    
    def process(self):
        while (self.counter < self.limit):
            self.do_search()
            time.sleep(1)
            self.counter += self.step
            print(green("\tSearching " + str(self.counter) + " results..."))
            
    def get_emails(self):
        rawres = myparser(self.totalresults, self.word)
        return rawres.emails()    
    
###################################################################

def yellow(text):
    return colored(text, 'yellow', attrs=['bold'])

def green(text):
    return colored(text, 'green', attrs=['bold'])

def blue(text):
    return colored(text, 'blue', attrs=['bold'])

def red(text):
    return colored(text, 'red', attrs=['bold'])

def unique(data):
        return list(set(data))

def checkProxyUrl(url):
    url_checked = urlparse(url)
    if (url_checked.scheme not in ('http', 'https')) | (url_checked.netloc == ''):
        raise argparse.ArgumentTypeError('Invalid {} Proxy URL (example: http://127.0.0.1:8080).'.format(url))
    return url_checked
        
###################################################################

def limit_type(x):
    x = int(x)
    if x <= 0:
        raise argparse.ArgumentTypeError("Minimum results limit is 1.")
    return x

def engine_type(x):
    if x not in ("google", "bing", "yahoo", "ask", "all"):
        raise argparse.ArgumentTypeError("Invalid search engine, try with: google, bing, yahoo, ask, all.")
    return x


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
""".format(red('Version'), yellow(__version__)),                                 
                                     formatter_class=RawTextHelpFormatter)
    
    parser.add_argument("-d", '--domain', metavar='DOMAIN', dest='domain', type=str, help="Domain to search.")
    parser.add_argument("-s", '--save', metavar='FILE', dest='filename', type=str, help="Save the results into a TXT and XML file (both).")
    parser.add_argument("-e", '--engine', metavar='ENGINE', dest='engine', default="all", type=engine_type, help="Select search engine(google, bing, yahoo, ask, all).")
    parser.add_argument("-l", '--limit', metavar='LIMIT', dest='limit', type=limit_type, default=100, help="Limit the number of results.")
    parser.add_argument('-u', '--user-agent', metavar='USER-AGENT', dest='uagent', type=str, help="Set the User-Agent request header.")
    parser.add_argument('-x', '--proxy', metavar='PROXY', dest='proxy', type=checkProxyUrl, help='Setup proxy server (example: http://127.0.0.1:8080)')
    
    if len(sys.argv) is 1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()
    if not args.domain:
        print(red("[-] Please specify a domain name to search."))
        sys.exit(2)
    domain = args.domain

    userAgent = (args.uagent or
                 "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1")
    
    print("User-Agent in use: {}".format(yellow(userAgent)))
    
    if args.proxy:
        print("Proxy server in use: {}".format(yellow(args.proxy.scheme + "://" + args.proxy.netloc)))

    filename = args.filename or ""
    limit = args.limit        
    engine = args.engine

    googleUrl = 'http://www.google.com/search?num=100&start={counter}&hl=en&q=%40"{word}"'
    bingUrl = "http://www.bing.com/search?q=%40{word}&count=50&first={counter}"
    askUrl = "http://www.ask.com/web?q=%40{word}"
    yahooUrl = "http://search.yahoo.com/search?p=%40{word}&n=100&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b={counter}"
    
    if engine == "google":
        print(green("[+] Searching in Google..\n"))
        search = SearchEngine(googleUrl, domain, limit, 0, 100, userAgent, args.proxy)
        search.process()
        all_emails = search.get_emails()
        
    elif engine == "bing":
        print(green("[+] Searching in Bing..\n"))
        search = SearchEngine(bingUrl, domain, limit, 0, 50, userAgent, args.proxy)
        search.process()
        all_emails = search.get_emails()
        
    elif engine == "ask":
        print(green("[+] Searching in ASK..\n"))
        search = SearchEngine(askUrl, domain, limit, 0, 100, userAgent, args.proxy)
        search.process()
        all_emails = search.get_emails()
        
    elif engine == "yahoo":
        print(green("[+] Searching in Yahoo..\n"))
        search = SearchEngine(yahooUrl, domain, limit, 1, 100, userAgent, args.proxy)
        search.process()
        all_emails = search.get_emails()
        
    elif engine == "all":
        print(green("[+] Searching everywhere..\n"))
        all_emails = []
        print(green("[+] Searching in Google..\n"))
        search = SearchEngine(googleUrl, domain, limit, 0, 100, userAgent, args.proxy)
        search.process()
        all_emails.extend(search.get_emails())
        print(green("\n[+] Searching in Bing..\n"))
        search = SearchEngine(bingUrl, domain, limit, 0, 50, userAgent, args.proxy)
        search.process()
        all_emails.extend(search.get_emails())
        print(green("\n[+] Searching in ASK..\n"))
        search = SearchEngine(askUrl, domain, limit, 0, 100, userAgent, args.proxy)
        search.process()
        all_emails.extend(search.get_emails())
        print(green("\n[+] Searching in Yahoo..\n"))
        search = SearchEngine(yahooUrl, domain, limit, 1, 100, userAgent, args.proxy)
        search.process()
        all_emails.extend(search.get_emails())
        all_emails = unique(all_emails)
    
    print(green("\n\n[+] Emails found:"))
    print(green("-" * 18))
    
    if not all_emails:
        print(red("No emails found"))
        sys.exit(3)
    else:
        for emails in all_emails:
            print(emails)
            
    if filename:
        try:
            print(green("[+] Saving files..."))
            with open(filename, 'w') as out_file:
                for email in all_emails:
                    try:
                        out_file.write(email + "\n")
                    except:
                        print(red("Exception " + email))
        except Exception as e:
            print(red("Error saving TXT file: " + e))
            
        try:
            filename = filename.split(".")[0] + ".xml"
            with open(filename, 'w') as out_file:
                out_file.write('<?xml version="1.0" encoding="UTF-8"?><EmailHarvester>')
                for x in all_emails:
                    out_file.write('<email>{}</email>'.format(x))
                out_file.write('</EmailHarvester>')
            print(green("Files saved!"))
        except Exception as er:
            print(red("Error saving XML file: " + er))

