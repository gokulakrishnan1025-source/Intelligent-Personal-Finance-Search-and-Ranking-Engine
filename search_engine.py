"""Search Engine: connects user queries to linear or binary search."""
import time
from linear_search import linear_search
from binary_search import binary_search
from bubble_sort import bubble_sort
from selection_sort import selection_sort

SEARCHABLE_FIELDS = ["transaction_id", "description", "category",
                     "merchant", "payment_method"]


class SearchEngine:
    """Runs searches and measures performance."""

    def smart_text_search(self, records, query, fields=None):
        """LINEAR SEARCH on text. Partial match, case-insensitive.

        Returns (results, info_dict)."""
        if fields is None:
            fields = SEARCHABLE_FIELDS
        start = time.perf_counter()
        results = linear_search(records, query, fields)
        elapsed = time.perf_counter() - start
        return results, {
            "algorithm": "Linear Search",
            "query": query,
            "matches": len(results),
            "time_ms": round(elapsed * 1000, 3),
            "note": "Checked every record one by one (no sorting needed).",
        }

    def exact_id_search(self, records, transaction_id):
        """BINARY SEARCH on Transaction ID (exact match).

        The records are first sorted by Transaction ID,
        because binary search only works on sorted data.
        """
        start = time.perf_counter()
        sorted_records = bubble_sort_by_text(records, "transaction_id")
        results = binary_search(sorted_records, transaction_id, "transaction_id")
        elapsed = time.perf_counter() - start
        return results, {
            "algorithm": "Binary Search",
            "query": transaction_id,
            "matches": len(results),
            "time_ms": round(elapsed * 1000, 3),
            "note": "Data was sorted by Transaction ID first "
                    "(binary search needs sorted data).",
        }

    def amount_search(self, records, amount):
        """BINARY SEARCH on Amount (exact match, sorted by amount)."""
        start = time.perf_counter()
        sorted_records = bubble_sort(records, "amount")
        results = binary_search(sorted_records, amount, "amount")
        elapsed = time.perf_counter() - start
        return results, {
            "algorithm": "Binary Search",
            "query": amount,
            "matches": len(results),
            "time_ms": round(elapsed * 1000, 3),
            "note": "Data was sorted by Amount first "
                    "(binary search needs sorted data).",
        }


def bubble_sort_by_text(records, key):
    """Manual bubble sort for text (used before binary search by ID)."""
    items = list(records)
    n = len(items)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if str(items[j].get(key, "")).lower() > str(items[j + 1].get(key, "")).lower():
                items[j], items[j + 1] = items[j + 1], items[j]
                swapped = True
        if not swapped:
            break
    return items