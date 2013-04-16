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

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)
#engine = create_engine('sqlite:///:memory:')
#engine = create_engine('sqlite:///test.sql', echo=True)

# Verify the connection to the DB:
engine.execute("select 1").scalar()

from orm import metadata
from firehose.model import Analysis, Issue, Failure, Info


# Create tables:
metadata.create_all(engine)

############################################################################


# Make a sessionmaker:
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

############################################################################

# Make a session:
session = Session()

# Use them
def simple_tests():
    ex = Analysis.from_xml('../firehose/examples/example-1.xml')
    print(ex)
    session.add(ex)
    print(ex.id)
    print(session.query(Analysis).first())
    print(session.query(Failure).first())
    print(ex.id)
    session.commit()

    # Do it from a new session:
    session2 = Session()
    print(session2.query(Analysis).first())
    print(session2.query(Failure).first())

# Slurp in all of the sample data:
def slurp_in_mass_run():
    import glob
    import sys
    sys.path.append('../mock-with-analysis/reports')
    from reports import get_filename, ResultsDir, AnalysisIssue, ResultDirModel, \
        AnalysisFailure, Failure

    session = Session()

    for path in glob.glob('../mock-with-analysis/fedora-17-mass-run/*/*/*/*/static-analysis'):
        print(path)
        rdir = ResultsDir(path)
        model = ResultDirModel(rdir)
        for a in model.iter_analyses():
            #print(a)
            session.add(a)

            print('#issues: %i' % session.query(Issue).count())
            print('#failures: %i' % session.query(Failure).count())
            print('#infos: %i' % session.query(Info).count())
            session.commit()

def queries():
    from pprint import pprint
    from sqlalchemy.orm import eagerload_all

    pprint(session.query(Issue).all())

simple_tests()
#slurp_in_mass_run()
queries()
