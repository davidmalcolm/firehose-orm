#   Copyright 2013 David Malcolm <dmalcolm@redhat.com>
#   Copyright 2013 Red Hat, Inc.
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation; either
#   version 2.1 of the License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with this library; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301
#   USA

import os
import unittest

from firehose.model import Analysis, Issue, Failure, Info

from orm import metadata

class OrmTests(unittest.TestCase):
    def setUp(self):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        # In-memory SQLite DB:
        self.engine = create_engine('sqlite:///:memory:', echo=False)

        # Create tables:
        metadata.create_all(self.engine)

        self.connection = self.engine.connect()

        # Make a sessionmaker:
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session(bind=self.connection)

    def tearDown(self):
        self.session.close()

    def roundtrip_example(self, filename):
        fullpath = os.path.join('../firehose/examples', filename) # FIXME
        a = Analysis.from_xml(fullpath)
        self.session.add(a)
        self.session.commit()

        session2 = self.Session()
        b = session2.query(Analysis).first()
        #print(b)
        self.assertEqual(a, b)

    def test_example_1(self):
        self.roundtrip_example('example-1.xml')

    def test_example_2(self):
        self.roundtrip_example('example-2.xml')

    def test_example_3(self):
        self.roundtrip_example('example-3.xml')

    def test_example_4(self):
        self.roundtrip_example('example-4.xml')

    def test_example_5(self):
        self.roundtrip_example('example-5.xml')

    def test_example_non_ascii_xml(self):
        self.roundtrip_example('example-non-ascii.xml')

if __name__ == '__main__':
    unittest.main()
