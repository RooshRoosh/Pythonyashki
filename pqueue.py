#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
'''
Объединяем поток данных из нескольких источников в 1.
'''

__author__ = 'talipov'


import heapq
import itertools

a = [9, 8, 9, 3, 14, 4, 11, 1, 0, 5, 12, 10, 2, 7, 13]
b = [7, 10, 13, 6, 16, 5, 15, 12, 11, 9, 3, 14, 17, 4, 8]
c = [10, 13, 9, 12, 18, 5, 16, 8, 17, 14, 11, 15, 19, 7, 6]


def multiplex(*source_list):
    '''
    :param source_list:
        list of number list
    :return:
    '''
    # init
    h = []
    for _iter in source_list:
        element = next(_iter)
        heapq.heappush(h, element)

    # run
    yield heapq.heappop(h)
    for elements in itertools.zip_longest(*source_list):
        for element in (element for element in elements if element is not None):
            yield heapq.heappushpop(h, element)

    # finish
    while h:
        yield heapq.heappop(h)

if __name__ == '__main__':
    for i in multiplex(iter(a), iter(b), iter(c)):
        print(i)