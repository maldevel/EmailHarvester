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

from com.core.SearchEngine import SearchEngine
from com.plugins.SocialNetworks import SocialNetworks


class Exalead(SearchEngine):
    def __init__(self, site=None):
        if site is None:
            url_dict = {
                "Exalead": {"url": "http://www.exalead.com/search/web/results/?q=%40{word}&elements_per_page=50&start_index={counter}",
                           "init": 0,
                           "step": 50}
            }
        else:
            url_dict = {
                site: {
                    "url": "http://www.exalead.com/search/web/results/?q=site%3A" +
                           SocialNetworks.get_all()[site] + "+%40{word}&elements_per_page=50&start_index={counter}",
                    "init": 0,
                    "step": 50}
            }
        super().__init__(url_dict)

