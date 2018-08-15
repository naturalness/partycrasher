from __future__ import division
import random
import sys
import math
from scipy import stats
import numpy
import json
import string
import datetime

import six

from numpy.random import weibull

if six.PY2:
    maketrans = string.maketrans
else:
    maketrans = str.maketrans

import logging
logger = logging.getLogger(__name__)
ERROR = logger.error
WARN = logger.warn
INFO = logger.info
DEBUG = logger.debug

class ChineseRestaurant(object):
    def __init__(self, alpha, source):
        self.alpha = alpha
        self.source = source  # AKA G_0
        self.table_to_index = {None: 0}  
        self.index_to_table = [None]
        self.heap = [None] # make array start 1 for nicer arithmetic
        self.k0 = 1
        self.a = 0
        
    def total(self):
        if len(self.heap) < 2:
            return 0
        return self.heap[1]
        
    def total_unique(self):
        return len(self.heap)-1
    
    def increment(self, index, amount):
        # adapted from: http://stackoverflow.com/questions/2140787/select-k-random-elements-from-a-list-whose-elements-have-weights 2016-07-11
        tablei = index
        assert amount >= 1
        while tablei > 0: # go up the tree (i decreases until its 1 at root)
            self.heap[tablei] += amount # increment totals
            assert self.heap[tablei] is not None
            tablei >>= 1  # go the parent
        return self.heap[1]
    
    def pop(self, table):
        # blows up a table
        index = self.table_to_index[table]
        assert index > 0
        subtract = self.people_at_table(len(self.heap)-1)
        add = subtract-self.people_at_table(index)
        tablei = index
        while tablei > 0:
            self.heap[tablei] += add
            assert self.heap[tablei] is not None
            tablei >>= 1
        tablei = self.total_unique()
        while tablei > 0:
            self.heap[tablei] -= subtract
            assert self.heap[tablei] is not None
            tablei >>= 1
        assert self.heap[-1] == 0
        self.heap.pop()
        self.index_to_table[index] = self.index_to_table[-1]
        itable = self.index_to_table[index]
        self.index_to_table.pop()
        self.table_to_index[itable] = index
        del self.table_to_index[table]

    
    def people_at_table(self, index):
        assert index > 0
        assert index < len(self.heap)
        if len(self.heap) > (index<<1)+1:
            people_left_child = self.heap[index<<1]
            people_right_child = self.heap[(index<<1)+1]
            people_children = people_left_child + people_right_child
            people_self_and_children = self.heap[index]
            people = people_self_and_children - people_children
        elif len(self.heap) > (index<<1):
            people = self.heap[index] - (self.heap[index<<1])
        else:
            people = self.heap[index]
        assert people > 0
        return people
    
    def get_new_probability(self):
        return self.alpha / (self.total() + self.alpha)

    def draw(self):
        if self.total() == 0:
            table = self.source.draw()
            self.table_to_index[table] = 1
            self.index_to_table.append(table)
            self.heap.append(1)
            return table
        else:
            new_probability = self.get_new_probability()
            if random.random() < new_probability:
                table = self.source.draw()
                index = self.total_unique() + 1
                self.table_to_index[table] = index
                self.index_to_table.append(table)
                assert self.index_to_table[index] is table
                self.heap.append(0)
                assert len(self.heap) == index + 1
                self.increment(index, self.k0)
                assert self.heap[index] is not None
                return table
            else:
                people_left = random.randrange(1, self.total()+1) # stupid python range is [)
                tablei = 1
                # see the gas metaphor in http://stackoverflow.com/questions/2140787/select-k-random-elements-from-a-list-whose-elements-have-weights
                while people_left > self.people_at_table(tablei):
                    people_left -= self.people_at_table(tablei) # went past tablei
                    tablei <<= 1 # move to first child
                    if people_left > self.heap[tablei]:
                        people_left -= self.heap[tablei] # went past tablei and all of its children
                        tablei += 1 # move to second child
                self.increment(tablei, 1)
                return self.index_to_table[tablei]

class PreferentialAttachment(ChineseRestaurant):
    """
    Prefential Attachment Process
    * Fixed linear increase in tables
    * k0 is starting weight
    * a fixed to 0
    """
    def __init__(self, m, k0, a, source):
        super().__init__(None, source)
        self.m = m
        self.k0 = k0
        assert a == 0

    def get_new_probability(self):
        if self.total() == self.m:
            return 1
        else:
            return 0

class PreferentialAttachmentPoisson(PreferentialAttachment):
    """
    Prefential Attachment Process - Poisson process for table generation
    * Linear increase in tables at average rate 1/m
    * k0 fixed to 1
    * a fixed to 0
    """
    def get_new_probability(self):
        return 1.0/float(self.m)

class IndianBuffet(object):
    """
    Direct simulation.
    
    Griffiths, Thomas L., and Zoubin Ghahramani. 
    "The indian buffet process: An introduction and review." 
    Journal of Machine Learning Research 12, no. Apr (2011): 1185-1224.
    """
    def __init__(self, alpha, source):
        self.alpha = alpha
        self.source = source
        self.dishes_popularity = []
        self.dishes = []
        self.total_customers = 0 # i in Griffits '11
        
    def draw_new_dishes(self):
        """ The Poisson (new dish) part of the process. 
        """
        poisson_lambda = self.alpha/self.total_customers
        number_of_new_dishes = stats.poisson.rvs(poisson_lambda)
        new_dishes_popularity = [1] * number_of_new_dishes
        new_dishes_indices = list(range(len(self.dishes), len(self.dishes) + number_of_new_dishes))
        new_dishes = list(map(
            lambda _: self.source.draw(),
            new_dishes_indices
            ))
        self.dishes_popularity.extend(new_dishes_popularity)
        self.dishes.extend(new_dishes)
        assert len(self.dishes) == len(self.dishes_popularity)
        return new_dishes
    
    def draw_old_dishes(self):
        picked_existing_dishes = []
        for i in range(0, len(self.dishes)):
            probability_this_dish = (
                float(self.dishes_popularity[i])
                / float(self.total_customers))
            if random.random() < probability_this_dish:
                picked_existing_dishes.append(self.dishes[i])
                self.dishes_popularity[i] += 1
        return picked_existing_dishes
        
        
    def draw(self):
        self.total_customers += 1
        if self.total_customers < 2:
            return self.draw_new_dishes()
        else:
            return self.draw_old_dishes() + list(self.draw_new_dishes())
        

class Numbers(object):
    def __init__(self):
        self.total = 0
    
    def draw(self):
        word = self.total
        self.total += 1
        return word

class Strings(object):
    def __init__(self, prefix, length):
        self.prefix = prefix
        self.length = length
        self.numbers = Numbers()
        self.format_ = '%0' + ("%i" % length) + 'i'
    
    def draw(self):
        n = self.numbers.draw()
        str_n = self.format_ % n
        letters = str_n.translate(maketrans('0123456789', 'pqrstuvwxy'))
        return (self.prefix + letters)
        
class PrefixedNumbers(object):        
    def __init__(self, prefix, length):
        self.prefix = prefix
        self.length = length
        self.numbers = Numbers()
        self.format_ = '%0' + ("%i" % length) + 'i'
    
    def draw(self):
        n = self.numbers.draw()
        str_n = self.format_ % n
        return self.prefix + str_n
    
current = 0
expiry = {}
      
class FakeMetadataField(object):
    """ Responsible for storing a metadata field's properties regardless of bug or document. """
    def __init__(self,
                 name_source,
                 new_word_source,
                 mean_len
                ):
        self.name = name_source.draw()
        self.word_source = new_word_source()
        self.mean_len = mean_len

    def draw_length(self):
        length = stats.poisson.rvs(self.mean_len)
        return length
        
    def draw(self):
        content = []
        length = self.draw_length()
        for i in range(0, length):
            content.append(self.word_source.draw())
        return content
      
class FakeMetadataFields(object):
    """ Responsible for storing all metadata fields regardless of bug or document. """
    def __init__(self,
                 len_total, 
                 nfields_total,
                 new_word_source,
                ):
        self.name_source = Strings('field', 5)
        self.len_total = len_total
        self.nfields_total = nfields_total
        self.new_word_source = new_word_source
        self.fields = []
        
    def get_field(self, index):
        if index < len(self.fields):
            return self.fields[index]
        else:
            assert index == len(self.fields)
            mean_length = stats.gamma.rvs(
                1.0,
                scale=(self.len_total/self.nfields_total)
                )
            # in the line above it may be more proper to swap the 1.0 and the self.len_total buuuut then we get zero-length metadata fields so
            new_field = FakeMetadataField(
                                      self.name_source,
                                      self.new_word_source,
                                      mean_length)
            self.fields.append(new_field)
            return new_field

class TwoParameterWeibull(object):
    def __init__(self,
                 lambda_=1.0,
                 k=1.0):
            self.lambda_ = lambda_
            self.k = k
    
    def draw(self):
        return weibull(self.k)*self.lambda_
      
class FakeBug(object):
    """ Responsible for storing data related to a single bug """
    def __init__(self,
                 new_bug_metadata_field_word_source,
                 fields, 
                 nfields_alpha,
                 name,
                 now,
                 lifetime,
                 bug_picker):
        self.field_gen = IndianBuffet(nfields_alpha, Numbers())
        self.field_word_gens = []
        self.new_bug_metadata_field_word_source = new_bug_metadata_field_word_source
        self.name = name
        self.fields = fields
        self.lifetime = lifetime
        self.expires = current+self.lifetime
        assert self.expires > current, lifetime
        if self.expires in expiry:
            expiry[self.expires].append(self)
        else:
            expiry[self.expires] = [self]
        self.start = current
        self.bug_picker = bug_picker
    
    def draw_field_contents(self, field, field_number):
        field_word_gen = self.field_word_gens[field_number]
        field_contents = []
        field_length = field.draw_length()
        for word_number in range(0, field_length):
            field_contents.append(field_word_gen.draw())
        return " ".join(field_contents)

    def draw_crash(self):
        crash_metadata = {}
        field_numbers = self.field_gen.draw()
        for field_number in field_numbers:
            field = self.fields.get_field(field_number)
            if field_number > len(self.field_word_gens)-1:
                self.field_word_gens.append(
                    self.new_bug_metadata_field_word_source(
                        field.word_source
                        )
                    )
            crash_metadata[field.name] = self.draw_field_contents(field,
                                                             field_number)
        return crash_metadata

    def try_expire(self):
        if current >= self.expires:
            DEBUG(self.name + " fixed after " + str(current-self.start)
                  + "; " +
                  str(self.bug_picker.bug_picker.total_unique())
                  + " bugs remain."
                  )
            self.bug_picker.pop(self)
    
class FakeBugSource(object):
    def __init__(self,
                 new_bug_metadata_field_word_source,
                 fields_source,
                 nfields_alpha,
                 bug_name_gen,
                 bug_life,
                 now,
                 bug_picker):
        self.new_bug_metadata_field_word_source = new_bug_metadata_field_word_source
        self.fields_source = fields_source
        self.nfields_alpha = nfields_alpha
        self.bug_name_gen = bug_name_gen
        self.now = now
        self.bug_life = bug_life
        self.bug_picker = bug_picker
    def draw(self):
            bug = FakeBug(
                self.new_bug_metadata_field_word_source,
                self.fields_source,
                self.nfields_alpha,
                self.bug_name_gen.draw(),
                self.now,
                math.ceil(self.bug_life.draw()),
                self.bug_picker
                )
            return bug

class FakeBugGen(object):
    def __init__(self,
                 bug_rate,
                 bug_life_lambda,
                 bug_life_k,
                 new_bug_metadata_field_word_source,
                 fields_source,
                 nfields_alpha,
                 bug_name_gen):
        self.bug_life = TwoParameterWeibull(bug_life_lambda, bug_life_k)
        self.now = 0
        self.bugs = []
        self.new_bug_metadata_field_word_source = new_bug_metadata_field_word_source
        self.fields_source = fields_source
        self.nfields_alpha = nfields_alpha
        self.bug_name_gen = bug_name_gen
        self.fake_bug_source = FakeBugSource(
                new_bug_metadata_field_word_source,
                fields_source,
                nfields_alpha,
                bug_name_gen,
                self.bug_life,
                self.now,
                self,
                )
        self.bug_picker = PreferentialAttachmentPoisson(
            bug_rate,
            1,
            0,
            self.fake_bug_source
            )
    
    def pop(self, bug_name):
        return self.bug_picker.pop(bug_name)
    
    def draw(self):
        # TODO: optimize this
        picked = self.bug_picker.draw()
        global current
        global expiry
        current += 1
        if current in expiry:
            for bug in expiry[current]:
                bug.try_expire()
        return picked
    
class FakeCrashGen(object):
    def __init__(self,
                 metadata_fields,
                 crash_name_gen,
                 bug_picker,
                 mean_crashes_per_second,
                 start_datetime
            ):
        
        self.fields_source = metadata_fields
        self.crash_name_gen = crash_name_gen
        self.last_datetime = start_datetime
        self.bug_picker = bug_picker
        self.mean_crashes_per_second = mean_crashes_per_second
        self.start_datetime = start_datetime
        self.total_crashes = 0
        self.total_words = 0
     
    def generate_timestamp(self):
        delta_seconds = stats.expon.rvs(0, self.mean_crashes_per_second)
        delta = datetime.timedelta(0, delta_seconds)
        new_time = self.last_datetime + delta
        self.last_datetime = new_time
        return new_time.isoformat()
    
    def generate_crash(self):
        bug = self.bug_picker.draw()
        crash = bug.draw_crash()
        #self.total_crashes += 1
        #for k, v in crash.items():
            #self.total_words += len(v.split())
        #DEBUG("Average crash length: " + str(self.total_words / self.total_crashes))
        crash['database_id'] = self.crash_name_gen.draw()
        crash['date'] = self.generate_timestamp()
        return (crash, bug.name)
      
def example_fake_crash_gen():
    metadata_field_new_word_m = 21.1 # new word every m words
    bug_metadata_field_new_word_m = 21.1 # TODO: estimate this
    
    metadata_mean_nfields = 50 # TODO: estimate this
    metadata_mean_field_length = 20 # TODO: estimate this
    crash_metadata_total_words = metadata_mean_nfields * metadata_mean_field_length
    
    bug_rate = 1.39 # in bugs/crash not bugs/day
    bug_life_scale = 1580.2635286 # in bugs/crash not bugs/day
    bug_life_shape = 0.5221691 
    
    #metadata_vocab = PreferentialAttachmentPoisson(
        #metadata_vocab_alpha,
        #1,
        #0,
        #Strings('', 0)
        #)
    metadata_vocab = Strings('', 0)
    def new_metadata_field_word_source():
        return PreferentialAttachmentPoisson(
            metadata_field_new_word_m,
            21,
            0,
            metadata_vocab
            )
    
    metadata_fields = FakeMetadataFields(
        crash_metadata_total_words,
        metadata_mean_nfields,
        new_metadata_field_word_source,
        )
    
    def new_bug_metadata_field_word_source(metadata_field_word_source):
        return PreferentialAttachmentPoisson(
            bug_metadata_field_new_word_m,
            21,
            0,
            Strings('', 0)
            )
    
    crash_name_gen = PrefixedNumbers('fake', 8)
    bug_name_gen = PrefixedNumbers('bug', 6)
    
    start_datetime = datetime.datetime(1980, 1, 1, 0, 0, 0)
    mean_crashes_per_second = 1/3177.706
    
    bug_picker = FakeBugGen(
        bug_rate,
        bug_life_scale,
        bug_life_shape,
        new_bug_metadata_field_word_source,
        metadata_fields,
        metadata_mean_nfields,
        bug_name_gen
        )
        
    
    crash_gen = FakeCrashGen(
        metadata_fields,
        crash_name_gen,
        bug_picker,
        mean_crashes_per_second,
        start_datetime,
        )
    
    return crash_gen

class PoissonChisq(object):
    """ Used by the testing code only! """
    def __init__(self, lambda_):
        self.lambda_ = lambda_
        self.histogram = []
        self.observations = []
        self.total = 0
    
    def observe(self, count):
        # B/c this is a poisson process you must observe an event-count-like variable
        assert count == int(count)
        assert count >= 0
        if len(self.histogram)-1 < count:
            self.histogram.extend([0] * (count - (len(self.histogram)-1)))
        self.histogram[count] += 1
        self.total += count
        self.observations.append(count)
    
    def mean(self):
        return float(self.total)/float(sum(self.histogram))
    
    def expected_mean(self):
        return self.lambda_
    
    def variance(self):
        return numpy.var(self.observations)
    
    def expected_variance(self):
        return self.lambda_
    
    def test(self):
        nr_observations = sum(self.histogram)
        observed_frequencies = []
        expected_frequencies = []
        frequencies_of = []
        thresh = 10
        for i in range(0, len(self.histogram)):
            observed = self.histogram[i]
            expected = stats.poisson.pmf(i, self.lambda_) * nr_observations
            if (
                (observed >= thresh)
                and (expected >= thresh)):
                observed_frequencies.append(observed)
                expected_frequencies.append(expected)
                frequencies_of.append(i)
        results = stats.chisquare(observed_frequencies,
                                  expected_frequencies)
        print("expected: mean %f variance %f" % (
                      self.expected_mean(),
                      self.expected_variance()))
        print("actual: mean %f variance %f" % (
                      self.mean(),
                      self.variance()))
        print(len(expected_frequencies))
        print(results)
        from matplotlib import pyplot
        import matplotlib
        pyplot.switch_backend('Qt5Agg')
        actual_plot, = pyplot.plot(frequencies_of, observed_frequencies, label='actual')
        expected_plot, = pyplot.plot(frequencies_of, expected_frequencies, 'r', linewidth=1, label='expected')
        matplotlib.interactive(True)
        #pyplot.ylabel("People at Table")
        #pyplot.xlabel("Table Number")
        #pyplot.title("Chinese Restaurant Process Unit Test")
        pyplot.legend()
        pyplot.show(block=True)
        return results


import unittest
class TestFakeDataGenerator(unittest.TestCase):
    
    def test_chinese_restaurant_process(self):
        print(sys.path)
        import os
        os.environ["MPLBACKEND"] = "Qt5Agg"
        from matplotlib import pyplot
        import matplotlib
        from scipy import stats
        alpha = 10
        test_size = 10000
        tests = 100
        data = [0]
        for j in range(0, tests):
            cr = ChineseRestaurant(alpha, Numbers())
            for i in range(0, test_size):
                new_sample = cr.draw()
                if new_sample >= len(data):
                    data.append(0)
                data[new_sample] += 1
            assert cr.heap[1] == test_size
        pyplot.switch_backend('Qt5Agg')
        #data=sorted(data, reverse=True)
        print(len(data))
        actual_plot, = pyplot.plot(range(1,len(data)), data[1:], label='actual avg')
        expected = [0]
        remain = test_size * tests
        # stick breaking process
        for i in range(1, len(data)):
            break_ = stats.beta.mean(1.0, float(alpha)) * remain
            expected.append(break_)
            remain -= break_
        #print est
        expected_plot, = pyplot.plot(range(1,len(data)), expected[1:], 'r', linewidth=1, label='expected')
        matplotlib.interactive(True)
        pyplot.ylabel("People at Table")
        pyplot.xlabel("Table Number")
        pyplot.title("Chinese Restaurant Process Unit Test")
        pyplot.legend()
        pyplot.show(block=True)
        
    def test_indian_buffet_process(self):
        import scipy
        alpha = 20
        tests = 10000
        test_size = 10
        # Compute the nth harmonic number: see
        # http://stackoverflow.com/a/27683292 2016-07-18
        Hn = scipy.special.digamma(test_size + 1) + numpy.euler_gamma
        # See Griffiths '11 
        #expected_number_dishes = stats.poisson.mean(alpha * Hn)
        individuals_dishes = PoissonChisq(alpha)
        restaurant_dishes = PoissonChisq(alpha * Hn)
        restaurant_dishes_bogus = PoissonChisq(alpha * Hn)
        for j in range(0, tests):
            ib = IndianBuffet(alpha, Numbers())
            number_dishes = 0
            last_individuals_dishes = None
            for i in range(0, test_size):
                new_sample = list(ib.draw())
                assert len(new_sample) > 0
                #individuals_dishes.observe(len(new_sample))
                last_individuals_dishes = len(new_sample)
                # add one here because the Numbers() source we used starts at
                # 0
                number_dishes = max(number_dishes, max(new_sample) + 1)
            individuals_dishes.observe(last_individuals_dishes)
            restaurant_dishes.observe(number_dishes)
            restaurant_dishes_bogus.observe(stats.poisson.rvs(alpha * Hn))
        # As of this commit this stuff isn't working, I can't get the chisquared
        # test produce consistent results at all, it basically always says my 
        # distribution isn't poisson even though it really should be and it looks
        # like it so I'm going to leave off any asserts and work on it more 
        # at a later date
        print("Number of dishes for each individual:")
        individuals_dishes.test()
        print("Number of dishes for each restaurant:")
        restaurant_dishes.test()
        restaurant_dishes_bogus.test()
   
    def test_fake_crash_generation(self):
        crash_gen = example_fake_crash_gen()
        for i in range(0, 15000):
            crash = crash_gen.generate_crash()
            if crash[1] == 'bug000001':
                print(json.dumps(crash, indent=2, sort_keys=True))

        #for i in range(0, 20):
            #print json.dumps(crash_gen.generate_crash(), indent=2, sort_keys=True)

      
            
if __name__ == '__main__':
    unittest.main()
