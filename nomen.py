# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 09:53:46 2016

@author: thm02004
"""
import numpy as np

computer = 'home'

if computer == 'laptop':
    path = r'C:\Users\thm02004.UCONN\Documents\Python Projects and Stuff\nomen\nomen.txt'
elif computer == 'home':
    path = r'C:\Users\caHt\Documents\MyPython\tournament\nomen.txt'
    
plebians = []
patricians = []

nomenFile = open(path)

nomenLine = nomenFile.readline()
while nomenLine:
    nomen, status = nomenLine.split(',')
    status = status[0]
    if status == 'N':
        plebians.append(nomen)
    elif status == 'Y':
        patricians.append(nomen)
    else:
        print "Unexpected status value: ", status
    nomenLine = nomenFile.readline()

def randomPleb():
    return np.random.choice(plebians)

def randomPatrician():
    return np.random.choice(patricians)

if __name__ == '__main__':
    choice = 'not q'
    while choice != 'q':
        choice = raw_input("Input [ p=plebian | P=patrician | q=quit] default = p: ")
        if len(choice) == 0:
            choice = 'p'

        if choice == 'p':
            print '\n', np.random.choice(plebians), '\n'
        elif choice == 'P':
            print '\n', np.random.choice(patricians), '\n'
        elif choice == 'q':
            continue
        else:
            print "Valid inputs are [ p | P]"