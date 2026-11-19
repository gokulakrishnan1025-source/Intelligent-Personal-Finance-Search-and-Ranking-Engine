"""Bubble Sort Algorithm - Manual Implementation

Bubble sort compares neighbours and swaps them.
Big values "bubble up" to the end, like bubbles in water.

We do NOT use Python's sorted() or sort() here.
This is written by hand to show the algorithm.
"""


def bubble_sort(records, key, reverse=False):
    """Sort records by a numeric field using bubble sort.

    Args:
        records: list of record dictionaries
        key: field name to sort by (e.g. "amount")
        reverse: False = lowest first, True = highest first

    Returns:
        a NEW sorted list (original list is not changed)
    """
    items = list(records)                # copy, do not change original
    n = len(items)

    for i in range(n - 1):             # pass through the list
        swapped = False                  # did we swap anything this pass?
        for j in range(n - 1 - i):       # compare neighbours
            a = float(items[j].get(key, 0))
            b = float(items[j + 1].get(key, 0))
            if (not reverse and a > b) or (reverse and a < b):
                items[j], items[j + 1] = items[j + 1], items[j]  # swap
                swapped = True
        if not swapped:                  # already sorted -> stop early
            break

    return items