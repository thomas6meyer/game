
import numpy as np

def irand(minimum, maximum):
    if minimum == maximum:
        return minimum
    return np.random.randint(minimum, maximum)

def rrand(minimum, maximum):
    if minimum == maximum:
        return minimum
    return np.random.uniform(minimum, maximum)


def nrand(mean = 0, stdev = 1.0, size=1):
    if size == 1:
        return np.random.normal(mean, stdev)
    else:
        return np.random.normal(mean, stdev, size)

def xrand(stdev = 1.0, size=1):
    if size == 1:
        return np.sqrt( sum(nrand(stdev=stdev, size=2)**2) )
    else:
        return [xrand(stdev) for i in range(size)]

def makeDeck():
    d=[]
    for c in range(2, 11):
        for suit in range(4):
            if c == 5 or c == 10:
                d.append(-0.5)
            else:
                d.append(0.0)
    for c in range(4):
        for suit in range(4):
            d.append(0.5)
    for c in range(78 - 9*4 - 4*4):
        d.append(1.0)
    d[-1] = 3.0
    d[-2] = 2.0
    d[-3] = -2.0
    d[-4] = -1.0
    return d

__defaultDeck__ = makeDeck()

def drawCards(n):
    return sum(np.random.choice(__defaultDeck__, n))

