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
from EmailHarvester.core.plugin import Plugin
from EmailHarvester.core.output import alert
from EmailHarvester.core.output import message


class InstagramPlugin(Plugin):
    engines = [
        {
            "name": "yahoo",
            "url": "http://search.yahoo.com/search?p=site%3Ainstagram.com+%40{word}&n=100&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b={counter}",
            "step": 100
        },
        {
            "name": "bing",
            "url": "http://www.bing.com/search?q=site%3Ainstagram.com+%40{word}&count=50&first={counter}",
            "step": 50
        },
        {
            "name": "google",
            "url": 'https://www.google.com/search?num=100&start={counter}&hl=en&q=site%3Ainstagram.com+"%40{word}"',
            "step": 100
        },
        {
            "name": "baidu",
            "url": 'http://www.baidu.com/search/s?wd=site%3Ainstagram.com+"%40{word}"&pn={counter}',
            "step": 10
        },
        {
            "name": "exalead",
            "url": "http://www.exalead.com/search/web/results/?q=site%3Ainstagram.com+%40{word}&elements_per_page=10&start_index={counter}",
            "step": 50
        },
    ]

    def __init__(self, domain, limit, proxy, user_agent):
        Plugin.__init__(self, url=self.url, word=domain,
                        limit=limit, start=self.start, step=self.step,
                        name=__name__, proxy=proxy, user_agent=user_agent)

    def process(self):
        while self.start < self.limit:
            self.search()
            time.sleep(1)
            self.start += self.step
            message("\tSearching {0} results...".format(self.start))

    def run(self):
        results = []
        for engine in self.engines:
            self.initialize(engine)
            alert("\n[+] Searching in {0} + Instagram..\n".format(engine["name"]))
            self.process()
            results.extend(self.get_emails())

        return results


def start(domain, limit, proxy, user_agent):
    plugin = InstagramPlugin(domain, limit, proxy, user_agent)
    return plugin.run()
