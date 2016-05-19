__author__ = 'talipov'

with open('input.txt','r') as f:
    _count = f.readline()
    data = [int(i) for i in f.readline().split()]

D_max = 0
current_iter = 0

_max = 0
_min = int(data[0])

_max_2 = 0
_min_2 = _min
index = 0
for item in data:
    item = int(item)

    if _count >= current_iter:
        item2 = data[index]
        index+=1
        if item2 < _min_2:
            _min_2 = item2
        if item2 > _max_2:
            _max_2 = item2

    if item < _min:
        _min = item
    if item > _max:
        _max = item
    current_iter += 1

with open('output.txt','w') as f:
    f.write('%s' % (max(_max,_max_2) - min(_min,_min_2)))
