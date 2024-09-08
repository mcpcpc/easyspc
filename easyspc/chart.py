#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: 2024 Michael Czigler
SPDX-License-Identifier: BSD-3-Clause
"""

from itertools import islice
from json import loads
from pkgutil import get_data
from statistics import mean
from statistics import stdev

from .const import abc_table


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

    def summary(self) -> None:
        raise NotImplemented
 

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
        subgroup_size: int = 5,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.subgroup_size = subgroup_size
        groups = self._batch_data(self.subgroup_size)
        self.x_bar = list(map(mean, groups))
        self.r = list(map(lambda v: max(v) - min(v), groups))
        self.center_line_x = mean(self.x_bar)
        self.center_line_r = mean(self.r)
        self.upper_control_limit_x = self.center_line_x + (A2 * self.r_bar)
        self.lower_control_limit_x = self.center_line_x - (A2 * self.r_bar)
        self.upper_control_limit_r = D4 * self.center_line_r
        self.lower_control_limit_r = D3 * self.center_line_r

    def plot(self) -> dict:
        template = load_template("stacked.json")
        template["data"][0]["x"] = list(range(len(self.x_bar)))
        template["data"][0]["y"] = self.x_bar
        template["data"][1]["x"] = list(range(len(self.r)))
        template["data"][1]["y"] = self.r
        template["layout"]["shapes"][0]["name"] = "CL"
        template["layout"]["shapes"][0]["y0"] = self.center_line_x
        template["layout"]["shapes"][0]["y1"] = self.center_line_x
        template["layout"]["shapes"][1]["name"] = "LCL"
        template["layout"]["shapes"][1]["y0"] = self.lower_control_limit_x
        template["layout"]["shapes"][1]["y1"] = self.lower_control_limit_x
        template["layout"]["shapes"][2]["name"] = "UCL"
        template["layout"]["shapes"][2]["y0"] = self.upper_control_limit_x
        template["layout"]["shapes"][2]["y1"] = self.upper_control_limit_x
        template["layout"]["shapes"][3]["name"] = "Rbar"
        template["layout"]["shapes"][3]["y0"] = self.center_line_r
        template["layout"]["shapes"][3]["y1"] = self.center_line_r
        template["layout"]["shapes"][4]["name"] = "MR_LCL"
        template["layout"]["shapes"][4]["y0"] = self.lower_control_limit_r
        template["layout"]["shapes"][4]["y1"] = self.lower_control_limit_r
        template["layout"]["shapes"][5]["name"] = "MR_UCL"
        template["layout"]["shapes"][5]["y0"] = self.upper_control_limit_r
        template["layout"]["shapes"][5]["y1"] = self.upper_control_limit_r
        template["layout"]["xaxis"]["title"]["text"] = "Sample"
        template["layout"]["xaxis2"]["title"]["text"] = "Sample"
        template["layout"]["yaxis"]["title"]["text"] = "Sample Mean"
        template["layout"]["yaxis2"]["title"]["text"] = "Sample Range"
        return template

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
        subgroup_size: int = 5,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.subgroup_size = subgroup_size
        A3 = abc_table[self.subgroup_size].A3
        B3 = abc_table[self.subgroup_size].B3
        B4 = abc_table[self.subgroup_size].B4
        groups = self._batch_data(self.subgroup_size)
        self.x_bar = list(map(mean, groups))
        self.s = list(map(stdev, groups))
        self.center_line_x = mean(self.x_bar)
        self.center_line_s = mean(self.s)
        self.upper_control_limit_x = self.center_line_x + (A3 * self.s_bar)
        self.lower_control_limit_x = self.center_line_x - (A3 * self.s_bar)
        self.upper_control_limit_s = B4 * self.center_line_s
        self.lower_control_limit_s = B3 * self.center_line_s

    def plot(self) -> dict:
        template = load_template("stacked.json")
        template["data"][0]["x"] = list(range(len(self.x_bar)))
        template["data"][0]["y"] = self.x_bar
        template["data"][1]["x"] = list(range(len(self.s)))
        template["data"][1]["y"] = self.s
        template["layout"]["shapes"][0]["name"] = "CL"
        template["layout"]["shapes"][0]["y0"] = self.center_line_x
        template["layout"]["shapes"][0]["y1"] = self.center_line_x
        template["layout"]["shapes"][1]["name"] = "LCL"
        template["layout"]["shapes"][1]["y0"] = self.lower_control_limit_x
        template["layout"]["shapes"][1]["y1"] = self.lower_control_limit_x
        template["layout"]["shapes"][2]["name"] = "UCL"
        template["layout"]["shapes"][2]["y0"] = self.upper_control_limit_x
        template["layout"]["shapes"][2]["y1"] = self.upper_control_limit_x
        template["layout"]["shapes"][3]["name"] = "SBar"
        template["layout"]["shapes"][3]["y0"] = self.center_line_s
        template["layout"]["shapes"][3]["y1"] = self.center_line_s
        template["layout"]["shapes"][4]["name"] = "S_LCL"
        template["layout"]["shapes"][4]["y0"] = self.lower_control_limit_s
        template["layout"]["shapes"][4]["y1"] = self.lower_control_limit_s
        template["layout"]["shapes"][5]["name"] = "S_UCL"
        template["layout"]["shapes"][5]["y0"] = self.upper_control_limit_s
        template["layout"]["shapes"][5]["y1"] = self.upper_control_limit_s
        template["layout"]["xaxis"]["title"]["text"] = "Sample"
        template["layout"]["xaxis2"]["title"]["text"] = "Sample"
        template["layout"]["yaxis"]["title"]["text"] = "Sample Mean"
        template["layout"]["yaxis2"]["title"]["text"] = "Sample StdDev"
        return template

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
        self.upper_control_limit_i = self.center_line_i + (3 * stdev(self.data))
        self.lower_control_limit_i = self.center_line_i - (3 * stdev(self.data))
        self.upper_control_limit_mr = self.center_line_mr + (3 * self.center_line_i / 1.128)
        self.lower_control_limit_mr = self.center_line_mr - (3 * self.center_line_i / 1.128)

    def plot(self) -> dict:
        template = load_template("stacked.json")
        template["data"][0]["x"] = list(range(1, len(x) + 1))
        template["data"][0]["y"] = self.data
        template["data"][1]["x"] = list(range(2, len(x) + 1))
        template["data"][1]["y"] = self.mr
        template["layout"]["shapes"][0]["name"] = "CL"
        template["layout"]["shapes"][0]["y0"] = self.center_line_i
        template["layout"]["shapes"][0]["y1"] = self.center_line_i
        template["layout"]["shapes"][1]["name"] = "LCL"
        template["layout"]["shapes"][1]["y0"] = self.lower_control_limit_i
        template["layout"]["shapes"][1]["y1"] = self.lower_control_limit_i
        template["layout"]["shapes"][2]["name"] = "UCL"
        template["layout"]["shapes"][2]["y0"] = self.upper_control_limit_i
        template["layout"]["shapes"][2]["y1"] = self.upper_control_limit_i
        template["layout"]["shapes"][3]["name"] = "MRBar"
        template["layout"]["shapes"][3]["y0"] = self.center_line_mr
        template["layout"]["shapes"][3]["y1"] = self.center_line_mr
        template["layout"]["shapes"][4]["name"] = "MR_LCL"
        template["layout"]["shapes"][4]["y0"] = self.upper_control_limit_mr
        template["layout"]["shapes"][4]["y1"] = self.upper_control_limit_mr
        template["layout"]["shapes"][5]["name"] = "MR_UCL"
        template["layout"]["shapes"][5]["y0"] = self.upper_control_limit_mr
        template["layout"]["shapes"][5]["y1"] = self.upper_control_limit_mr
        template["layout"]["xaxis"]["title"]["text"] = "Observation"
        template["layout"]["xaxis2"]["title"]["text"] = "Observation"
        template["layout"]["yaxis"]["title"]["text"] = "Individual Value"
        template["layout"]["yaxis2"]["title"]["text"] = "Moving Range"
        return template

    def summary(self) -> None:
        print("I Chart Summary:")
        print(f"Center Line (CL): {self.center_line_i:.3f}")
        print(f"Upper Control Limit (UCL): {self.upper_control_limit_i:.3f}")
        print(f"Lower Control Limit (UCL): {self.lower_control_limit_i:.3f}")
        print("MR Summary:")
        print(f"Center Line (CL): {self.center_line_s:.3f}")
        print(f"Upper Control Limit (UCL): {self.upper_control_limit_mr:.3f}")
        print(f"Lower Control Limit (UCL): {self.lower_control_limit_mr:.3f}")
