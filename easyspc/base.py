#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: 2024 Michael Czigler
SPDX-License-Identifier: BSD-3-Clause
"""

from json import loads
from pkgutil import get_data


def batched(iterable, n: int):
    """
    Batch data from the iterable into tuples of
    length n. The last batch may be shorter
    than n.
    """

    if n < 1:
        raise ValueError("n is less than 1")
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch


def load_template(name: str) -> dict:
    """Load template resource."""

    data = get_data(__name__, name)
    if not isinstance(data, bytes):
        raise Exception("Invalid template.")
    template = loads(data.decode())
    return template


class ChartBase:
    def __init__(self, data: list) -> None:
        self.data = data

    def _batch_data(self, n: int) -> list:
        return list(batched(self.data, n))

    def plot(self) -> dict:
        raise NotImplemented

    def summary(self) -> dict:
        raise NotImplemented
 