#!/usr/bin/python

def answer(l, t):
    ''' Find lexicographically smallest sublist from 'l' that is equal to 't' '''
    total = 0
    start = 0
    for end in range(len(l)):
        total = sum(l[start:end + 1])
        
        while (total > t):
            total -= l[start]
            start += 1
            
        if total == t:
            return [start, end]
    
    return [-1, -1]


l1 = [4, 3, 5, 7, 8]
l2 = [1, 2, 3, 4]
l3 = [5, 7, 1, 17, 2, 8, 6, 10, 22, 4]
l4 = [1, 1, 1, 1, 1, 1, 1]
l5 = [42, 1, 1, 42, 17, 3, 5, 2, 4, 8, 1]

print ("Sublist: {}".format(answer(l1, 12)))
print ("Sublist: {}".format(answer(l2, 15)))
print ("Sublist: {}".format(answer(l3, 16)))
print ("Sublist: {}".format(answer(l2, 8)))
print ("Sublist: {}".format(answer(l4, 4)))
