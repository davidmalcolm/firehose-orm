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
#engine = create_engine('sqlite:///:memory:', echo=True)
#engine = create_engine('sqlite:///:memory:')
#engine = create_engine('sqlite:///test.sql', echo=True)
engine = create_engine('sqlite:///test.sql')

engine.execute("select 1").scalar()

from orm import metadata
from firehose.report import Analysis, Result, Issue, Failure

############################################################################


# Make a sessionmaker:
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

############################################################################

# Make a session:
session = Session()

############################################################################

#print(session.query(Result).count()) # FIXME: seems to be getting issues wrong
#print(session.query(Issue).count()) # FIXME: seems to be getting issues wrong
#print(session.query(Issue).first())
#print(session.query(Failure).count())
#print(session.query(Analysis).first())
#print(session.query(Failure).first())
#print(session.query(Failure).group_by(Failure.failureid))
print(session.query(Failure).filter(Failure.failureid=='python-exception').all())

