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

#config = None
app_emailharvester = None


def search(domain, limit):
    #search google+ only with google search engine
    #who is gonna have google+ indexed better than google itself?
    url = 'https://www.google.com/search?num=100&start={counter}&hl=en&q=site%3Aplus.google.com+intext:"Works at"+-inurl:photos+-inurl:about+-inurl:posts+-inurl:plusones+%40{word}'
    app_emailharvester.init_search(url, domain, limit, 0, 100, 'Google+')
    app_emailharvester.process()
    return app_emailharvester.get_emails()


class Plugin:
    def __init__(self, app, conf):#
        global app_emailharvester, config
        #config = conf
        app.register_plugin('googleplus', {'search': search})
        app_emailharvester = app
        