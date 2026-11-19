"""Text Processing, Indexing and Slicing helpers."""


def normalize_text(text):
    """Clean text: remove extra spaces and make it lower case.
    This makes searching case-insensitive."""
    return str(text).strip().lower()


def build_index(records, field):
    """Build a simple inverted index.
    Returns a dict: word -> list of records containing that word."""
    index = {}
    for record in records:
        for word in normalize_text(record.get(field, "")).split():
            index.setdefault(word, []).append(record)
    return index


def slice_records(records, start=0, limit=None):
    """Return only a part (slice) of the record list.
    Used to show 'top 10 results' etc."""
    if limit is None:
        return records[start:]
    return records[start:start + limit]


def get_by_index(records, i):
    """Get one record by its position (index) in the list."""
    if 0 <= i < len(records):
        return records[i]
    return None


def extract_keywords(text):
    """Split a search sentence into single words."""
    return [w for w in normalize_text(text).split() if w]