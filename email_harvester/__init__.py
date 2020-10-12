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
import logging
from sys import platform
from logging import NullHandler

from .parser import MyParser
from .harvester import EmailHarvester


logging.getLogger(__name__).addHandler(NullHandler())

if platform == 'win32':
    import colorama
    colorama.init()

__author__ = "maldevel"
__copyright__ = "Copyright (c) 2016 @maldevel"
__credits__ = ["maldevel", "PaulSec", "cclauss", "Christian Martorella"]
__license__ = "GPLv3"
__version__ = "1.3.2"
__maintainer__ = "maldevel"
