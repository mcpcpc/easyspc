#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: 2024 Michael Czigler
SPDX-License-Identifier: BSD-3-Clause
"""

from json import loads
from pkgutil import get_data
from statistics import mean
from statistics import stdev

from .const import abc_table


def load_template(name: str) -> dict:
    """Load template resource."""

    data = get_data(__name__, name)
    if not isinstance(data, bytes):
        raise Exception
    template = loads(data.decode())
    return template


def imr(x: list) -> dict:
    """Individual moving range (I-MR) template.

    Use I-MR Chart to monitor the mean and
    variation of your process when you have
    continuous data that are individual
    observations not in subgroups. Use this
    control chart to monitor process
    stability over time so that you can
    identify and correct instabilities in a
    process.
    """

    template = load_template("plotly.json")
    observations = list(range(1, len(x) + 1))
    center, sigma = mean(x), stdev(x)
    func = lambda i: abs(x[i] - x[i - 1])
    mr = list(map(func, range(1, len(x))))
    mr_bar = mean(mr)
    lcl = center - (3 * sigma)
    ucl = center + (3 * sigma)
    mr_lcl = mr_bar - (3 * center / 1.128)
    mr_ucl = mr_bar + (3 * center / 1.128)
    template["data"][0]["x"] = observations
    template["data"][0]["y"] = x
    template["data"][1]["x"] = observations[1:]
    template["data"][1]["y"] = mr
    template["layout"]["annotations"][0]["text"] = f"{center:.3f}"
    template["layout"]["annotations"][0]["y"] = center
    template["layout"]["annotations"][1]["text"] = f"{mr_bar:.3f}"
    template["layout"]["annotations"][1]["y"] = mr_bar
    template["layout"]["shapes"][0]["name"] = "Center"
    template["layout"]["shapes"][0]["y0"] = center
    template["layout"]["shapes"][0]["y1"] = center
    template["layout"]["shapes"][1]["name"] = "UCL"
    template["layout"]["shapes"][1]["y0"] = ucl
    template["layout"]["shapes"][1]["y1"] = ucl
    template["layout"]["shapes"][2]["name"] = "LCL"
    template["layout"]["shapes"][2]["y0"] = lcl
    template["layout"]["shapes"][2]["y1"] = lcl
    template["layout"]["shapes"][3]["name"] = "MRBar"
    template["layout"]["shapes"][3]["y0"] = mr_bar
    template["layout"]["shapes"][3]["y1"] = mr_bar
    template["layout"]["shapes"][4]["name"] = "MR_LCL"
    template["layout"]["shapes"][4]["y0"] = mr_lcl
    template["layout"]["shapes"][4]["y1"] = mr_lcl
    template["layout"]["shapes"][5]["name"] = "MR_UCL"
    template["layout"]["shapes"][5]["y0"] = mr_ucl
    template["layout"]["shapes"][5]["y1"] = mr_ucl
    template["layout"]["xaxis"]["title"]["text"] = "Observation"
    template["layout"]["xaxis2"]["title"]["text"] = "Observation"
    template["layout"]["yaxis"]["title"]["text"] = "Individual Value"
    template["layout"]["yaxis2"]["title"]["text"] = "Moving Range"
    return template


def xbarr(x: list) -> dict:
    """Average Sample Range (XBar-R) template.

    Use Xbar-R Chart to monitor the mean and
    variation of a process when you have
    continuous data and subgroup sizes of 8
    or less. Use this control chart to monitor
    process stability over time so that you
    can identify and correct instabilities in
    a process.
    """

    template = load_template("plotly.json")
    A2 = abc_table[len(x[0])].A2
    D3 = abc_table[len(x[0])].D3
    D4 = abc_table[len(x[0])].D4
    x_bar = list(map(mean, x))
    x_grand_mean = mean(x_bar)
    func = lambda v: max(v) - min(v)
    r = list(map(func, x))
    r_bar = mean(r)
    lcl = x_grand_mean - (A2 * r_bar)
    ucl = x_grand_mean + (A2 * r_bar)
    r_lcl = D3 * r_bar
    r_ucl = D4 * r_bar
    sample = list(range(len(x)))
    template["data"][0]["x"] = sample
    template["data"][0]["y"] = x_bar
    template["data"][1]["x"] = sample
    template["data"][1]["y"] = r
    template["layout"]["annotations"][0]["text"] = f"{x_grand_mean:.3f}"
    template["layout"]["annotations"][0]["y"] = x_grand_mean
    template["layout"]["annotations"][1]["text"] = f"{r_bar:.3f}"
    template["layout"]["annotations"][1]["y"] = r_bar
    template["layout"]["shapes"][0]["name"] = "Center"
    template["layout"]["shapes"][0]["y0"] = x_grand_mean
    template["layout"]["shapes"][0]["y1"] = x_grand_mean
    template["layout"]["shapes"][1]["name"] = "UCL"
    template["layout"]["shapes"][1]["y0"] = ucl
    template["layout"]["shapes"][1]["y1"] = ucl
    template["layout"]["shapes"][2]["name"] = "LCL"
    template["layout"]["shapes"][2]["y0"] = lcl
    template["layout"]["shapes"][2]["y1"] = lcl
    template["layout"]["shapes"][3]["name"] = "Rbar"
    template["layout"]["shapes"][3]["y0"] = r_bar
    template["layout"]["shapes"][3]["y1"] = r_bar
    template["layout"]["shapes"][4]["name"] = "MR_LCL"
    template["layout"]["shapes"][4]["y0"] = r_lcl
    template["layout"]["shapes"][4]["y1"] = r_lcl
    template["layout"]["shapes"][5]["name"] = "MR_UCL"
    template["layout"]["shapes"][5]["y0"] = r_ucl
    template["layout"]["shapes"][5]["y1"] = r_ucl
    template["layout"]["xaxis"]["title"]["text"] = "Sample"
    template["layout"]["xaxis2"]["title"]["text"] = "Sample"
    template["layout"]["yaxis"]["title"]["text"] = "Sample Mean"
    template["layout"]["yaxis2"]["title"]["text"] = "Sample Range"
    return template


def xbars(x: list) -> dict:
    """Average Sample STDEV (XBar-S) template.

    Use Xbar-S Chart to monitor the mean and
    variation of a process when you have
    continuous data and subgroup sizes of 9 or
    more. Use this control chart to monitor
    process stability over time so that you
    can identify and correct instabilities in
    a process.
    """

    template = load_template("plotly.json")
    A3 = abc_table[len(x[0])].A3
    B3 = abc_table[len(x[0])].B3
    B4 = abc_table[len(x[0])].B4
    x_bar = list(map(mean, x))
    x_grand_mean = mean(x_bar)
    s = list(map(stdev, x))
    s_bar = mean(s)
    lcl = x_grand_mean - (A3 * s_bar)
    ucl = x_grand_mean + (A3 * s_bar)
    s_lcl = B3 * s_bar
    s_ucl = B4 * s_bar
    sample = list(range(len(x)))
    template["data"][0]["x"] = sample
    template["data"][0]["y"] = x_bar
    template["data"][1]["x"] = sample
    template["data"][1]["y"] = s
    template["layout"]["annotations"][0]["text"] = f"{x_grand_mean:.3f}"
    template["layout"]["annotations"][0]["y"] = x_grand_mean
    template["layout"]["annotations"][1]["text"] = f"{s_bar:.3f}"
    template["layout"]["annotations"][1]["y"] = s_bar
    template["layout"]["shapes"][0]["name"] = "Center"
    template["layout"]["shapes"][0]["y0"] = x_grand_mean
    template["layout"]["shapes"][0]["y1"] = x_grand_mean
    template["layout"]["shapes"][1]["name"] = "UCL"
    template["layout"]["shapes"][1]["y0"] = ucl
    template["layout"]["shapes"][1]["y1"] = ucl
    template["layout"]["shapes"][2]["name"] = "LCL"
    template["layout"]["shapes"][2]["y0"] = lcl
    template["layout"]["shapes"][2]["y1"] = lcl
    template["layout"]["shapes"][3]["name"] = "SBar"
    template["layout"]["shapes"][3]["y0"] = s_bar
    template["layout"]["shapes"][3]["y1"] = s_bar
    template["layout"]["shapes"][4]["name"] = "S_LCL"
    template["layout"]["shapes"][4]["y0"] = s_lcl
    template["layout"]["shapes"][4]["y1"] = s_lcl
    template["layout"]["shapes"][5]["name"] = "S_UCL"
    template["layout"]["shapes"][5]["y0"] = s_ucl
    template["layout"]["shapes"][5]["y1"] = s_ucl
    template["layout"]["xaxis"]["title"]["text"] = "Sample"
    template["layout"]["xaxis2"]["title"]["text"] = "Sample"
    template["layout"]["yaxis"]["title"]["text"] = "Sample Mean"
    template["layout"]["yaxis2"]["title"]["text"] = "Sample StdDev"
    return template
