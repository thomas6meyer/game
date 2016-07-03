"""
Return a galic name (nome)
"""

import numpy as np

computer = 'home'

if computer == 'laptop':
    prefixPath = r'C:\Users\thm02004.UCONN\Documents\Python Projects and Stuff\tournament\nome-prefix.txt'
    suffixPath = r'C:\Users\thm02004.UCONN\Documents\Python Projects and Stuff\tournament\nome-suffix.txt'
elif computer == 'home':
    prefixPath = r'C:\Users\caHt\Documents\MyPython\tournament\nome-prefix.txt'
    suffixPath = r'C:\Users\caHt\Documents\MyPython\tournament\nome-suffix.txt'

nome = []

prefixFile = open(prefixPath)
suffixFile = open(suffixPath)

prefix = prefixFile.readlines()
suffix = suffixFile.readlines()

def randomNome():
    return np.random.choice(prefix)[:-1] + np.random.choice(suffix)[:-1]