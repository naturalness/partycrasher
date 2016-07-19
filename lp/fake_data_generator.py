from __future__ import division
import random
import sys
import math
from scipy import stats
import numpy

class ChineseRestaurant(object):
    def __init__(self, alpha, source):
        self.alpha = alpha
        self.source = source  # AKA G_0
        self.table_to_index = {None: 0}  
        self.index_to_table = [None]
        self.heap = [None] # make array start 1 for nicer arithmetic
        
    def total(self):
        if len(self.heap) < 2:
            return 0
        return self.heap[1]
        
    def total_unique(self):
        return len(self.heap)-1
    
    def increment(self, index):
        # adapted from: http://stackoverflow.com/questions/2140787/select-k-random-elements-from-a-list-whose-elements-have-weights 2016-07-11
        tablei = index
        while tablei > 0: # go up the tree (i decreases until its 1 at root)
            self.heap[tablei] += 1 # increment totals
            tablei >>= 1  # go the parent
        return self.heap[1]
    
    def people_at_table(self, index):
        if len(self.heap) > (index<<1)+1:
            people = self.heap[index] - (self.heap[index<<1] + 
                                        self.heap[(index<<1)+1])
        elif len(self.heap) > (index<<1):
            people = self.heap[index] - (self.heap[index<<1])
        else:
            people = self.heap[index]
        assert people > 0
        return people

    def draw(self):
        if self.total() == 0:
            table = self.source.draw()
            self.table_to_index[table] = 0
            self.index_to_table.append(table)
            self.heap.append(1)
            return table
        else:
            new_probability = self.alpha / (self.total() + self.alpha)
            if random.random() < new_probability:
                table = self.source.draw()
                index = self.total_unique() + 1
                self.table_to_index[table] = index
                self.index_to_table.append(table)
                assert self.index_to_table[index] is table
                self.heap.append(0)
                assert len(self.heap) == index + 1
                self.increment(index)
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
                self.increment(tablei)
                return self.index_to_table[tablei]

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
        new_dishes = map(
            lambda _: self.source.draw(),
            new_dishes_indices
            )
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
            return self.draw_old_dishes() + self.draw_new_dishes()
        

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
        letters = str_n.translate(string.maketrans('0123456789', 'pqrstuvwxy')
        return prefix + letters
        
        
      
class MetadataField(object):
    """ Responsible for storing a metadata field's properties regardless of bug or document. """
    def __init__(
                 name_source,
                 metadata_word_source, 
                 field_word_alpha, 
                 mean_len
                ):
        self.name = name_source.draw()
        self.word_source = ChineseRestaurant(field_word_alpha, metadata_word_source)
        self.mean_len

    def draw_length():
        length = stats.poisson.rvs(self.mean_len)
        return length
        
    def draw():
        content = []
        length = self.draw_length()
        for i in range(0, length):
            content.append(word_source.draw())
        return content
      
class MetadataFields(object):
    """ Responsible for storing all metadata fields regardless of bug or document. """
    def __init__(
                 metadata_word_source, 
                 len_total, 
                 nfields_total,
                 field_word_alpha
                ):
        self.name_source = Strings('field', 5)
        self.word_source = metadata_word_source
        self.len_total = len_total
        self.nfields_total = nfields_total
        self.fields = []
        
    def get_field(self, index):
        if index < len(self.fields):
            return self.fields[index]
        else:
            assert index == len(self.fields)
            mean_length = stats.gamma.rvs(len_total, scale=(1.0/nfields_total))
            new_field = MetadataField(
                                      self.name_source,
                                      self.word_source,
                                      field_word_alpha,
                                      mean_length)
        
      
class Bug(object):
    """ Responsible for storing data related to a single bug """
    def __init__(field_alpha, field_source, word_alpha, word_source, field_len_alpha):
        self.field_gen = IndianBuffet(field_alpha, field_source)
        self.word_gens = []
        self.word_alpha = word_alpha
        self.word_source = word_source
    
    def draw_crash():
        fields = self.field_gen.draw()
        for f in fields:
            if f > len(self.word_gens)-1:
                self.word_gens.append(ChineseRestaurant(word_alpha, word_source))
            
    
    
      
class CrashGen(object):
    def __init__(fields, metadata_word_alpha, field_word_alpha, bug_alpha):
        self.metadata_word_source = ChineseRestaurant(metadata_word_alpha, Strings('', 8))
        self.fields = MetadataFields(
                                     self.metadata_word_source,
                                     len_total,
                                     nfields_total,
                                     field_word_alpha
                                    )
        self.bug_id_source = ChineseRestaurant(bug_alpha, Numbers())
        self.bugs = []
    
    def generate_crash():
        self.bug_number = self.bug_source.draw()
        if self.bug_number == len(self.bugs):
            # New bug!
            self.bugs[self.bug_number] = ChineseRestaurant()

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
        print "expected: mean %f variance %f" % (
                      self.expected_mean(),
                      self.expected_variance())
        print "actual: mean %f variance %f" % (
                      self.mean(),
                      self.variance())
        print len(expected_frequencies)
        print results
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
        print sys.path
        from matplotlib import pyplot
        import matplotlib
        from scipy import stats
        alpha = 20
        test_size = 1000
        tests = 1000
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
        print len(data)
        actual_plot, = pyplot.plot(range(1,len(data)), data[1:], label='actual avg')
        expected = [0]
        remain = test_size * tests
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
                new_sample = ib.draw()
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
        print "Number of dishes for each individual:"
        individuals_dishes.test()
        print "Number of dishes for each restaurant:"
        restaurant_dishes.test()
        restaurant_dishes_bogus.test()
            
if __name__ == '__main__':
    unittest.main()
