"""Selection Sort Algorithm - Manual Implementation

Selection sort finds the smallest (or biggest) item
and moves it to the front. Then repeats.

We do NOT use Python's sorted() or sort() here.
This is written by hand to show the algorithm.
"""


def selection_sort(records, key, reverse=False):
    """Sort records by a text or numeric field using selection sort.

    Args:
        records: list of record dictionaries
        key: field name to sort by (e.g. "merchant", "date")
        reverse: False = A-Z / smallest first, True = reversed

    Returns:
        a NEW sorted list (original list is not changed)
    """
    items = list(records)                # copy, do not change original
    n = len(items)

    def value(rec):                      # helper: get value to compare
        v = rec.get(key, "")
        try:
            return (0, float(v))         # numbers first
        except (ValueError, TypeError):
            return (1, str(v).lower())   # text, lower case

    for i in range(n - 1):
        best = i                          # position of best item so far
        for j in range(i + 1, n):
            better = value(items[j]) < value(items[best])
            if reverse:
                better = value(items[j]) > value(items[best])
            if better:
                best = j
        if best != i:
            items[i], items[best] = items[best], items[i]  # swap

    return items