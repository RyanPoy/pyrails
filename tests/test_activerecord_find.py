#coding: utf8

# The MIT License (MIT)
#
# Copyright (c) 2013 PengYi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from pyrails.tests import create_table, drop_table
from pyrails.activerecord import ActiveRecord
from pyrails.activesupport import RecordNotFound
import unittest


class ActiveRecordFindTest(unittest.TestCase):

    def setUp(self):
        self.user_table_name = 'users'
        drop_table(self.user_table_name)
        create_table("""
create table if not exists %s (
    id int auto_increment,
    username varchar(32) not null,
    age int default 0,
    password varchar(32),
    PRIMARY KEY (id)
);""" % self.user_table_name)
        
    def tearDown(self):
        drop_table(self.user_table_name)

    def test_find_one(self):
        class User(ActiveRecord): pass
        User.create(username="abc", password="123")
        User.create(username="efg", password="456")
        u = User.find(1)
        self.assertEqual('abc', u.username)
        self.assertEqual('123', u.password)

    def test_find_some(self):
        class User(ActiveRecord): pass
        User.create(username="abc", password="123")
        User.create(username="efg", password="456")

        us = User.find(1, 2)
        self.assertEqual(2, len(us))

        self.assertEqual('abc', us[0].username)
        self.assertEqual('123', us[0].password)

        self.assertEqual('efg', us[1].username)
        self.assertEqual('456', us[1].password)

    def test_should_throw_exception_if_can_not_found(self):
        class User(ActiveRecord): pass
        self.assertRaises(RecordNotFound, User.find, 1)
        
        User.create(username="abc", password="123")
        self.assertRaises(RecordNotFound, User.find, 1, 2)

    def test_find_method_missing(self):
        class User(ActiveRecord): pass
        User.create(username="abc", password="123")
        User.create(username="efg", password="456")

        u = User.find_by_username_and_password('efg', '456')
        self.assertEqual('efg', u.username)
        self.assertEqual('456', u.password)


if __name__ == '__main__':
    unittest.main()
