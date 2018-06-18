#!/usr/bin/python

id_list = []

def new_minion_id(number, base):
    ''' Return subtracted and converted result using base 'base' '''
    minion_id = str(number)
    dec_x = int(''.join(sorted(minion_id, reverse=True)), base)
    dec_y = int(''.join(sorted(minion_id)), base)
    subtracted = dec_x - dec_y
    result = ""

    while subtracted:
        result = str(subtracted % base) + result
        subtracted //= base

    length = len(str(dec_x))
    result = str(result).rjust(length, '0')

    return (result)

def answer(n, b):
    ''' Recursive function to add and check for minion id match '''
    minion_id = new_minion_id(n, b)

    for index, value in enumerate(id_list):
        if value == minion_id:
            return (len(id_list) - index)

    id_list.append(minion_id)

    return (answer(minion_id, b))

print ("final answer: {}".format(answer(1211, 10)))
print ("final answer: {}".format(answer(210022, 3)))
print ("final answer: {}".format(answer(1234567, 9)))
print ("final answer: {}".format(answer(23410, 5)))
print ("final answer: {}".format(answer(7246513, 8)))
print ("final answer: {}".format(answer(552246, 10)))

