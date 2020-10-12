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
import os
import sys
import time
import logging

import requests

from .colors import cyan, green
from .parser import MyParser


class EmailHarvester(object):
    logger = logging.getLogger(__name__ + '.EmailHarvester')
    
    def __init__(self, user_agent, proxy, stdout=False):
        self.plugins = {}
        self.proxy = proxy
        self.user_agent = user_agent
        self.parser = MyParser()
        self.active_engine = "None"
        self.results = None
        self.total_results = None
        self.limit = None
        self.counter = None
        self.url = None
        self.step = None
        self.stdout = stdout
        self.word = None
        
        path = os.path.dirname(os.path.abspath(__file__)) + "/plugins/"
        plugins = {}
        
        sys.path.insert(0, path)
        for f in os.listdir(path):
            f_name, ext = os.path.splitext(f)
            if ext == '.py':
                mod = __import__(f_name, fromlist=[''])
                plugins[f_name] = mod.Plugin(self, {'useragent': user_agent, 'proxy': proxy})
    
    def register_plugin(self, search_method, functions):
        self.plugins[search_method] = functions
        
    def get_plugins(self):
        return self.plugins
        
    def init_search(self, url, word, limit, counterInit, counterStep, engineName):
        self.results = ""
        self.total_results = ""
        self.limit = int(limit)
        self.counter = int(counterInit)
        self.url = url
        self.step = int(counterStep)
        self.word = word
        self.active_engine = engineName
        
    def do_search(self):
        try:
            url = self.url.format(counter=str(self.counter), word=self.word)
            headers = {'User-Agent': self.user_agent}
            if self.proxy:
                proxies = {self.proxy.scheme: "http://" + self.proxy.netloc}
                r = requests.get(url, headers=headers, proxies=proxies)
            else:
                r = requests.get(url, headers=headers)
                
        except Exception as e:
            if self.stdout:
                print(e)
            else:
                self.logger.error(e)
            # Should never really call sys.exit from a module. Future refactor needed
            sys.exit(4)

        if r.encoding is None:
            r.encoding = 'UTF-8'

        self.results = r.content.decode(r.encoding)
        self.total_results += self.results
    
    def process(self):
        while self.counter < self.limit:
            self.do_search()
            time.sleep(1)
            self.counter += self.step
            if self.stdout:
                print(green("[+] Searching in {}:".format(self.active_engine)) +
                      cyan(" {} results".format(str(self.counter))))
            else:
                self.logger.info('[+] Searching in {}: {} results'.format(self.active_engine, self.counter))
            
    def get_emails(self):
        self.parser.extract(self.total_results, self.word)
        return self.parser.emails()
