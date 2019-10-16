# Global Benchmark Database (GBD)
# Copyright (C) 2019 Markus Iser, Luca Springer, Karlsruhe Institute of Technology (KIT)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3
from os.path import isfile

from gbd_tool.hashing.gbd_hash import HASH_VERSION
from gbd_tool.util import eprint

VERSION = 0


class DatabaseException(Exception):
    pass


class Database:

    def __init__(self, path):
        self.create_mode = not isfile(path)
        self.path = path
        # init connections
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.inlining_connection = sqlite3.connect(path)
        self.inlining_connection.row_factory = lambda cursor, row: row[0]
        # create mode
        if self.create_mode:
            eprint("Initializing DB with version {} and hash-version {}".format(VERSION, HASH_VERSION))
            self.init(VERSION, HASH_VERSION)
        # version check
        self.version_check()
        if not self.has_table('benchmarks'):
            raise DatabaseException('Table benchmarks is missing in db {}, initialization error?'.format(path))

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.commit()
        self.connection.close()
        self.inlining_connection.close()

    def init(self, version, hash_version):
        self.submit("CREATE TABLE __version (entry UNIQUE, version INT, hash_version INT)")
        self.submit(
            "INSERT INTO __version (entry, version, hash_version) VALUES (0, {}, {})".format(version, hash_version))
        self.submit("CREATE TABLE benchmarks (hash TEXT NOT NULL, value TEXT NOT NULL)")

    def has_table(self, name):
        return len(self.value_query("SELECT * FROM sqlite_master WHERE tbl_name = '{}'".format(name))) != 0

    def get_version(self):
        if self.has_table('__version'):
            return self.value_query("SELECT version FROM __version").pop()
        else:
            return 0

    def get_hash_version(self):
        if self.has_table('__version'):
            return self.value_query("SELECT hash_version FROM __version").pop()
        else:
            return 0

    def value_query(self, q):
        cur = self.inlining_connection.cursor()
        lst = cur.execute(q).fetchall()
        return set(lst)

    def query(self, q):
        return self.cursor.execute(q).fetchall()

    def submit(self, q):
        eprint(q)
        self.cursor.execute(q)
        self.commit()

    def bulk_insert(self, table, lst):
        self.cursor.executemany("INSERT INTO {} VALUES (?,?)".format(table), lst)

    def version_check(self):
        if self.get_version() != VERSION:
            raise DatabaseException(
                "Version Mismatch. DB Version is at {} but script version is at {}".format(self.get_version(), VERSION))
        if self.get_hash_version() != HASH_VERSION:
            raise DatabaseException(
                "Hash-Version Mismatch. DB Hash-Version is at {} but script hash-version is at {}".format(
                    self.get_hash_version(), HASH_VERSION))

    def commit(self):
        self.connection.commit()
