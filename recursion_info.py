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
    id              TEXT PRIMARY KEY,
    json            TEXT,       -- JSON encoded
    stack_length    INTEGER,    -- Length of the primary stack trace
    bucket_id       TEXT
);

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
            assert isinstance(module, six.string_types)
        if function is not None:
            assert isinstance(function, six.string_types)
        if arguments is not None:
            assert iter(arguments)
            # TODO: enforce all arguments to be str? assert all([isinstance(arg, str) for arg in arguments])
        if filename is not None:
            assert isinstance(filename, six.string_types)
        if line_number is not None:
            assert isinstance(line_number, six.integer_types)
        if address is not None:
            assert isinstance(address, six.integer_types)
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
        if isinstance(index, six.string_types):
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
    @property
    def has_recursion(self):
        """
        >>> stack = [StackFrame.of(function='main')]
        >>> crash = Crash('0', 'launchpad', stack, {})
        >>> crash.has_recursion
        False

        >>> stack.append(StackFrame.of(function='init'))
        >>> crash = Crash('1', 'launchpad', stack, {})
        >>> crash.has_recursion
        False

        >>> stack = []
        >>> stack.append(StackFrame.of(function='log'))
        >>> stack.append(StackFrame.of(function='fib'))
        >>> stack.append(StackFrame.of(function='fib'))
        >>> stack.append(StackFrame.of(function='main'))
        >>> crash = Crash('2', 'launchpad', stack, {})
        >>> crash.has_recursion
        True

        """
        return len(self.find_recursion()) > 0

    def find_recursion(self):
        """
        Returns a list of (depth, length) pairs of instances of recursion
        within this crash's stack trace. Note that "depth" is zero-indexed
        (top of the stack is depth=0), and that the length is always at least
        2 (it counts the number of frames involved in the recursion).

        >>> stack = []
        >>> stack.append(StackFrame.of(function='log'))
        >>> stack.append(StackFrame.of(function='fib'))
        >>> stack.append(StackFrame.of(function='fib'))
        >>> stack.append(StackFrame.of(function='main'))
        >>> crash = Crash('1', 'launchpad', stack, {})
        >>> crash.find_recursion()
        [(1, 2)]

        >>> stack.insert(0, StackFrame.of(function='log'))
        >>> crash = Crash('2', 'launchpad', stack, {})
        >>> crash.find_recursion()
        [(0, 2), (2, 2)]
        """
        saw_recursion = False
        recursion_length = []
        recursion_depth = []

        for depth, consecutive_frames in enumerate(bigrams(self.stack_trace)):
            a, b = consecutive_frames

            if saw_recursion:
                if a.function and a.function == b.function:
                    # Increase the count of identical frames.
                    recursion_length[-1] += 1
                else:
                    # Exit the recursion state.
                    saw_recursion = False
            else:
                if a.function and a.function == b.function:
                    # Enter "recursion" state
                    saw_recursion = True
                    # Recursion length of two (two identical frames).
                    recursion_length.append(2)
                    recursion_depth.append(depth)
                # Otherwise, remain in "no recursion" state"

        # Combine the results.
        return list(zip(recursion_depth, recursion_length))


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
    assert isinstance(string, six.string_types)
    return json_decoder.decode(string)


def parse_crash(raw_crash):
    """
    Parses a string or OrderedDict into a Crash instance.
    """
    # Automatically parse a JSON string.
    if isinstance(raw_crash, six.string_types):
        raw_crash = decode_json(raw_crash)

    # We will mutate the input, so copy it.
    raw_crash = raw_crash.copy()

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


class RecursionInfo(namedtuple('RecursionInfo', 'crash_id depth length')):
    """
    Metadata about found instance of recursion.
    """
    def __init__(self, crash_id, count, length):
        assert isinstance(depth, int)
        assert isinstance(length, int)
        assert count >= 0
        assert length > 1


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

    def insert_crash(self, report_id, raw_crash, bucket_id):
        """
        Inserts a parsable crash into the database.
        """
        assert not isinstance(raw_crash, six.string_types)
        crash = parse_crash(raw_crash)

        if len(crash.stack_trace) == 0:
            dbg("Ignoring crash with empty stack trace: {id}", id=report_id)
            return

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                'INSERT INTO crash (id, json, stack_length, bucket_id) VALUES'
                ' (?, ?, ?, ?)',
                (report_id, json.dumps(raw_crash), len(crash.stack_trace),
                 bucket_id)
            )

            # Insert all instances of recursion
            for depth, length in crash.find_recursion():
                cursor.execute(
                    'INSERT INTO recursion (crash_id, depth, length) VALUES'
                    ' (?, ?, ?)', (report_id, depth, length)
                )

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

    # Maps id-> { database_id, bucket }
    oracle = database['oracle']
    # Maps id -> { stacktrace, others... }
    raw_crashes = database['crashes']

    corpus = Corpus(filename.namebase + '.sqlite')

    dbg("Parsing crashes...")
    for crash_id, crash_data in iteritems(raw_crashes):
        bucket_id = oracle[crash_id]['bucket']
        corpus.insert_crash(crash_id, crash_data, bucket_id)

    return corpus


def load_from_database(filename):
    assert filename.exists()
    return Corpus(filename)


def load(database_name):
    database_name = Path(database_name)
    json_filename = Path(database_name.namebase + '.json')
    db_filename = Path(database_name.namebase + '.sqlite')
    if not db_filename.exists() or json_filename.mtime > db_filename.mtime:
        return load_from_json(json_filename)
    return load_from_database(db_filename)


if __name__ == '__main__':
    corpus = load('lp_big.json')

    if len(sys.argv) == 2:
        _, crash_id = sys.argv

        from pprint import pprint
        pprint(corpus[crash_id].crash)
