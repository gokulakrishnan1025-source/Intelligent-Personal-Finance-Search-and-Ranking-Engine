"""Ranking Engine: sorts search results using bubble sort
and selection sort, and explains which one is used."""
from bubble_sort import bubble_sort
from selection_sort import selection_sort


def rank_results(records, criterion):
    """Rank records by the chosen criterion.

    Bubble Sort is used for NUMERIC ranking (amount).
    Selection Sort is used for TEXT ranking (alphabetical, category, date).

    Returns (sorted_list, explanation).
    """
    if criterion == "Highest amount first":
        return bubble_sort(records, "amount", reverse=True), \
            "Bubble Sort (descending) on Amount"
    if criterion == "Lowest amount first":
        return bubble_sort(records, "amount", reverse=False), \
            "Bubble Sort (ascending) on Amount"
    if criterion == "Alphabetical (Merchant A-Z)":
        return selection_sort(records, "merchant"), \
            "Selection Sort (ascending) on Merchant"
    if criterion == "Category (A-Z)":
        return selection_sort(records, "category"), \
            "Selection Sort (ascending) on Category"
    if criterion == "Recent transaction first":
        return selection_sort(records, "date", reverse=True), \
            "Selection Sort (descending) on Date"
    return list(records), "No sorting applied"