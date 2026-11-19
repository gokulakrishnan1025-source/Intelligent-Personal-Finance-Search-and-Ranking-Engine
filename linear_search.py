"""Linear Search Algorithm - Manual Implementation

Linear search checks every record, one by one.
It is simple. It works on any data (sorted or not).
"""
from text_processing import normalize_text


def linear_search(records, keyword, fields):
    """Search all records for a keyword in the given fields.

    Args:
        records: list of record dictionaries
        keyword: the text to search for
        fields: list of field names to look inside

    Returns:
        list of matching records (keeps original order)
    """
    keyword = normalize_text(keyword)   # make lower case + strip spaces
    matches = []

    for record in records:              # check one record at a time
        for field in fields:
            value = normalize_text(record.get(field, ""))
            if keyword in value:        # partial match is OK
                matches.append(record)
                break                   # one match is enough, go to next record

    return matches