# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 20:34:26 2014

@author: Michael
"""

import math
from matplotlib import pyplot
import random

def tossCoin():
    return random.choice(["H", "T"])

def waitForString(string):
    """returns the number of flips needed until
    we get a desired sequence"""
    n = len(string)
    lastN = []
    trials = 0
    while len(lastN) < len(string):
        lastN += [tossCoin()]
        trials += 1
    while not same(string, lastN):
        lastN = lastN[1:] + [tossCoin()]
        trials += 1
    return trials

def same(string, L):
    for x in range(len(L)):
        if string[x] != L[x]:
            return False
    return True

def getTstats(string1, string2, trials=1000):
    """gets a t-score for a pooled test comparing
    the number of flips needed for two different strings"""
    r1 = []
    r2 = []
    for trial in range(trials):
        r1.append(waitForString(string1))
        r2.append(waitForString(string2))
    avg1 = sum(r1)/float(trials)
    avg2 = sum(r2)/float(trials)
    var1 = 1/float(trials-1)*sum([(x - avg1)**2 for x in r1])
    var2 = 1/float(trials-1)*sum([(x - avg2)**2 for x in r2])
    S_p  = math.sqrt((trials-1)*(var1 + var2)/float(2*trials - 2))
    df   = 2*trials - 2
    print "Difference in variances is: ", (var2 - var1)/((var1 + var2)/2)
    T = (avg1 - avg2)/(S_p*math.sqrt(2/float(trials)))
    return T, df

#the main verifies that not all strings
#of the same length take the same number
#of flips on average
trials = 500
r1 = []
r2 = []
for trial in range(trials):
    r1.append(waitForString(10*"H"))
    r2.append(waitForString(5*"HT"))
pyplot.hist(r1)
pyplot.hist(r2)
