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
CREATE TABLE IF NOT EXISTS crash(id, json, bucket_id);

-- Allow indexing by database_id.
CREATE INDEX IF NOT EXISTS crash_id ON crash (id);

-- TODO: Add stuff here!
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

    # TODO: Canonical crash feilds

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
            raise IndexError('Not sure how to handle index: {}'.format(index))

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
        assert not isinstance(crash, str)
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                'INSERT INTO crash (id, json, bucket_id) VALUES'
                ' (?, ?, ?)', (report_id, json.dumps(crash), bucket_id)
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


class Crash(object):
    def __init__(self, id, project=None):
        self.id = id
        self.project = project
        self.stack = []
        self.context = {}
        self.extra = {}

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

    def tokenize(self, tokenizer):
        # From stack trace
        tokens = [token for frame in self.stack
                  for token in frame.tokenize(tokenizer)]

        # From context
        for field in itervalues(self.context):
            tokens.extend(tokenizer(field))

        return tokens



frame_fields = 'module function arguments filename line_number address'


class StackFrame(namedtuple('StackFrame', frame_fields)):
    @classmethod
    def of(cls, **kwargs):
        return StackFrame(module=kwargs.get('module', ''),
                          function=kwargs.get('function', ''),
                          arguments=kwargs.get('arguments', ''),
                          filename=kwargs.get('filename', ''),
                          line_number=kwargs.get('line_number', ''),
                          address=kwargs.get('address', ''))

    @classmethod
    def parse(cls, raw_frame):
        return cls(module=raw_frame.get('dylib', ''),
                   function=raw_frame.get('function', ''),
                   arguments=raw_frame.get('args', ''),
                   filename=raw_frame.get('file', ''),
                   line_number='',
                   address=raw_frame.get('address', ''))

    def tokenize(self, tokenizer):
        tokens = []
        tokens.extend(tokenizer(self.module))
        tokens.extend(tokenizer(self.function))
        tokens.extend(tokenizer(self.arguments))
        tokens.extend(tokenizer(self.filename))
        tokens.extend(tokenizer(self.line_number))
        tokens.extend(tokenizer(self.address))
        return tokens


class Bucket(object):
    def __init__(self, bucket_id):
        self.id = bucket_id
        self.crashes = {}

    def add(self, report_id, crash):
        assert isinstance(crash, Crash)
        self.crashes[report_id] = crash

    def __len__(self):
        return len(self.crashes)

    def __contains__(self, key):
        if isinstance(self, crash):
            for other in iteritems(self.crashes):
                if other is crash:
                    return True
            return False
        else:
            return key in self.crashes


class Corpus(namedtuple('Corpus', 'name crashes buckets')):
    @classmethod
    def new(cls, name):
        return cls(name, {}, {})

    def add_to_bucket(self, report_id, bucket_id):
        if bucket_id not in self.buckets:
            self.buckets[bucket_id] = Bucket(bucket_id)
        bucket = self.buckets[bucket_id]
        bucket.add(report_id, self.crashes[report_id])


class Distribution(object):
    """
    Basic abstract class for all distributions.
    """
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        result = "{}:\n".format(self.label)

        if hasattr(self, 'min'):
            result += "\tMin:\t{} × {}\n".format(*self.min)
        if hasattr(self, 'max'):
            result += "\tMax:\t{} × {}\n".format(*self.max)
        if hasattr(self, 'mode'):
            result += "\tMode:\t{} × {}\n".format(*self.mode)
        if hasattr(self, 'mean'):
            result += "\tMean:\t{}\n".format(self.mean)
        if hasattr(self, 'variance'):
            result += "\tVar:\t{}\n".format(self.variance)
        if hasattr(self, 'counter'):
            result += "\tTop 3:\t{!r}\n".format(self.counter.most_common(n=3))

        return result

    def save_observations(self, basename, key_label="key", amount_label="value"):
        """
        Saves a CSV file containing each individual observation; this is
        suitable for analysis in R.
        """
        with open(basename+'.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow((key_label, amount_label))
            for key in self.counter.elements():
                writer.writerow((key, '1'))


class NominalDistribution(Distribution):
    """
    A distribution of nominal data (e.g., tokens).
    """

    def __init__(self, label):
        super(NominalDistribution, self).__init__(label)
        self.counter = Counter()

    def __iadd__(self, thing):
        self.counter[thing] += 1
        return self

    def __len__(self):
        """
        How many total obeservations there are.
        """
        return sum(itervalues(self.counter))

    @property
    def mode(self):
        return self.counter.most_common(n=1)[0]


class OrdinalDistribution(NominalDistribution):
    """
    A distribution of ordinal data.
    """

    @property
    def max(self):
        key = max(iterkeys(self.counter))
        return key, self.counter[key]

    @property
    def min(self):
        key = min(iterkeys(self.counter))
        return key, self.counter[key]


class IntervalDistribtion(OrdinalDistribution):
    @property
    def interval(self):
        lower, _ = self.min
        upper, _ = self.max
        return lower, upper

    @property
    def range(self):
        lower, upper = self.interval
        return upper - lower

    @property
    def mean(self):
        return sum(self.counter.elements()) / len(self)


class RatioDistribution(IntervalDistribtion):
    """
    A distribution of ratio data (e.g., recursion depth).
    """

    @property
    def variance(self):
        mean = self.mean
        obvs = len(self)
        return sum(amount / obvs * (value - mean) ** 2
                   for value, amount in iteritems(self.counter))


class PatternTokenizer(object):
    """
    A tokenizer based on a splitting regular expression.

    >>> lerch('a little bit of tea') == ['little']
    True
    >>> camel('call MooseX::FTPClass2_beta') == ["call", "Moose", "X", "FTP", "Class", "2", "beta"]
    True
    >>> camel('hello world') == ['hello', 'world']
    True

    """
    def __init__(self, pattern, transform=None,
                 min_length=None, max_length=None):
        self.pattern = regex.compile(pattern, regex.VERSION1)
        self.min = min_length or 0
        self.max = max_length or float('infinity')
        self.transform = transform or (lambda x: x)

    def __call__(self, string):
        tokens = self.pattern.splititer(self.transform(string))
        min_len = self.min
        max_len = self.max
        return [token for token in tokens
                if token and min_len <= len(token) <= max_len]


# From ES Docs: https://github.com/elastic/elasticsearch/blob/1.6/docs/reference/analysis/analyzers/pattern-analyzer.asciidoc
# 2016-01-27
camel = PatternTokenizer(
    '(?:[^\\p{L}\\d]+)|'
    '(?<=\\D)(?=\\d)|'
    '(?<=\\d)(?=\\D)|'
    '(?<=[\\p{L}&&[^\\p{Lu}]])(?=\\p{Lu})|'
    '(?<=\\p{Lu})(?=\\p{Lu}[\\p{L}&&[^\\p{Lu}]])'
)
lerch = PatternTokenizer('\W+',
                         transform=six.text_type.lower,
                         min_length=4,
                         max_length=2000)
space = PatternTokenizer('\s+')


def mtime(filename):
    try:
        return os.stat(filename).st_mtime
    except OSError:
        return -float('inf')


def load_from_json():
    dbg("Parsing JSON...")

    with open('lp.json', 'r') as jsonfile:
        database = json.load(jsonfile)

    # Maps id-> { database_id, bucket }
    oracle = database['oracle']
    # Maps id -> { stacktrace, others }
    raw_crashes = database['crashes']

    corpus = Corpus.new('launchpad')

    dbg("Parsing crashes...")
    for dbid, crash_data in iteritems(raw_crashes):
        corpus.crashes[dbid] = Crash.parse(dbid, crash_data)

    dbg("Figuring out buckets...")
    for report_id, info in iteritems(oracle):
        assert report_id == info['database_id']
        bucket_id = info['bucket']
        corpus.add_to_bucket(report_id, bucket_id)

    with open('lp.corpus', 'wb') as picklefile:
        pickle.dump(corpus, picklefile)

    return corpus


def load_from_pickle():
    dbg("Loading from pickle...")
    try:
        with open('lp.corpus', 'rb') as picklefile:
            return pickle.load(picklefile)
    except EOFError:
        return load_from_json()


def load():
    if mtime('lp.json') > mtime('lp.corpus'):
        return load_from_json()
    return load_from_pickle()


def lazy_setdefault(d, k, fn):
    return d[k] if k in d else d.setdefault(k, fn())


# TODO: per corpus: figure out field length.

# Collect means and totals (modes are trivial!)
#  - per field
#  - per bucket
#  - per report
#  - per corpus
#
# - Unique tokens [fbrc]
# - Tokens per crash [bc]
# - How many context fields? [r]
# - Stack depth [r]
# - Distribution of tokens [fbbc]
#
if __name__ == '__main__':
    corpus = load()
    dbg("Corpus loaded!")

    print("# crashes:", len(corpus.crashes))
    print("# buckets:", len(corpus.buckets))

    dist = RatioDistribution('Max recursion depth per crash (corpus-wide)')

    field_token_dists = {}
    field_count_dists = {}
    field_presence_dist = NominalDistribution('Popular fields (corpus-wide)')

    dbg("Computing per-crash token distributions")
    for report_id, crash in iteritems(corpus.crashes):
        # Report recursion depth.
        dist += crash.max_recursion_depth

        # Figure out raw stats on token length.
        for field, value in iteritems(crash.context):
            field_presence_dist += field

            tokens = camel(value)

            when_new = lambda: RatioDistribution('Raw number of tokens in '+ str(field))
            count_dist = lazy_setdefault(field_count_dists, field, when_new)
            count_dist += len(tokens)

            when_new = lambda: NominalDistribution('Unique tokens in '+ str(field))
            token_dist = lazy_setdefault(field_token_dists, field, when_new)
            for token in tokens:
                token_dist += token

    # Print recursion depth.
    print(dist)
    crashes_with_recursion = sum(amount for value, amount in dist.counter.items() if value > 0)
    dist.save_observations("recursion", key_label="max.depth")

    print()

    # Print field information
    print(field_presence_dist)

    print()

    # Print token information for each field.
    for field in field_count_dists:
        print(field_count_dists[field])
        print(field_token_dists[field])
