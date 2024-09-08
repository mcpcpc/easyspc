#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: 2024 Michael Czigler
SPDX-License-Identifier: BSD-3-Clause
"""

from statistics import mean
from statistics import stdev

from .base import ChartBase


class IMR(ChartBase):
    """I-MR Chart.

    Use I-MR Chart to monitor the mean and
    variation of your process when you have
    continuous data that are individual
    observations not in subgroups. Use this
    control chart to monitor process
    stability over time so that you can
    identify and correct instabilities in a
    process.
    """

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        func = lambda v: abs(v[i] - v[i - 1])
        self.mr = list(map(func, self.data))
        self.center_line_i = mean(self.data)
        self.center_line_mr = mean(self.mr)
        self.upper_control_limit_i = self.center_line_i + (3 * stdev(self.data)
        self.lower_control_limit_i = self.center_line_i - (3 * stdev(self.data)
        self.upper_control_limit_mr = self.center_line_mr + (3 * self.center_line_i / 1.128)
        self.lower_control_limit_mr = self.center_line_mr - (3 * self.center_line_i / 1.128)

    def plot(self) -> dict:
        pass

    def summary(self) -> None:
        print("I Chart Summary:")
        print(f"Center Line (CL): {self.center_line_i:.3f}")
        print(f"Upper Control Limit (UCL): {self.upper_control_limit_i:.3f}")
        print(f"Lower Control Limit (UCL): {self.lower_control_limit_i:.3f}")
        print("MR Summary:")
        print(f"Center Line (CL): {self.center_line_s:.3f}")
        print(f"Upper Control Limit (UCL): {self.upper_control_limit_mr:.3f}")
        print(f"Lower Control Limit (UCL): {self.lower_control_limit_mr:.3f}")

