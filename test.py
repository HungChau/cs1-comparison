# Linear search checks every item in the list in turn. It stops when the
# item is found or when no more items are contained in the list.
def linear_search_v1(L, item):
    '''Return the index of item in list L. If item is not in L, return -1.
    '''

    index = 0
    while index < len(L) and L[index] != item:
        index += 1

    if index == len(L):
        index = -1

    return index


#  Version 1 works, but we didn't like how we had to set the index
# to -1 at the end. We decided we would start at the end and search
# toward the beginning instead. The complexity of the code is the
# same, but the implementation is cleaner.
def linear_search_v2(L, item):
    '''Return the index of item in list L. If item is not in L, return -1.
    '''

    # The not found case should return -1, so search the list backwards.
    index = len(L) - 1
    while index >= 0 and L[index] != item:
        index -= 1

    return index


def time_searchfunc(f, sz):
    '''Return the time required to search a list of size sz using the
    search function f. Always performs a worst-case search.
    '''

    import random
    import time

    large_L = range(sz)
    random.shuffle(large_L)
    t1 = time.time()
    index = f(large_L, -1)
    t2 = time.time()
    return t2 - t1


# For comparison, let's see how fast Python's search is.
def python_search(L, item):
    return L.index(item)


if __name__ == "__main__":
    for sz in range(10000, 160001, 10000):
        print
        "%d items: %f" % (sz, time_searchfunc(linear_search_v2, sz))

    # Python's search is comparable to linear search!
    print
    "Python search on %d items: %f" % (sz, time_searchfunc(python_search, sz))