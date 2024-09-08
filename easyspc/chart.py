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
    """Batch iterable by length n."""

    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch


class ChartBase:
    """Chart base representation."""

    default_template_name = None

    def __init__(self, template=None) -> None:
        self.template = template

    def get_template(self) -> dict:
        """Get and/or return template."""

        if not isinstance(self.template, dict):
            name = self.default_template_name
            data = get_data(__name__, name)
            self.template = loads(data.decode())
        return self.template

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

    default_template_name = "stacked.json"

    def __init__(
        self,
        data: list,
        subgroup_size: int = 5,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        groups = list(batched(data, n=subgroup_size))
        self.subgroup_size = subgroup_size
        self.x_bar = list(map(mean, groups))
        self.r = list(map(lambda v: max(v) - min(v), groups))

    @property
    def center_line_x(self) -> float:
        return mean(self.x_bar)

    @property
    def center_line_r(self) -> float:
        return mean(self.r)

    @property
    def lower_control_limit_x(self) -> float:
        A2 = abc_table[self.subgroup_size].A2
        return self.center_line_x - (A2 * self.center_line_r)

    @property
    def upper_control_limit_x(self) -> float:
        A2 = abc_table[self.subgroup_size].A2
        return self.center_line_x + (A2 * self.center_line_r)

    @property
    def lower_control_limit_r(self) -> float:
        D3 = abc_table[self.subgroup_size].D3
        return D3 * self.center_line_r

    @property
    def upper_control_limit_r(self) -> float:
        D4 = abc_table[self.subgroup_size].D4
        return D4 * self.center_line_r

    def plot(self) -> dict:
        template = self.get_template()
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

    default_template_name = "stacked.json"

    def __init__(
        self,
        data: list,
        subgroup_size: int = 9,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        groups = list(batched(data, n=subgroup_size))
        self.subgroup_size = subgroup_size
        self.x_bar = list(map(mean, groups))
        self.s = list(map(stdev, groups))

    @property
    def center_line_x(self) -> float:
        return mean(self.x_bar)

    @property
    def center_line_s(self) -> float:
        return mean(self.s)

    @property
    def lower_control_limit_x(self) -> float:
        A3 = abc_table[self.subgroup_size].A3
        return self.center_line_x - (A3 * self.center_line_s)

    @property
    def upper_control_limit_x(self) -> float:
        A3 = abc_table[self.subgroup_size].A3
        return self.center_line_x + (A3 * self.center_line_s)

    @property
    def lower_control_limit_s(self) -> float:
        B3 = abc_table[self.subgroup_size].B3
        return B3 * self.center_line_s

    @property
    def upper_control_limit_s(self) -> float:
        B4 = abc_table[self.subgroup_size].B4
        return B4 * self.center_line_s

    def plot(self) -> dict:
        template = self.get_template()
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

    default_template_name = "stacked.json"

    def __init__(self, data: list, **kwargs) -> None:
        super().__init__(**kwargs)
        func = lambda i: abs(data[i] - data[i - 1])
        self.i = data
        self.mr = list(map(func, range(1, len(data))))

    @property
    def center_line_i(self) -> float:
        return mean(self.i)

    @property
    def center_line_mr(self) -> float:
        return mean(self.mr)

    @property
    def lower_control_limit_i(self) -> float:
        return self.center_line_i - (3 * stdev(self.i))

    @property
    def upper_control_limit_i(self) -> float:
        return self.center_line_i + (3 * stdev(self.i))

    @property
    def lower_control_limit_mr(self) -> float:
        return self.center_line_mr - (
            3 * self.center_line_i / abc_table[2].d2
        )

    @property
    def upper_control_limit_mr(self) -> float:
        return self.center_line_mr + (
            3 * self.center_line_i / abc_table[2].d2
        )

    def plot(self) -> dict:
        template = self.get_template()
        template["data"][0]["x"] = list(range(1, len(self.i) + 1))
        template["data"][0]["y"] = self.i
        template["data"][1]["x"] = list(range(2, len(self.i) + 1))
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
