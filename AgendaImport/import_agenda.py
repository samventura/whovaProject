#!/usr/bin/env python3

import xlrd
import sys
from db_table import db_table


def process_excel(db, sh):
    # Column definitions
    columns = ["date", "time_start", "time_end", "session_type", "title",
               "location", "description", "speakers", "session_num", "subsess_num"]

    # Monitors session number (will begin at 1) and sub-session numbers
    session_num = 0
    subsess_num = 2

    # Begin on line 16 (15 b/c 0-indexed) and process all excel file data
    for row_idx in range(15, sh.nrows):
        # Given a row: parse data within row (8 columns of data)
        data = {}
        for col_idx in range(8):
            # print("row: %s col: %s" % (row_idx, col_idx))

            cell_value = sh.cell_value(rowx=row_idx, colx=col_idx)
            if col_idx == 3:
                if cell_value == "Session":
                    session_num += 1
                    data[columns[8]] = session_num
                    data[columns[9]] = 1
                    subsess_num = 2
                else:
                    data[columns[8]] = session_num
                    data[columns[9]] = subsess_num
                    subsess_num += 1

            data[columns[col_idx]] = cell_value.replace("'", "''")

        # print("Data for row %s: %s" % (row_idx, data))
        db.insert(data)


if __name__ == "__main__":
    # Create schema for table
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

    # Create table
    db = db_table("my_table", schema)

    if len(sys.argv) != 2:
        raise RuntimeError("No file name provided")
    file_name = sys.argv[1]

    # Using xlrd to open the input file (and get the specific sheet)
    book = xlrd.open_workbook(file_name)
    sh = book.sheet_by_index(0)

    # Parse the excel file and populate db with it
    # process_excel(db, sh)

    # just to confirm retrieval works
    print(db.select())

    db.close()
