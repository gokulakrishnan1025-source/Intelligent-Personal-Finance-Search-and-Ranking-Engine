"""Binary Search Algorithm - Manual Implementation

Binary search is FAST. But it has one rule:
the records MUST be sorted by the same field you search.

It cuts the data in half again and again.
That is why it is fast (O(log n)).
"""


def _compare(value, target):
    """Compare two values that may be numbers or text."""
    # Try to compare as numbers first
    try:
        return (float(value) > float(target)) - (float(value) < float(target))
    except (ValueError, TypeError):
        v, t = str(value).lower(), str(target).lower()
        return (v > t) - (v < t)


def binary_search(records, target, key_field):
    """Exact-match binary search on records sorted by key_field.

    Args:
        records: list of records, SORTED by key_field
        target: the exact value to find
        key_field: field to search in (e.g. "transaction_id" or "amount")

    Returns:
        list of all records matching the target exactly
    """
    results = []
    low = 0
    high = len(records) - 1

    while low <= high:
        mid = (low + high) // 2          # middle index
        cmp = _compare(records[mid].get(key_field, ""), target)

        if cmp == 0:                     # found it!
            results.append(records[mid])
            # check neighbours too (there may be duplicates)
            left = mid - 1
            while left >= low and _compare(records[left].get(key_field, ""), target) == 0:
                results.append(records[left])
                left -= 1
            right = mid + 1
            while right <= high and _compare(records[right].get(key_field, ""), target) == 0:
                results.append(records[right])
                right += 1
            return results
        elif cmp < 0:                    # target is on the right side
            low = mid + 1
        else:                            # target is on the left side
            high = mid - 1

    return results                       # not found -> empty list