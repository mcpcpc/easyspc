#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: 2024 Michael Czigler
SPDX-License-Identifier: BSD-3-Clause
"""

from statistics import mean
from statistics import stdev


class RulesBase:
    def __init__(
        self,
        x: list | None = None,
        center: float | list | None = None,
        sigma: float | list | None = None,
    ) -> None:
        if not isinstance(x, list):
            self.center = center
            self.sigma = sigma
            return
        if isinstance(x[0], float):
            self.center = mean(x)
        elif isinstance(x[0], list):
            self.center = list(map(mean, x))
        if isinstance(x[0], float):
            self.sigma = stdev(x)
        elif isinstance(x[0], list):
            self.sigma = list(map(stdev, x))

    @property
    def center(self) -> list | float:
        return self._center

    @center.setter
    def center(self, value: float) -> None:
        if not isinstance(value, (float, list)):
            raise TypeError(value)
        self._center = value

    @property
    def sigma(self) -> list | float:
        return self._sigma

    @sigma.setter
    def sigma(self, value: float) -> None:
        if not isinstance(value, (float, list)):
            raise TypeError(value)
        self._sigma = value


class WECO(RulesBase):
    """Western Electric (WECO) decision rules.

    The Western Electric rules are decision rules in
    statistical process control for detecting
    out-of-control or non-random conditions on control
    charts. Locations of the observations relative to
    the control chart control limits (typically at ±3
    standard deviations) and centerline indicate
    whether the process in question should be
    investigated for assignable causes. The Western
    Electric rules were codified by a
    specially-appointed committee of the manufacturing
    division of the Western Electric Company and
    appeared in the first edition of a 1956 handbook,
    that became a standard text of the field. Their
    purpose was to ensure that line workers and
    engineers interpret control charts in a uniform
    way.

    The rules attempt to distinguish unnatural
    patterns from natural patterns based on several
    criteria: The absence of points near the
    centerline is identified as a mixture pattern.

    The absence of points near the control limits is
    identified as a stratification pattern.

    The presence of points outside the control
    limits is identified as an instability pattern.
    """

    def rule_1(self, x: list) -> bool:
        """Western Electric (WECO) Rule #1

        Any single data point falls outside the
        3σ-limit from the centerline (i.e., any point
        that falls outside Zone A, beyond either the
        upper or lower control limit)
        """

        ll = self.center - (3 * self.sigma)
        lu = self.center + (3 * self.sigma)
        func = lambda d: (d < ll) or (d > lu)
        return any(list(map(func, x)))

    def rule_2(self, x: list) -> bool:
        """Western Electric (WECO) Rule #2

        Two out of three consecutive points fall
        beyond the 2σ-limit (in zone A or beyond),
        on the same side of the centerline.
        """

        ll = self.center - (2 * self.sigma)
        lu = self.center + (2 * self.sigma)
        for i in range(1, len(x)):
            sub = x[i - 1 : i + 1]
            if sum(map(lambda d: d < ll, sub)) == 2:
                return True
            if sum(map(lambda d: d > lu, sub)) == 2:
                return True
        return False

    def rule_3(self, x: list) -> bool:
        """Western Electric (WECO) Rule #3

        Four out of five consecutive points fall
        beyond the 1σ-limit (in zone B or beyond),
        on the same side of the centerline.
        """

        ll = self.center - (1 * self.sigma)
        lu = self.center + (1 * self.sigma)
        for i in range(3, len(x)):
            sub = x[i - 3 : i + 1]
            if sum(map(lambda d: d < ll, sub)) == 4:
                return True
            if sum(map(lambda d: d > lu, sub)) == 4:
                return True
        return False

    def rule_4(self, x: list) -> bool:
        """Western Electric (WECO) Rule #4

        Eight consecutive points fall on the same
        side of the centerline (in zone C or
        beyond)
        """

        center = self.center
        for i in range(7, len(x)):
            sub = x[i - 7 : i + 1]
            if all(map(lambda d: d < center, sub)):
                return True
            if all(map(lambda d: d > center, sub)):
                return True
        return False
