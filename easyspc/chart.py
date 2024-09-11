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

    def cp(self, lsl: float, usl: float) -> float:
        """Process capability ratio.""" 

        d2 = abc_table[self.subgroup_size].d2
        sigma = self.center_line_r / d2
        return (usl - lsl) / (6 * sigma)

    def cpk(self, lsl: float, usl: float) -> float:
        """Process performance ratio."""

        d2 = abc_table[self.subgroup_size].d2
        sigma = self.center_line_r / d2
        cpk_upper = (usl - self.x_bar) / (3 * sigma)
        cpk_lower = (self.x_bar - lsl) / (3 * sigma)
        return min((cpk_upper, cpk_lower))

    def plot(self) -> Figure:
        figure = make_subplots(rows=2, cols=1)
        figure.add_hline(y=self.center_line_x, name="CL", row=1, col=1, line_dash="dot")
        figure.add_hline(y=self.lower_control_limit_x, name="LCL", row=1, col=1)
        figure.add_hline(y=self.upper_control_limit_x, name="UCL", row=1, col=1)
        figure.add_scatter(
            x=list(range(len(self.x_bar))),
            y=self.x_bar,
            mode="lines+markers",
            row=1,
            col=1,
        )
        figure.update_xaxes(title="Sample", showgrid=False, zeroline=False, row=1, col=1)
        figure.update_yaxes(title="Sample Mean", showgrid=False, zeroline=False, row=1, col=1)
        figure.add_hline(y=self.center_line_r, name="CL", row=2, col=1, line_dash="dot")
        figure.add_hline(y=self.lower_control_limit_r, name="R_LCL", row=2, col=1)
        figure.add_hline(y=self.upper_control_limit_r, name="R_UCL", row=2, col=1)
        figure.add_scatter(
            x=list(range(len(self.r))),
            y=self.r,
            mode="lines+markers",
            row=2,
            col=1,
        )
        figure.update_xaxes(title="Sample", showgrid=False, zeroline=False, row=2, col=1)
        figure.update_yaxes(title="Sample Range", showgrid=False, zeroline=False, row=2, col=1)
        figure.update_layout(showlegend=False)
        return figure

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

    def cp(self, lsl: float, usl: float) -> float:
        """Process capability ratio.""" 

        C4 = abc_table[self.subgroup_size].C4
        sigma = self.center_line_s / C4
        return (usl - lsl) / (6 * sigma)

    def cpk(self, lsl: float, usl: float) -> float:
        """Process performance ratio."""

        C4 = abc_table[self.subgroup_size].C4
        sigma = self.center_line_s / C4
        cpk_upper = (usl - self.x_bar) / (3 * sigma)
        cpk_lower = (self.x_bar - lsl) / (3 * sigma)
        return min((cpk_upper, cpk_lower))

    def plot(self) -> Figure:
        figure = make_subplots(rows=2, cols=1)
        figure.add_hline(y=self.center_line_x, name="CL", row=1, col=1, line_dash="dot")
        figure.add_hline(y=self.lower_control_limit_x, name="LCL", row=1, col=1)
        figure.add_hline(y=self.upper_control_limit_x, name="UCL", row=1, col=1)
        figure.add_scatter(
            x=list(range(len(self.x_bar))),
            y=self.x_bar,
            mode="lines+markers",
            row=1,
            col=1,
        )
        figure.update_xaxes(title="Sample", showgrid=False, zeroline=False, row=1, col=1)
        figure.update_yaxes(title="Sample Mean", showgrid=False, zeroline=False, row=1, col=1)
        figure.add_hline(y=self.center_line_s, name="CL", row=2, col=1, line_dash="dot")
        figure.add_hline(y=self.lower_control_limit_s, name="S_LCL", row=2, col=1)
        figure.add_hline(y=self.upper_control_limit_s, name="S_UCL", row=2, col=1)
        figure.add_scatter(
            x=list(range(len(self.s))),
            y=self.s,
            mode="lines+markers",
            row=2,
            col=1,
        )
        figure.update_xaxes(title="Sample", showgrid=False, zeroline=False, row=2, col=1)
        figure.update_yaxes(title="Sample StdDev", showgrid=False, zeroline=False, row=2, col=1)
        figure.update_layout(showlegend=False)
        return figure

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
        d2 = abc_table[2].d2
        return self.center_line_mr - (
            3 * self.center_line_i / d2
        )

    @property
    def upper_control_limit_mr(self) -> float:
        d2 = abc_table[2].d2
        return self.center_line_mr + (
            3 * self.center_line_i / d2
        ) 

    def plot(self) -> Figure:
        figure = make_subplots(rows=2, cols=1)
        figure.add_hline(y=self.center_line_i, name="CL", row=1, col=1, line_dash="dot")
        figure.add_hline(y=self.lower_control_limit_i, name="LCL", row=1, col=1)
        figure.add_hline(y=self.upper_control_limit_i, name="UCL", row=1, col=1)
        figure.add_scatter(
            x=list(range(len(self.i))),
            y=self.i,
            mode="lines+markers",
            row=1,
            col=1,
        )
        figure.update_xaxes(title="Observation", showgrid=False, zeroline=False, row=1, col=1)
        figure.update_yaxes(title="Individual Value", showgrid=False, zeroline=False, row=1, col=1)
        figure.add_hline(y=self.center_line_mr, name="CL", row=2, col=1, line_dash="dot")
        figure.add_hline(y=self.lower_control_limit_mr, name="MR_LCL", row=2, col=1)
        figure.add_hline(y=self.upper_control_limit_mr, name="MR_UCL", row=2, col=1)
        figure.add_scatter(
            x=list(range(len(self.mr))),
            y=self.mr,
            mode="lines+markers",
            row=2,
            col=1,
        )
        figure.update_xaxes(title="Observation", showgrid=False, zeroline=False, row=2, col=1)
        figure.update_yaxes(title="Moving Range", showgrid=False, zeroline=False, row=2, col=1)
        figure.update_layout(showlegend=False)
        return figure

    def summary(self) -> None:
        print("I Chart Summary:")
        print(f"Center Line (CL): {self.center_line_i:.3f}")
        print(f"Upper Control Limit (UCL): {self.upper_control_limit_i:.3f}")
        print(f"Lower Control Limit (UCL): {self.lower_control_limit_i:.3f}")
        print("MR Summary:")
        print(f"Center Line (CL): {self.center_line_s:.3f}")
        print(f"Upper Control Limit (UCL): {self.upper_control_limit_mr:.3f}")
        print(f"Lower Control Limit (UCL): {self.lower_control_limit_mr:.3f}")


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
    defects: list,
    sample_sizes: list | int, 
) -> None:
    self.defects = defects
    self.sample_sizes = sample_sizes
 
    @property
    def p(self) -> list | float | int:
        if isinstance(self.sample_sizes, list):
            func = lambda v: v[0] / v[1]
            z = zip(self.defects, self.sample_sizes)
            return list(map(func, z))
        func = lambda v: v / self.sample_sizes
        return list(map(func, self.defects))
 
    @property
    def center_line(self) -> float | int:
        return mean(self.p)
 
    @property
    def upper_control_limit(self) -> list | float:
        p_bar = self.center_line
        if isinstance(p_bar, list):
            return p_bar + 3 * (
                p_bar * (1 - p_bar)
            ) ** (.5) / (self.sample_sizes ** (.5))
        func = lambda n: p_bar + 3 * (
            p_bar * (1 - p_bar)
        ) ** (.5) / (n ** (.5))
        return list(map(func, self.sample_sizes))

    @property
    def lower_control_limit(self) -> list | float:
        p_bar = self.center_line
        if isinstance(p_bar, list):
            return p_bar - 3 * (
                p_bar * (1 - p_bar)
            ) ** (.5) / (self.sample_sizes ** (.5))
        func = lambda n: p_bar - 3 * (
            p_bar * (1 - p_bar)
        ) ** (.5) / (n ** (.5))
        return list(map(func, self.sample_sizes))

    def plot(self) -> Figure:
        figure = Figure()
        figure.add_hline(y=self.p_bar, name="CL", line_dash="dot")
        figure.add_hline(y=self.lower_control_limit, name="LCL")
        figure.add_hline(y=self.upper_control_limit, name="UCL")
        figure.add_scatter(x=list(map(len(self.p))), y=self.p)
        figure.update_xaxes(title="Sample", showgrid=False, zeroline=False, row=2, col=1)
        figure.update_yaxes(title="P", showgrid=False, zeroline=False, row=2, col=1)
        figure.update_layout(showlegend=False)
        return figure

    def summary(self) -> None:
        print("P Chart Summary:")
        print(f"Center Line (CL): {self.center_line:.3f}")
        print(f"Upper Control Limit (UCL): {max(self.upper_control_limit:.3f}")
        print(f"Lower Control Limit (UCL): {min(self.lower_control_limit:.3f}")
        print(f"Number of Samples: {len(self.p)}")
