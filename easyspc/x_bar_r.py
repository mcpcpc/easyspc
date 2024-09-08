#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: 2024 Michael Czigler
SPDX-License-Identifier: BSD-3-Clause
"""

from statistics import mean

from .base import ChartBase
from .const import abc_table


class XBarR(ChartBase):
    """Xbar-R Chart.

    Use Xbar-R Chart to monitor the mean and
    variation of a process when you have
    continuous data and subgroup sizes of 8
    or less. Use this control chart to monitor
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
        samples = self._batch_data(self.subgroup_size)
        self.r = list(map(lambda v: max(v) - min(v), samples))
        self.x_bar = list(map(mean, groups))
        self.r_bar = mean(self.r)
        self.center_line_x = mean(self.x_bar)
        self.center_line_r = mean(self.r_bar)
        self.upper_control_limit_x = self.center_line_x + (A2 * self.r_bar)
        self.lower_control_limit_x = self.center_line_x - (A2 * self.r_bar)
        self.upper_control_limit_r = D4 * self.center_line_r
        self.lower_control_limit_r = D3 * self.center_line_r

    def plot(self) -> dict:
        pass

    def summary(self) -> None:
        print("X-Bar Chart Summary:")
        print(f"Center Line (CL): {self.center_line_x:.3f}")
        print(f"Upper Control Limit (UCL): {self.upper_control_limit_x:.3f}")
        print(f"Lower Control Limit (UCL): {self.lower_control_limit_x:.3f}")
        print(f"Number of Subgroups: {len(self.x_bar)}")
        print("R Chart Summary:")
        print(f"Center Line (CL): {self.center_line_r:.3f}")
        print(f"Upper Control Limit (UCL): {self.upper_control_limit_r:.3f}")
        print(f"Lower Control Limit (UCL): {self.lower_control_limit_r:.3f}")
        print(f"Number of Subgroups: {len(self.r_bar)}")
