#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: 2024 Michael Czigler
SPDX-License-Identifier: BSD-3-Clause
"""

from collections import namedtuple

# anti-bias constants
field_names = ("A2", "A3", "d2", "D3", "D4", "B3", "B4")
abc = namedtuple(typename="abc", field_names=field_names)

# anti-bias constant look-up table
abc_table = {
    2: abc(1.880, 2.659, 1.128, 0.000, 3.267, 0.000, 3.267),
    3: abc(1.023, 1.954, 1.693, 0.000, 2.574, 0.000, 2.568),
    4: abc(0.729, 1.628, 2.059, 0.000, 2.282, 0.000, 2.266),
    5: abc(0.577, 1.427, 2.326, 0.000, 2.114, 0.000, 2.089),
    6: abc(0.483, 1.287, 2.534, 0.000, 2.004, 0.030, 1.970),
    7: abc(0.419, 1.182, 2.704, 0.076, 1.924, 0.118, 1.882),
    8: abc(0.373, 1.099, 2.847, 0.136, 1.864, 0.185, 1.815),
    9: abc(0.337, 1.032, 2.970, 0.184, 1.816, 0.239, 1.761),
    10: abc(0.308, 0.975, 3.078, 0.223, 1.777, 0.284, 1.716),
    11: abc(0.285, 0.927, 3.173, 0.256, 1.744, 0.321, 1.679),
    12: abc(0.266, 0.886, 3.258, 0.283, 1.717, 0.354, 1.646),
    13: abc(0.249, 0.850, 3.336, 0.307, 1.693, 0.382, 1.618),
    14: abc(0.235, 0.817, 3.407, 0.328, 1.672, 0.406, 1.594),
    15: abc(0.223, 0.789, 3.472, 0.347, 1.653, 0.428, 1.572),
    16: abc(0.212, 0.763, 3.532, 0.363, 1.637, 0.448, 1.552),
    17: abc(0.203, 0.739, 3.588, 0.378, 1.622, 0.466, 1.534),
    18: abc(0.194, 0.718, 3.640, 0.391, 1.608, 0.482, 1.518),
    19: abc(0.187, 0.698, 3.689, 0.403, 1.597, 0.497, 1.503),
    20: abc(0.180, 0.680, 3.735, 0.415, 1.585, 0.510, 1.490),
    21: abc(0.173, 0.663, 3.778, 0.425, 1.575, 0.523, 1.477),
    22: abc(0.167, 0.647, 3.819, 0.434, 1.566, 0.534, 1.466),
    23: abc(0.162, 0.633, 3.858, 0.443, 1.557, 0.545, 1.455),
    24: abc(0.157, 0.619, 3.895, 0.451, 1.548, 0.555, 1.445),
    25: abc(0.153, 0.606, 3.931, 0.459, 1.541, 0.565, 1.435),
}
