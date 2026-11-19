"""Test cases for all algorithms. Run: pytest tests/ -v
or simply: python tests/test_algorithms.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linear_search import linear_search
from binary_search import binary_search
from bubble_sort import bubble_sort
from selection_sort import selection_sort
from data_manager import DataManager

SAMPLE = [
    {"transaction_id": "TX101", "description": "Grocery Shopping",
     "category": "Food", "merchant": "Local Store",
     "amount": 2500.0, "payment_method": "UPI", "date": "2026-11-01"},
    {"transaction_id": "TX102", "description": "Bus Ticket",
     "category": "Travel", "merchant": "City Bus",
     "amount": 50.0, "payment_method": "Cash", "date": "2026-11-02"},
    {"transaction_id": "TX103", "description": "Electricity Bill",
     "category": "Bills", "merchant": "Power Co",
     "amount": 1200.0, "payment_method": "UPI", "date": "2026-11-03"},
    {"transaction_id": "TX104", "description": "Movie Night",
     "category": "Entertainment", "merchant": "Cineplex",
     "amount": 500.0, "payment_method": "Card", "date": "2026-11-04"},
]


def test_linear_search_found():
    r = linear_search(SAMPLE, "grocery", ["description", "category"])
    assert len(r) == 1 and r[0]["transaction_id"] == "TX101"


def test_linear_search_case_insensitive():
    r = linear_search(SAMPLE, "UPI", ["payment_method"])
    assert len(r) == 2


def test_linear_search_not_found():
    r = linear_search(SAMPLE, "diamond", ["description"])
    assert r == []


def test_binary_search_sorted():
    s = selection_sort(SAMPLE, "transaction_id")   # sort by ID first
    r = binary_search(s, "TX103", "transaction_id")
    assert len(r) == 1 and r[0]["amount"] == 1200.0


def test_binary_search_not_found():
    s = selection_sort(SAMPLE, "transaction_id")
    r = binary_search(s, "TX999", "transaction_id")
    assert r == []


def test_bubble_sort_ascending():
    s = bubble_sort(SAMPLE, "amount")
    amounts = [r["amount"] for r in s]
    assert amounts == sorted(amounts) and len(s) == len(SAMPLE)


def test_bubble_sort_descending():
    s = bubble_sort(SAMPLE, "amount", reverse=True)
    amounts = [r["amount"] for r in s]
    assert amounts == sorted(amounts, reverse=True)


def test_selection_sort_ascending():
    s = selection_sort(SAMPLE, "merchant")
    names = [r["merchant"] for r in s]
    assert names == sorted(names, key=str.lower)


def test_selection_sort_descending():
    s = selection_sort(SAMPLE, "amount", reverse=True)
    amounts = [r["amount"] for r in s]
    assert amounts == sorted(amounts, reverse=True)


def test_crud(tmp_csv="test_records_tmp.csv"):
    dm = DataManager(tmp_csv)
    rec, err = dm.add_record("Grocery Shopping", "Food", "Local Store",
                             2500, "UPI", "2026-11-01", "TX101")
    assert err is None and rec["transaction_id"] == "TX101"
    # duplicate
    _, err = dm.add_record("Again", "Food", "X", 10, "UPI",
                           "2026-11-01", "TX101")
    assert err is not None
    # invalid amount
    _, err = dm.add_record("Bad", "Food", "X", "abc", "UPI", "2026-11-01")
    assert err is not None
    # edit
    rec, err = dm.update_record("TX101", amount=3000)
    assert err is None and rec["amount"] == 3000.0
    # delete
    assert dm.delete_record("TX101") is True
    assert dm.find_by_id("TX101") is None
    os.remove(tmp_csv)


if __name__ == "__main__":
    fns = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS  {fn.__name__}")
    print(f"\nAll {len(fns)} tests passed!")