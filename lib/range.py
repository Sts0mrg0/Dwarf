"""
Dwarf - Copyright (C) 2018 iGio90

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""


class Range(object):
    def __init__(self, app):
        super().__init__()

        self.app = app

        self.base = 0
        self.size = 0
        self.tail = 0
        self.data = bytes()

        self.start_address = 0

    def invalidate(self):
        self.base = 0
        self.size = 0
        self.tail = 0
        self.data = bytes()

        self.start_address = 0

    def init_with_address(self, address):
        if isinstance(address, str):
            if address.startswith('0x'):
                self.start_address = int(address, 16)
            else:
                self.start_address = int(address)
        else:
            self.start_address = address

        if self.base > 0:
            if self.base < self.start_address < self.tail:
                return -1

        try:
            range = self.app.dwarf_api('getRange', address)
        except:
            return 1

        if range is None or len(range) == 0:
            return 1

        self.base = int(range['base'], 16)
        self.size = range['size']
        self.tail = self.base + self.size
        self.data = self.app.dwarf_api('readBytes', [self.base, self.size])
        if self.data is None:
            self.data = bytes()
            return 1
        if len(self.data) == 0:
            return 1
        return 0
