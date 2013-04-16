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

from sqlalchemy import Table, MetaData, Column, \
    ForeignKey, Integer, String, Float
from sqlalchemy.orm import mapper, relationship, polymorphic_union

metadata = MetaData()

############################################################################
from firehose.model import *

############################################################################
# Tables
############################################################################

t_analysis = \
    Table('analysis', metadata,
          Column('id', Integer, primary_key=True),
          Column('metadata_id', Integer, ForeignKey('metadata.id')),
          Column('customfields_id', Integer, ForeignKey('customfields.id')),
          )

t_metadata = \
    Table('metadata', metadata,
          Column('id', Integer, primary_key=True),
          Column('generator_id', Integer, ForeignKey('generator.id')),
          Column('sut_id', Integer, ForeignKey('sut.id')),
          Column('file_id', Integer, ForeignKey('file.id')),
          Column('stats_id', Integer, ForeignKey('stats.id')),
          )

t_stats = \
    Table('stats', metadata,
          Column('id', Integer, primary_key=True),
          Column('wallclocktime', Float),
          )

t_generator = \
    Table('generator', metadata,
          Column('id', Integer, primary_key=True),
          Column('name',  String),
          Column('version',  String),
          )

# For the Sut hierarchy we use single-table inheritance
t_sut = \
    Table('sut', metadata,
          Column('id', Integer, primary_key=True),

          Column('type', String(20), nullable=False),

          Column('name',  String),
          Column('version',  String),
          Column('release',  String),
          Column('buildarch',  String),
          )

# For the Result hierarchy we use joined-table inheritance
t_result = \
    Table('result', metadata,
          Column('result_id', Integer,
                 primary_key=True),
          Column('analysis_id', Integer, ForeignKey('analysis.id')),
          Column('type', String(10), nullable=False),
          )

t_issue = \
    Table('issue', metadata,
          Column('result_id', Integer,
                 ForeignKey('result.result_id'),
                 primary_key=True),
          Column('cwe', Integer),
          Column('testid', String),
          Column('location_id', Integer, ForeignKey('location.id')),
          Column('message_id',  Integer, ForeignKey('message.id')),
          Column('notes_id',  Integer, ForeignKey('notes.id')),
          Column('trace_id',  Integer, ForeignKey('trace.id')),
          Column('severity',  String),
          Column('customfields_id', Integer, ForeignKey('customfields.id')),
          )

t_failure = \
    Table('failure', metadata,
          Column('result_id', Integer,
                 ForeignKey('result.result_id'),
                 primary_key=True),
          Column('failureid', String),
          Column('location_id', Integer, ForeignKey('location.id')),
          Column('message_id',  Integer, ForeignKey('message.id')),
          Column('customfields_id', Integer, ForeignKey('customfields.id')),
          )

t_info = \
    Table('info', metadata,
          Column('result_id', Integer,
                 ForeignKey('result.result_id'),
                 primary_key=True),
          Column('infoid', String),
          Column('location_id', Integer, ForeignKey('location.id')),
          Column('message_id',  Integer, ForeignKey('message.id')),
          Column('customfields_id', Integer, ForeignKey('customfields.id')),
          )

t_message = \
    Table('message', metadata,
          Column('id', Integer, primary_key=True),
          Column('text', String),
          )
# ideally we should just store a String where these get used

t_notes = \
    Table('notes', metadata,
          Column('id', Integer, primary_key=True),
          Column('text', String),
          )
# ideally we should just store a String where these get used


t_trace = \
    Table('trace', metadata,
          Column('id', Integer, primary_key=True)
          )

t_state = \
    Table('state', metadata,
          Column('id', Integer, primary_key=True),
          Column('trace_id',  Integer, ForeignKey('trace.id')),
          Column('location_id', Integer, ForeignKey('location.id')),
          Column('notes_id',  Integer, ForeignKey('notes.id')),
          )

t_location = \
    Table('location', metadata,
          Column('id', Integer, primary_key=True),
          Column('file_id', Integer, ForeignKey('file.id')),
          Column('function_id', Integer, ForeignKey('function.id')),
          Column('point_id', Integer, ForeignKey('point.id')),
          Column('range_id', Integer, ForeignKey('range.id')),

          #Column('startline', Integer),
          #Column('startcol', Integer),
          #Column('endline', Integer),
          #Column('endcol', Integer),
          )

t_file = \
    Table('file', metadata,
          Column('id', Integer, primary_key=True),
          Column('givenpath', String),
          Column('abspath', String),
          Column('hash_id', Integer, ForeignKey('hash.id')),
          )
t_hash = \
    Table('hash', metadata,
          Column('id', Integer, primary_key=True),
          Column('alg', String),
          Column('hexdigest', String),
          )

t_function = \
    Table('function', metadata,
          Column('id', Integer, primary_key=True),
          Column('name', String),
          )

t_point = \
    Table('point', metadata,
          Column('id', Integer, primary_key=True),
          Column('line', Integer),
          Column('column', Integer),
          )

t_range = \
    Table('range', metadata,
          Column('id', Integer, primary_key=True),
          Column('start_id', Integer, ForeignKey('point.id')),
          Column('end_id', Integer, ForeignKey('point.id')),
          )

t_customfields = \
    Table('customfields', metadata,
          Column('id', Integer, primary_key=True))

t_intfield = \
    Table('intfield', metadata,
          Column('id', Integer, primary_key=True),
          Column('customfields_id', Integer, ForeignKey('customfields.id')),
          Column('name', String),
          Column('value', Integer),
          )

t_strfield = \
    Table('strfield', metadata,
          Column('id', Integer, primary_key=True),
          Column('customfields_id', Integer, ForeignKey('customfields.id')),
          Column('name', String),
          Column('value', String),
          )

############################################################################
# Mappers
############################################################################

mapper(Analysis, t_analysis,
       properties={
        'metadata' : relationship(Metadata),
        # FIXME: should do both issues *and* failures
        'results' : relationship(Result), #, backref='analysis', order_by=t_issue.c.id)
        'customfields' : relationship(CustomFields),
        }
       )

mapper(Metadata, t_metadata,
       properties={
        'generator' : relationship(Generator),
        'sut' : relationship(Sut),
        'file_' : relationship(File),
        'stats' : relationship(Stats),
        }
       )

mapper(Generator, t_generator)

# Map the Sut hierarchy using single table inheritance
sut_mapper = mapper(Sut, t_sut, \
    polymorphic_on=t_sut.c.type, polymorphic_identity='sut')
srpmbuild_mapper = mapper(SourceRpm,
                          inherits=sut_mapper,
                          polymorphic_identity='source-rpm')

mapper(Stats, t_stats)

mapper(Message, t_message)
mapper(Notes, t_notes)

mapper(Trace, t_trace,
       properties={
        'states' : relationship(State, backref='trace', order_by=t_state.c.id,
                                lazy='joined')
        }
       )

mapper(State, t_state,
       properties={
        'location': relationship(Location, lazy='joined'),
        'notes': relationship(Notes, lazy='joined'),
        }
       )

# Map the Result hierarchy using Joined Table Inheritance:

mapper(Result, t_result,
       polymorphic_on=t_result.c.type,
       polymorphic_identity='result')

mapper(Issue, t_issue,
       inherits=Result,
       polymorphic_identity='issue',
       properties={
        'location' : relationship(Location,
                                  backref='issues',
                                  order_by=t_location.c.id,
                                  lazy='joined'),
        'message':  relationship(Message, lazy='joined'),
        'notes':  relationship(Notes, lazy='joined'),
        'trace' : relationship(Trace, lazy='joined'),
        'customfields' : relationship(CustomFields),
        }
       )

mapper(Failure, t_failure,
       inherits=Result,
       polymorphic_identity='failure',
       properties={
       'location' : relationship(Location),
       'message' : relationship(Message),
       'customfields' : relationship(CustomFields),
       }
       )

mapper(Info, t_info,
       inherits=Result,
       polymorphic_identity='info',
       properties={
       'location' : relationship(Location),
       'message' : relationship(Message),
       'customfields' : relationship(CustomFields),
       }
       )

mapper(Location, t_location,
        properties={
        'file' : relationship(File,
                              lazy='joined'), #, backref='locations', order_by=t_file.c.abspath)
        'function' : relationship(Function, lazy='joined'),
        'point' : relationship(Point, lazy='joined'),
        'range_' : relationship(Range, lazy='joined'),
        }
       )

mapper(File, t_file,
       properties={
        'hash_' : relationship(Hash, lazy='joined'),
        }
       )
mapper(Hash, t_hash)
mapper(Function, t_function)
mapper(Point, t_point)
mapper(Range, t_range)

mapper(CustomFields, t_customfields)
