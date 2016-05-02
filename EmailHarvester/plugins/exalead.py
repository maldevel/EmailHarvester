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
from EmailHarvester.core.plugin import Plugin


class ExaleadPlugin(Plugin):
    url = "http://www.exalead.com/search/web/results/?q=%40{word}&elements_per_page=10&start_index={counter}"
    start = 0
    step = 50

    def __init__(self, domain, limit, proxy, user_agent):
        Plugin.__init__(self, url=self.url, word=domain,
                        limit=limit, start=self.start, step=self.step,
                        name=__name__, proxy=proxy, user_agent=user_agent)

    def run(self):
        self.process()
        return self.get_emails()


def start(domain, limit, proxy, user_agent):
    plugin = ExaleadPlugin(domain, limit, proxy, user_agent)
    return plugin.run()
