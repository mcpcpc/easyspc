#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: 2024 Michael Czigler
SPDX-License-Identifier: BSD-3-Clause
"""

from statistics import mean
from statistics import stdev

from .base import ChartBase
from .const import abc_table


class XBarS(ChartBase):
    """XBar-S Chart.

    Use Xbar-S Chart to monitor the mean and
    variation of a process when you have
    continuous data and subgroup sizes of 9 or
    more. Use this control chart to monitor
    process stability over time so that you
    can identify and correct instabilities in
    a process.
    """

    def __init__(
        *args,
        **kwargs,
        subgroup_size: int = 5,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.subgroup_size = subgroup_size
        A3 = abc_table[self.subgroup_size].A3
        B3 = abc_table[self.subgroup_size].B3
        B4 = abc_table[self.subgroup_size].B4
        samples = self._batch_data(self.subgroup_size)
        self.s = list(map(stdev, samples))
        self.x_bar = list(map(mean, groups))
        self.s_bar = mean(self.s)
        self.center_line_x = mean(self.x_bar)
        self.center_line_s = mean(self.s_bar)
        self.upper_control_limit_x = self.center_line_x + (A3 * self.s_bar)
        self.lower_control_limit_x = self.center_line_x - (A3 * self.s_bar)
        self.upper_control_limit_s = B4 * self.center_line_s
        self.lower_control_limit_s = B3 * self.center_line_s

    def plot(self) -> dict:
        pass

    def summary(self) -> None:
        print("X-Bar Chart Summary:")
        print(f"Center Line (CL): {self.center_line_x:.3f}")
        print(f"Upper Control Limit (UCL): {self.upper_control_limit_x:.3f}")
        print(f"Lower Control Limit (UCL): {self.lower_control_limit_x:.3f}")
        print(f"Number of Subgroups: {len(self.x_bar)}")
        print("S Chart Summary:")
        print(f"Center Line (CL): {self.center_line_s:.3f}")
        print(f"Upper Control Limit (UCL): {self.upper_control_limit_s:.3f}")
        print(f"Lower Control Limit (UCL): {self.lower_control_limit_s:.3f}")
        print(f"Number of Subgroups: {len(self.s_bar)}")
