"""Financial Record Management.

Stores records in a Python list (in-memory).
Each record is a dictionary.
Also saves to a CSV file so data survives app restarts.
"""
import csv
import os
import pandas as pd

FIELDS = ["transaction_id", "description", "category", "merchant",
          "amount", "payment_method", "date"]
CSV_FILE = "finance_records.csv"


class DataManager:
    """Manages the collection of financial records."""

    def __init__(self, csv_file=CSV_FILE):
        self.csv_file = csv_file
        self.records = []          # our main Python list
        self._next_id_number = 1
        self.load()

    # ---------- CRUD: Create, Read, Update, Delete ----------

    def add_record(self, description, category, merchant, amount,
                   payment_method, date, transaction_id=None):
        """Add a new record. Returns (record, error_message)."""
        # ----- validate inputs -----
        if not str(description).strip():
            return None, "Description cannot be empty."
        if not str(category).strip():
            return None, "Category cannot be empty."
        try:
            amount = float(amount)
            if amount < 0:
                return None, "Amount cannot be negative."
        except (ValueError, TypeError):
            return None, "Amount must be a valid number."
        if not str(date).strip():
            return None, "Date cannot be empty."

        # ----- auto-create ID if not given -----
        if not transaction_id:
            transaction_id = "TX" + str(self._next_id_number).zfill(3)
        if self.find_by_id(transaction_id):
            return None, f"Duplicate! {transaction_id} already exists."

        record = {
            "transaction_id": str(transaction_id).strip(),
            "description": str(description).strip(),
            "category": str(category).strip(),
            "merchant": str(merchant).strip(),
            "amount": amount,
            "payment_method": str(payment_method).strip(),
            "date": str(date).strip(),
        }
        self.records.append(record)     # add to the list
        self._next_id_number += 1
        self.save()
        return record, None

    def find_by_id(self, transaction_id):
        """Find one record by its Transaction ID."""
        tid = str(transaction_id).strip().lower()
        for r in self.records:
            if r["transaction_id"].lower() == tid:
                return r
        return None

    def get_record_at(self, index):
        """Read one record by its index (position)."""
        if 0 <= index < len(self.records):
            return self.records[index]
        return None

    def update_record(self, transaction_id, **changes):
        """Edit an existing record."""
        record = self.find_by_id(transaction_id)
        if record is None:
            return None, "Record not found."
        for field, value in changes.items():
            if field == "amount":
                try:
                    value = float(value)
                    if value < 0:
                        return None, "Amount cannot be negative."
                except (ValueError, TypeError):
                    return None, "Amount must be a valid number."
            record[field] = value
        self.save()
        return record, None

    def delete_record(self, transaction_id):
        """Remove a record from the list."""
        record = self.find_by_id(transaction_id)
        if record is None:
            return False
        self.records.remove(record)     # remove from the list
        self.save()
        return True

    # ---------- Storage ----------

    def save(self):
        """Write all records to a CSV file."""
        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(self.records)

    def load(self):
        """Read records from the CSV file (if it exists)."""
        if os.path.exists(self.csv_file):
            with open(self.csv_file, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row["amount"] = float(row["amount"])
                    self.records.append(row)
            if self.records:
                nums = [int(r["transaction_id"][2:]) for r in self.records
                        if r["transaction_id"][2:].isdigit()]
                if nums:
                    self._next_id_number = max(nums) + 1

    def to_dataframe(self, records=None):
        """Convert records to a pandas DataFrame (easy table + CSV export)."""
        recs = self.records if records is None else records
        return pd.DataFrame(recs, columns=FIELDS)