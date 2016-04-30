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
from sys import platform as _platform

from core.output import File
from core.output import message
from core.output import alert
from core.output import warning
from core.output import error
import core.parameters as parameters
from core.plugins import *
from core.plugins import Plugins
from core.commons import unique
import core.settings as settings


if _platform == 'win32':
    import colorama
    colorama.init()


class Launcher:
    parser = None
    args = None
    domain = None
    user_agent = None
    proxy = None
    filename = None
    limit = None
    engine = None
    app = None
    plugins = None
    results = []
    excluded = []

    def __init__(self):
        self.parser = parameters.setup()
        self.args = self.parser.parse_args()
        self.setup_plugins()
        self.setup_domain()
        self.setup_user_agent()
        self.setup_proxy()
        self.filename = self.args.filename or ""
        self.limit = self.args.limit
        self.engine = self.args.engine

    def setup_plugins(self):
        self.plugins = Plugins()
        if self.args.listplugins:
            self.plugins.display()

    def setup_domain(self):
        if not self.args.domain:
            error("[-] Please specify a domain name to search.")
            sys.exit(2)
        self.domain = self.args.domain

    def setup_user_agent(self):
        self.user_agent = (self.args.uagent or settings.DFAULT_USER_AGENT)
        message("User-Agent in use: {}".format(self.user_agent))

    def setup_proxy(self):
        if self.args.proxy:
            msg = "Proxy server in use: {0}://{1}".format(
                self.args.proxy.scheme,
                self.args.proxy.netloc
            )
            warning(msg)
        self.proxy = self.args.proxy

    def setup_exclude(self):
        if self.args.exclude:
            self.excluded = self.args.exclude.split(',')

    def search(self):
        if self.engine == "all":
            alert("[+] Searching everywhere..")
            for search_engine in self.plugins:
                if search_engine in self.excluded:
                    continue
                self.results += self.plugins.execute(search_engine,
                                                     self.domain,
                                                     self.limit,
                                                     self.proxy,
                                                     self.user_agent)
        elif self.engine not in self.plugins:
            error("Search engine plugin not found")
            sys.exit(3)
        else:
            self.results = self.plugins.execute(self.engine,
                                                self.domain,
                                                self.limit,
                                                self.proxy,
                                                self.user_agent)
        self.results = unique(self.results)

    def display_results(self):
        if not self.results:
            error("\nNo emails found!")
            sys.exit(4)

        alert("\n\n[+] {} emails found:".format(len(self.results)), underline=True)

        if not self.args.noprint:
            message(self.results)

    def save(self):
        if not self.filename:
            return
        save_file = File(self.filename, self.results)
        save_file.save()

    def run(self):
        self.search()
        self.display_results()
        self.save()


if __name__ == '__main__':
    launcher = Launcher()
    launcher.run()
    


