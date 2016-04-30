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

import requests
import time
import sys
from termcolor import colored

config = None
app_emailharvester = None

def green(text):
    return colored(text, 'green', attrs=['bold'])

def red(text):
    return colored(text, 'red', attrs=['bold'])

def cyan(text):
    return colored(text, 'cyan', attrs=['bold'])

class AskSearch(object):
    
    def __init__(self, url, word, limit):
        self.results = ""
        self.totalresults = ""
        self.limit = int(limit)
        self.page = 1
        self.url = url
        self.word = word
        self.proxy = config["proxy"]
        self.userAgent = config["useragent"]
        self.counter = 0
        
    def do_search(self):
        try:
            urly = self.url.format(page=str(self.page), word=self.word)
            headers = {'User-Agent': self.userAgent}
            if(self.proxy):
                proxies = {self.proxy.scheme: "http://" + self.proxy.netloc}
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
            self.counter += 10
            self.page += 1
            print(green("[+] Searching in ASK:") + cyan(" {} results".format(str(self.counter))))
            
    def get_emails(self):
        app_emailharvester.parser.extract(self.totalresults, self.word)
        return app_emailharvester.parser.emails()
    
    
def search(domain, limit):
    url = "http://www.ask.com/web?q=%40{word}&page={page}"
    search = AskSearch(url, domain, limit)
    search.process()
    return search.get_emails()


class Plugin:
    def __init__(self, app, conf):
        global app_emailharvester, config
        config = conf
        app.register_plugin('ask', {'search': search})
        app_emailharvester = app
        