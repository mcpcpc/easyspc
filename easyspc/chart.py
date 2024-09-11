#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: 2024 Michael Czigler
SPDX-License-Identifier: BSD-3-Clause
"""

from itertools import islice
from statistics import mean
from statistics import stdev

from plotly.graph_objects import Figure
from plotly.subplots import make_subplots

from .const import abc_table


def batched(iterable, n: int):
    """Batch iterable by length n."""

    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch


class XBarR:
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
        self,
        data: list,
        subgroup_size: int = 5,
    ) -> None:
        self.data = data
        self.subgroup_size = subgroup_size

    def x_bar(self) -> list:
        n = self.subgroup_size
        groups = list(batched(self.data, n))
        return list(map(mean, groups))

    def r(self) -> list:
        n = self.subgroup_size
        groups = list(batched(self.data, n))
        func = lambda v: max(v) - min(v)
        return list(map(func, groups))

    def center_line_x(self) -> float:
        x_bar = self.x_bar()
        return mean(x_bar)

    def center_line_r(self) -> float:
        r = self.r()
        return mean(r)

    def lower_control_limit_x(self) -> float:
        A2 = abc_table[self.subgroup_size].A2
        center_line_x = self.center_line_x()
        center_line_r = self.center_line_r()
        return center_line_x - (A2 * center_line_r)

    def upper_control_limit_x(self) -> float:
        A2 = abc_table[self.subgroup_size].A2
        center_line_x = self.center_line_x()
        center_line_r = self.center_line_r()
        return center_line_x + (A2 * center_line_r)

    def lower_control_limit_r(self) -> float:
        D3 = abc_table[self.subgroup_size].D3
        center_line_r = self.center_line_r()
        return D3 * center_line_r

    def upper_control_limit_r(self) -> float:
        D4 = abc_table[self.subgroup_size].D4
        center_line_r = self.center_line_r()
        return D4 * center_line_r

    def cp(self, lsl: float, usl: float) -> float:
        d2 = abc_table[self.subgroup_size].d2
        center_line_r = self.center_line_r()
        sigma = center_line_r / d2
        return (usl - lsl) / (6 * sigma)

    def cpk(self, lsl: float, usl: float) -> float:
        d2 = abc_table[self.subgroup_size].d2
        center_line_r = self.center_line_r()
        sigma = center_line_r / d2
        cpk_upper = (usl - self.x_bar) / (3 * sigma)
        cpk_lower = (self.x_bar - lsl) / (3 * sigma)
        return min((cpk_upper, cpk_lower))

    def plot(self) -> Figure:
        x_bar = self.x_bar()
        cl_x = self.center_line_x()
        lcl_x = self.lower_control_limit_x()
        ucl_x = self.upper_control_limit_x()
        r = self.r()
        cl_r = self.center_line_r()
        lcl_r = self.lower_control_limit_r()
        ucl_r = self.upper_control_limit_r()
        figure = make_subplots(rows=2, cols=1)
        figure.add_hline(y=cl_x, name="CL", row=1, col=1, line_dash="dot")
        figure.add_hline(y=lcl_x, name="LCL", row=1, col=1)
        figure.add_hline(y=ucl_x, name="UCL", row=1, col=1)
        figure.add_scatter(
            x=list(range(len(x_bar))),
            y=x_bar,
            mode="lines+markers",
            row=1,
            col=1,
        )
        figure.update_xaxes(
            title="Sample", showgrid=False, zeroline=False, row=1, col=1
        )
        figure.update_yaxes(
            title="Sample Mean", showgrid=False, zeroline=False, row=1, col=1
        )
        figure.add_hline(y=cl_r, name="CL", row=2, col=1, line_dash="dot")
        figure.add_hline(y=lcl_r, name="R_LCL", row=2, col=1)
        figure.add_hline(y=ucl_r, name="R_UCL", row=2, col=1)
        figure.add_scatter(
            x=list(range(len(r))),
            y=r,
            mode="lines+markers",
            row=2,
            col=1,
        )
        figure.update_xaxes(
            title="Sample", showgrid=False, zeroline=False, row=2, col=1
        )
        figure.update_yaxes(
            title="Sample Range", showgrid=False, zeroline=False, row=2, col=1
        )
        figure.update_layout(showlegend=False)
        return figure


class XBarS:
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
        self,
        data: list,
        subgroup_size: int = 9,
    ) -> None:
        self.data = data
        self.subgroup_size = subgroup_size

    def x_bar(self) -> list:
        n = self.subgroup_size
        groups = list(batched(self.data, n))
        return list(map(mean, groups))

    def s(self) -> list:
        n = self.subgroup_size
        groups = list(batched(self.data, n))
        return list(map(stdev, groups))

    def center_line_x(self) -> float:
        x_bar = self.x_bar()
        return mean(x_bar)

    def center_line_s(self) -> float:
        s = self.s()
        return mean(s)

    def lower_control_limit_x(self) -> float:
        A3 = abc_table[self.subgroup_size].A3
        center_line_x = self.center_line_x()
        center_line_s = self.center_line_s()
        return center_line_x - (A3 * center_line_s)

    def upper_control_limit_x(self) -> float:
        A3 = abc_table[self.subgroup_size].A3
        center_line_x = self.center_line_x()
        center_line_s = self.center_line_s()
        return center_line_x + (A3 * center_line_s)

    def lower_control_limit_s(self) -> float:
        B3 = abc_table[self.subgroup_size].B3
        center_line_s = self.center_line_s()
        return B3 * center_line_s

    def upper_control_limit_s(self) -> float:
        B4 = abc_table[self.subgroup_size].B4
        center_line_s = self.center_line_s()
        return B4 * center_line_s

    def cp(self, lsl: float, usl: float) -> float:
        C4 = abc_table[self.subgroup_size].C4
        center_line_s = self.center_line_s()
        sigma = center_line_s / C4
        return (usl - lsl) / (6 * sigma)

    def cpk(self, lsl: float, usl: float) -> float:
        C4 = abc_table[self.subgroup_size].C4
        center_line_s = center_line_s()
        x_bar = self.x_bar()
        sigma = center_line_s / C4
        cpk_upper = (usl - x_bar) / (3 * sigma)
        cpk_lower = (x_bar - lsl) / (3 * sigma)
        return min((cpk_upper, cpk_lower))

    def plot(self) -> Figure:
        x_bar = self.x_bar()
        cl_x = self.center_line_x()
        lcl_x = self.lower_control_limit_x()
        ucl_x = self.upper_control_limit_x()
        s = self.s()
        cl_s = self.center_line_s()
        lcl_s = self.lower_control_limit_s()
        ucl_s = self.upper_control_limit_s()
        figure = make_subplots(rows=2, cols=1)
        figure.add_hline(y=cl_x, name="CL", row=1, col=1, line_dash="dot")
        figure.add_hline(y=lcl_x, name="LCL", row=1, col=1)
        figure.add_hline(y=ucl_x, name="UCL", row=1, col=1)
        figure.add_scatter(
            x=list(range(len(x_bar))),
            y=x_bar,
            mode="lines+markers",
            row=1,
            col=1,
        )
        figure.update_xaxes(
            title="Sample", showgrid=False, zeroline=False, row=1, col=1
        )
        figure.update_yaxes(
            title="Sample Mean", showgrid=False, zeroline=False, row=1, col=1
        )
        figure.add_hline(y=cl_s, name="CL", row=2, col=1, line_dash="dot")
        figure.add_hline(y=lcl_s, name="S_LCL", row=2, col=1)
        figure.add_hline(y=ucl_s, name="S_UCL", row=2, col=1)
        figure.add_scatter(
            x=list(range(len(s))),
            y=s,
            mode="lines+markers",
            row=2,
            col=1,
        )
        figure.update_xaxes(
            title="Sample", showgrid=False, zeroline=False, row=2, col=1
        )
        figure.update_yaxes(
            title="Sample StdDev", showgrid=False, zeroline=False, row=2, col=1
        )
        figure.update_layout(showlegend=False)
        return figure


class IMR:
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

    def __init__(self, data: list) -> None:
        self.data = data

    @property
    def mr(self) -> list:
        data = self.data
        indexes = range(1, len(data))
        func = lambda i: abs(data[i] - data[i - 1])
        return list(map(func, indexes))

    @property
    def center_line_i(self) -> float:
        return mean(self.data)

    @property
    def center_line_mr(self) -> float:
        return mean(self.mr)

    @property
    def lower_control_limit_i(self) -> float:
        return self.center_line_i - (3 * stdev(self.data))

    @property
    def upper_control_limit_i(self) -> float:
        return self.center_line_i + (3 * stdev(self.data))

    @property
    def lower_control_limit_mr(self) -> float:
        d2 = abc_table[2].d2
        return self.center_line_mr - (3 * self.center_line_i / d2)

    @property
    def upper_control_limit_mr(self) -> float:
        d2 = abc_table[2].d2
        return self.center_line_mr + (3 * self.center_line_i / d2)

    def plot(self) -> Figure:
        figure = make_subplots(rows=2, cols=1)
        figure.add_hline(y=self.center_line_i, name="CL", row=1, col=1, line_dash="dot")
        figure.add_hline(y=self.lower_control_limit_i, name="LCL", row=1, col=1)
        figure.add_hline(y=self.upper_control_limit_i, name="UCL", row=1, col=1)
        figure.add_scatter(
            x=list(range(len(self.data))),
            y=self.data,
            mode="lines+markers",
            row=1,
            col=1,
        )
        figure.update_xaxes(
            title="Observation", showgrid=False, zeroline=False, row=1, col=1
        )
        figure.update_yaxes(
            title="Individual Value", showgrid=False, zeroline=False, row=1, col=1
        )
        figure.add_hline(
            y=self.center_line_mr, name="CL", row=2, col=1, line_dash="dot"
        )
        figure.add_hline(y=self.lower_control_limit_mr, name="MR_LCL", row=2, col=1)
        figure.add_hline(y=self.upper_control_limit_mr, name="MR_UCL", row=2, col=1)
        figure.add_scatter(
            x=list(range(len(self.mr))),
            y=self.mr,
            mode="lines+markers",
            row=2,
            col=1,
        )
        figure.update_xaxes(
            title="Observation", showgrid=False, zeroline=False, row=2, col=1
        )
        figure.update_yaxes(
            title="Moving Range", showgrid=False, zeroline=False, row=2, col=1
        )
        figure.update_layout(showlegend=False)
        return figure


class P:
    """Proportion (P) chart.

    Use P Chart to monitor the proportion of
    defective items where each item can be
    classified into one of two categories,
    such as pass or fail. Use this control
    chart to monitor process stability over
    time so that you can identify and correct
    instabilities in a process.
    """

    def __init__(
        self,
        data: list,
        sample_sizes: list | int,
    ) -> None:
        self.data = data
        self.sample_sizes = sample_sizes

    def p(self) -> list | float | int:
        if isinstance(self.sample_sizes, list):
            func = lambda v: v[0] / v[1]
            z = zip(self.data, self.sample_sizes)
            return list(map(func, z))
        func = lambda v: v / self.sample_sizes
        return list(map(func, self.data))

    def center_line(self) -> float | int:
        p = self.p()
        return mean(p)

    def lower_control_limit(self) -> list | float:
        p_bar = self.center_line()
        if isinstance(self.sample_sizes, (float | int)):
            return p_bar - 3 * (p_bar * (1 - p_bar)) ** (0.5) / (
                self.sample_sizes ** (0.5)
            )
        func = lambda n: p_bar - 3 * (p_bar * (1 - p_bar)) ** (0.5) / (n ** (0.5))
        return list(map(func, self.sample_sizes))

    def upper_control_limit(self) -> list | float:
        p_bar = self.center_line()
        if isinstance(self.sample_sizes, (float | int)):
            return p_bar + 3 * (p_bar * (1 - p_bar)) ** (0.5) / (
                self.sample_sizes ** (0.5)
            )
        func = lambda n: p_bar + 3 * (p_bar * (1 - p_bar)) ** (0.5) / (n ** (0.5))
        return list(map(func, self.sample_sizes))

    def plot(self) -> Figure:
        p = self.p()
        cl = self.center_line()
        lcl = self.lower_control_limit()
        ucl = self.upper_control_limit()
        figure = Figure()
        figure.add_hline(y=cl, name="CL", line_dash="dot")
        figure.add_hline(y=lcl, name="LCL")
        figure.add_hline(y=ucl, name="UCL")
        figure.add_scatter(x=list(range(len(p))), y=p)
        figure.update_xaxes(title="Sample", showgrid=False, zeroline=False)
        figure.update_yaxes(title="Proportion", showgrid=False, zeroline=False)
        figure.update_layout(showlegend=False)
        return figure
