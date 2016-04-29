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



################################
import os

from sys import platform as _platform

from core import colors
from core.output import save
from core.output import stdout_print
import core.parameters as parameters
from core.plugins import *
from core.plugins import Plugins
from core.commons import unique


if _platform == 'win32':
    import colorama
    colorama.init()


class Launcher():
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
    all_emails = []
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
            print(colors.red("[-] Please specify a domain name to search."))
            sys.exit(2)
        self.domain = self.args.domain

    def setup_user_agent(self):
        self.user_agent = (self.args.uagent or
                     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1")

        print("User-Agent in use: {}".format(colors.yellow(self.user_agent)))

    def setup_proxy(self):
        if self.args.proxy:
            print("Proxy server in use: {}".format(
                colors.yellow(self.args.proxy.scheme + "://" + self.args.proxy.netloc))
            )
        self.proxy = self.args.proxy

    def setup_exclude(self):
        if self.args.exclude:
            self.excluded = self.args.exclude.split(',')

    def search(self):
        if self.engine == "all":
            print(colors.green("[+] Searching everywhere.."))
            for search_engine in self.plugins:
                if search_engine in self.excluded:
                    continue
                self.all_emails += self.plugins.execute(search_engine,
                                                   self.domain,
                                                   self.limit,
                                                   self.proxy,
                                                   self.user_agent)
        elif self.engine not in self.plugins:
            print(colors.red("Search engine plugin not found"))
            sys.exit(3)
        else:
            self.all_emails = self.plugins.execute(self.engine,
                                                   self.domain,
                                                   self.limit,
                                                   self.proxy,
                                                   self.user_agent)

    def run(self):
        print(self.plugins)

        self.search()
        if not self.all_emails:
            print(colors.red("\nNo emails found!"))
            sys.exit(4)

        msg = "\n\n[+] {} emails found:".format(len(self.all_emails))
        print(colors.green(msg))
        print(colors.green("-" * len(msg)))

        if not self.args.noprint:
            stdout_print(unique(self.all_emails))

        save(self.filename, unique(self.all_emails))


if __name__ == '__main__':
    launcher = Launcher()
    launcher.run()
    


