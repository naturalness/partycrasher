#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function, unicode_literals, division

"""
Print descriptive statistics of launchpad data.

Mostly deals with recursion stuff.
"""

import csv
import json
import os
import sqlite3
import sys

from collections import namedtuple, OrderedDict, Counter
from itertools import islice, tee
from json import JSONDecoder

import regex
import six

from six import iterkeys, itervalues, iteritems
from six.moves import cPickle as pickle
from six.moves import zip as izip

from path import Path


SCHEMA = r"""
-- Stores the database ID, its JSON representation, and the oracle bucket ID.
CREATE TABLE IF NOT EXISTS crash(
    id          TEXT,
    json        BLOB, -- UTF-8 blob.
    bucket_id   TEXT
);

-- Allow indexing by database_id.
CREATE INDEX IF NOT EXISTS crash_id ON crash (id);

-- Stores instances of recursion.
CREATE TABLE IF NOT EXISTS recursion(
    crash_id    TEXT,
    depth       INTEGER, -- At what depth was the first recursion stack frame
                         -- found? 0 = top of the stack; N = bottom of stack
                         -- (usually main() or start())
    length      INTEGER  -- How many frames of recursion are there?
);

-- Allow indexing by database_id.
CREATE INDEX IF NOT EXISTS recursion_crash_id ON recursion (crash_id);

-- TODO: Store bucket field? Is there enough justification for it?
"""

# Decodes JSON Objects as ordered dictionaries (sometimes order matters).
json_decoder = JSONDecoder(object_pairs_hook=OrderedDict)


def dbg(message, **kwargs):
    """
    Prints loud and obnoxious debug messages.

    Keyword arguments are passed to str.format()
    """
    ITALIC = "\x1b[3m"
    YELLOW = "\x1b[33m"
    RESET = "\x1b[m"
    print(ITALIC, YELLOW, six.text_type(message).format(**kwargs), RESET,
          file=sys.stderr, sep='')


def bigrams(seq):
    """
    Yields bigrams from the given sequence.

    >>> list(bigrams(range(4)))
    [(0, 1), (1, 2), (2, 3)]
    """
    first, second = tee(seq, 2)
    second = islice(second, 1, None)
    return izip(first, second)



# Base class for the stack frame; does not include spiffy methods.
BaseStackFrame = namedtuple('BaseStackFrame', [
    'module', 'function', 'arguments', 'filename', 'line_number', 'address'
])


class StackFrame(BaseStackFrame):
    """
    A single stack frame or execution frame. This is usually a function call,
    or the site of an exception.

    >>> arguments = []
    >>> arguments.extend(["data", "__init__", map(str, arguments), "data.py", 29, 211])
    >>> sf = StackFrame(*arguments)
    """
    def __init__(self, module, function, arguments, filename, line_number, address):
        """
        Assert the integrity of the data.
        """
        if module is not None:
            assert isinstance(module, str)
        if function is not None:
            assert isinstance(function, str)
        if arguments is not None:
            assert iter(arguments)
            # TODO: enforce all arguments to be str? assert all([isinstance(arg, str) for arg in arguments])
        if filename is not None:
            assert isinstance(filename, str)
        if line_number is not None:
            assert isinstance(line_number, int)
        if address is not None:
            assert isinstance(address, int)
            assert 0 <= address <= 2**64-1

    def to_dict(self):
        """
        Returns the contents of this as a dictionary.
        """
        # Delegate to namedtuple interface.
        return self._asdict()

    @classmethod
    def of(cls, module=None, function=None, arguments=None, filename=None,
           line_number=None, address=None):
        return cls(module=module, function=function, arguments=arguments,
                   filename=filename, line_number=line_number,
                   address=address)


class StackTrace(object):
    """
    Ordered series of stack frames. The first (index zero) stack frame is the
    site of the exception. This is also known as the top of the stack. The
    last (index len(stack_trace) - 1) is usually the start of the thread.
    """

    def __init__(self, stack_frames):
        self._stack = tuple(stack_frames)
        assert all(isinstance(thing, StackFrame) for thing in self._stack)

    def __repr__(self):
        frames = ", ".join(repr(frame) for frame in self._stack)
        return "{cls}([{frames}])".format(cls=self.__class__.__name__,
                                          frames=frames)

    # Delegate sequence methods to the underlying immutable sequence of StackFrames
    def __getitem__(self, index):
        return self._stack[index]

    def __iter__(self):
        return iter(self._stack)

    def __len__(self):
        return len(self._stack)


class Crash(object):
    """
    Represents one full crash, complete with stack trace.
    """

    def __init__(self, report_id, project, stack_frames, metadata=()):
        """
        TODO:
            - exception
            - report ID
            - operating system
            - build
        """
        self.id = report_id
        self.project = project or "<unknown>"
        self._stack = StackTrace(stack_frames)
        if isinstance(metadata, OrderedDict):
            self._meta = metadata
        else:
            self._meta = OrderedDict(metadata)

    def __getitem__(self, index):
        """
        Returns a stack frame.
        """
        if isinstance(index, str):
            return self._meta[index]
        elif isinstance(index, int):
            return self._stack[index]
        else:
            raise IndexError('Not sure how to handle index: {!r}'.format(index))

    def __getattr__(self, name):
        """
        Attempts to find unknown attributes as names.
        """
        if name.startswith('_'):
            # Prevent special Python object look-up
            raise AttributeError(name)

        return self._meta[name]

    @property
    def stack_trace(self):
        """
        The crash's stack trace. Read-only.
        """
        return self._stack

    @property
    def context(self):
        return self._meta

    def __repr__(self):
        template = "{cls}({id!r}, {project!r}, {frames!r}, metadata={metadata!r})"
        return template.format(cls=self.__class__.__name__,
                               id=self.id,
                               frames=self._stack,
                               project=self.project,
                               metadata=self.context)

    @classmethod
    def parse(cls, report_id, raw_crash):
        project = raw_crash.pop('project')
        del raw_crash['extra']
        del raw_crash['database_id']

        crash = cls(report_id, project)
        stack = raw_crash.pop('stacktrace', [])
        crash.stack.extend(StackFrame.parse(frame) for frame in stack)
        crash.context.update(raw_crash)

        return crash

    @property
    def has_recursion(self):
        """
        >>> crash = Crash('0')
        >>> crash.stack.append(StackFrame.of(function='main'))
        >>> crash.has_recursion
        False

        >>> crash.stack.append(StackFrame.of(function='init'))
        >>> crash.has_recursion
        False

        >>> crash = Crash('1')
        >>> crash.stack.append(StackFrame.of(function='log'))
        >>> crash.stack.append(StackFrame.of(function='fib'))
        >>> crash.stack.append(StackFrame.of(function='fib'))
        >>> crash.stack.append(StackFrame.of(function='main'))
        >>> crash.has_recursion
        True

        """
        return self.max_recursion_depth > 0

    @property
    def max_recursion_depth(self):
        recursion_depth = [0]

        for a, b in bigrams(self.stack):
            saw_recursion = False
            if a.function:
                if a.function == b.function:
                    recursion_depth[-1] += 1
                    saw_recursion = True

            if not saw_recursion and recursion_depth[-1] > 0:
                #dbg("Recursion in {crash}: {func}", crash=self.id, func=a.function)
                recursion_depth.append(0)

        return max(recursion_depth)


def to_address(value):
    if value is None:
        return None
    try:
        return int(value, base=16)
    except ValueError:
        return None


def decode_json(string):
    """
    Decodes a JSON string correctly for use with parse_crash.
    """
    assert isinstance(string, str)
    return json_decoder.decode(string)


def parse_crash(raw_crash):
    """
    Parses a string or OrderedDict into a Crash instance.
    """
    # Automatically parse a JSON string.
    if isinstance(raw_crash, str):
        raw_crash = decode_json(raw_crash)

    # Get rid of the report id, stacktrace, and project.
    # TODO: date ingested
    raw_stack_trace = raw_crash.pop('stacktrace', [])
    report_id = raw_crash.pop('database_id')
    project = raw_crash.pop('project', None)
    del raw_crash['extra']

    stack_trace = [
        StackFrame(function=frame.get('function'),
                   arguments=frame.get('args'),
                   module=frame.get('dylib'),
                   address=to_address(frame.get('address')),
                   filename=frame.get('file'),
                   line_number=None)
        for frame in raw_stack_trace
    ]

    return Crash(report_id, project, stack_trace, metadata=raw_crash)


class CrashInfo:
    """
    A bunch of info about a crash including its bucket assignment.
    """
    __slots__ = ('id', '_json', '_crash', 'bucket_id')

    def __init__(self, report_id, json, bucket_id):
        self.id = report_id
        self._crash = None
        self._json = json
        self.bucket_id = bucket_id

    @property
    def crash(self):
        if self._crash is None:
            self._crash = parse_crash(self._json)
            self._json = None
        return self._crash


class Corpus:
    """
    Represents a corpus, backed by a database file.

    Use indexing operators to get a specific crash.
    """
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file)
        self.conn.executescript(SCHEMA)

    def __iter__(self):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT id, json, bucket_id FROM crash '
            'ORDER BY rowid'
        )
        return (CrashInfo(*data) for data in cursor.fetchall())

    def __len__(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM crash')
        # Unpack the tuple.
        result, = cursor.fetchone()
        return result
        return

    def __getitem__(self, database_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT id, json, bucket_id FROM crash'
            ' WHERE id = :id', {'id': database_id}
        )
        report_id, crash_json, bucket_id = cursor.fetchone()
        return CrashInfo(report_id, crash_json, bucket_id)

    def __repr__(self):
        return "Corpus({!r})".format(self.conn)

    def insert_crash(self, report_id, crash, bucket_id):
        """
        Inserts a parsable crash into the database.
        """
        assert not isinstance(crash, str)
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                'INSERT INTO crash (id, json, bucket_id) VALUES'
                ' (?, ?, ?)', (report_id, json.dumps(crash), bucket_id)
            )
            # TODO: also, figure out recursion!

    def count_buckets(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(DISTINCT bucket_id) FROM crash')
        # Unpack the tuple.
        result, = cursor.fetchone()
        return result

    @classmethod
    def from_json(cls, json_filename, db_filename='crashes.sqlite'):
        """
        Parses JSON creating a database.
        """

        json_filename = Path(json_filename)
        db_filename = Path(db_filename)

        if not db_filename.exists():
            pass
        elif db_filename.mtime > json_filename.mtime:
            return Corpus(db_filename)

        # Autovivify the corpus
        corpus = Corpus(db_filename)

        # Parse the JSON.
        data = load_oracle_data(json_filename, should_parse=False)
        crashes, _oracle_all, crash2bucket, _total_ids, _total_buckets = data

        for report_id, bucket_id in crash2bucket.items():
            if report_id not in crashes:
                continue
            corpus.insert_crash(report_id, crashes[report_id], bucket_id)

def load_from_json(filename):
    dbg("Loading {filename}...", filename=filename)

    with open(filename, 'r') as jsonfile:
        database = json.load(jsonfile)

    dbg("Loaded {size} bytes of content.", size=sys.getsizeof(database, '???'))

    # Maps id-> { database_id, bucket }
    oracle = database['oracle']
    # Maps id -> { stacktrace, ... }
    raw_crashes = database['crashes']

    corpus = Corpus(filename.namebase + '.sqlite')

    dbg("Parsing crashes...")
    for crash_id, crash_data in iteritems(raw_crashes):
        bucket_id = oracle[crash_id]
        corpus.insert_crash(crash_id, crash_data, bucket_id)

    return corpus


def load_from_database(filename):
    assert filename.exists()
    return Corpus(filename)


def load(database_name):
    json_filename = database_name.namebase + '.json'
    db_filename = database_name.namebase + '.sqlite'
    if not db_filename.exists() or json_filename.mtime > db_filename.mtime:
        return load_from_json(json_filename)
    return load_from_database(db_filename)
