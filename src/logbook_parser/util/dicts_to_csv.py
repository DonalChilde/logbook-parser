####################################################
#                                                  #
#      src/snippets/file/dicts_to_csv.py
#                                                  #
####################################################
# Created by: Chad Lowe                            #
# Created on: 2022-10-13T11:41:58-07:00            #
# Last Modified: _iso_date_         #
# Source: https://github.com/DonalChilde/snippets  #
####################################################

import csv
from pathlib import Path
from typing import Any, Dict, Iterable, Literal, Optional, Sequence

try:
    from more_itertools import peekable
except ImportError:
    from snippets.vendor.peekable import peekable  # type: ignore


def dicts_to_csv(
    dicts: Iterable[Dict],
    output_path: Path,
    *,
    parents: bool = True,
    overwrite_ok: bool = False,
    write_header: bool = True,
    fields: Optional[Sequence] = None,
    restval: Any = "",
):
    """
    Save an iterable of dicts to csv.

    If a list of fields is not provided, all fields will be output, in the order
    they are defined in the dict.

    Args:
        dicts: _description_
        output_path: Output path to the csv file.
        parents: Create missing parent directories. Defaults to True.
        overwrite_ok: Overwrite an existing file. Defaults to False.
        write_header: First line of the csv file contains column headers.
            Defaults to True.
        fields: Ordered list of fields to be output. Defaults to None.
        restval: Default value for missing field. Defaults to "".
    """
    if overwrite_ok:
        mode = "w"
    else:
        mode = "x"
    if parents:
        output_path.parent.mkdir(parents=parents, exist_ok=True)
    source = peekable(dicts)
    if fields is None:
        first = source.peek()
        fieldnames: Sequence = list(first.keys())
    else:
        fieldnames = fields
    if fields is not None:
        extras: Literal["raise", "ignore"] = "ignore"
    else:
        extras = "raise"
    with open(output_path, mode, newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=fieldnames, extrasaction=extras, restval=restval
        )
        if write_header:
            writer.writeheader()
        for row in source:
            writer.writerow(row)
