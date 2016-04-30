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
import time
import requests
import sys
from core.plugin import Plugin
from core.output import error
from core.output import message
from core.output import alert


class AskPlugin(Plugin):
    url = "http://www.ask.com/web?q=%40{word}&page={page}"
    step = 10
    page = 1

    def __init__(self, domain, limit, proxy, user_agent):
        Plugin.__init__(self, url=self.url, word=domain,
                        limit=limit, start=self.start, step=self.step,
                        name=__name__, proxy=proxy, user_agent=user_agent)

    def search(self):
        try:
            url = self.url.format(page=str(self.page), word=self.word)
            headers = {'User-Agent': self.user_agent}
            if self.proxy:
                proxies = {self.proxy.scheme: "http://" + self.proxy.netloc}
                req = requests.get(url, headers=headers, proxies=proxies)
            else:
                req = requests.get(url, headers=headers)

        except Exception as e:
            error(e)
            sys.exit(4)

        self.results += req.content.decode(req.encoding)

    def process(self):
        alert("\n[+] Searching in {0}..\n".format(self.name))
        while self.start < self.limit:
            self.search()
            time.sleep(1)
            self.start += self.step
            self.page += 1
            message("\tSearching {0} results...".format(self.start))

    def run(self):
        self.process()
        return self.get_emails()


def start(domain, limit, proxy, user_agent):
    plugin = AskPlugin(domain, limit, proxy, user_agent)
    return plugin.run()
