#!/usr/bin/env python3

import sys
from db_table import db_table


def lookup(db, col, val):
    result = []
    initial_query = db.select([], {col:  val})
    for row in initial_query:
        result.extend(db.select([], {"session_num":  row["session_num"]}))
    no_dups = []
    for item in result:
        if item not in no_dups:
            no_dups.append(item)
    print(no_dups)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise RuntimeError("Invalid # of args provided")

    # Retrieve the column and value from cmd line args
    column = sys.argv[1]
    value = sys.argv[2]
    print(value)

    # Create table using existing schema. Note that db will already be populated
    schema = {"date": "text",
              "time_start": "text",
              "time_end": "text",
              "session_type": "text",
              "title": "text",
              "location": "text",
              "description": "text",
              "speakers": "text",
              "session_num": "integer",
              "subsess_num": "integer", }

    db = db_table("my_table", schema)

    lookup(db, column, value)
