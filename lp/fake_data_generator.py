from __future__ import division
import random
import sys
import math

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
    def __init__(alpha, source):
        self.alpha = alpha
        self.source = source
        

class Numbers(object):
    def __init__(self):
        self.total = 0
    
    def draw(self):
        word = self.total
        self.total += 1
        return word
      
class Bug(object):
    def __init__(field_alpha, field_source, word_alpha, word_source):
        self.field_gen = ChineseRestaurant(field_alpha, field_source)
        self.word_gens = []
        self.word_alpha = word_alpha
        self.word_source = word_source
    
    
    
      
class CrashGen(object):
    def __init__(fields, max_field_len, bug_alpha):
        self.fields = fields
        self.max_field_len = max_field_len
        self.bug_source = ChineseRestaurant(bug_alpha, Numbers())
        self.bugs = []
    
    def generate_crash():
        self.bug_number = self.bug_source.draw()
        if self.bug_number == len(self.bugs):
            # New bug!
            self.bugs[self.bug_number] = ChineseRestaurant()

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
            
if __name__ == '__main__':
    unittest.main()
