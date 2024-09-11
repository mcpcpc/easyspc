#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest import main
from unittest.mock import patch

from easyspc.chart import batched
from easyspc.chart import IMR
from easyspc.chart import XBarR
from easyspc.chart import XBarS
from easyspc.chart import P


class ChartTestCase(TestCase):
    def test_batched(self):
        iterable = list(range(6))
        response = list(batched(iterable, n=2))
        self.assertEqual(len(response), 3)

    def test_imr_center_line_i(self):
        data = list(range(9))
        chart = IMR(data)
        response = chart.center_line_i
        self.assertIsInstance(response, (float, int))

    def test_imr_center_line_mr(self):
        data = list(range(9))
        chart = IMR(data)
        response = chart.center_line_mr
        self.assertIsInstance(response, (float, int))

    def test_imr_lower_control_limit_i(self):
        data = list(range(9))
        chart = IMR(data)
        response = chart.lower_control_limit_i
        self.assertIsInstance(response, (float, int))

    def test_imr_upper_control_limit_i(self):
        data = list(range(9))
        chart = IMR(data)
        response = chart.upper_control_limit_i
        self.assertIsInstance(response, (float, int))

    def test_imr_lower_control_limit_mr(self):
        data = list(range(9))
        chart = IMR(data)
        response = chart.lower_control_limit_mr
        self.assertIsInstance(response, (float, int))

    def test_imr_upper_control_limit_mr(self):
        data = list(range(9))
        chart = IMR(data)
        response = chart.lower_control_limit_mr
        self.assertIsInstance(response, (float, int))

    def test_xbarr_center_line_x(self):
        data = list(range(9))
        chart = XBarR(data, subgroup_size=3)
        response = chart.center_line_x()
        self.assertIsInstance(response, (float, int))

    def test_xbarr_center_line_r(self):
        data = list(range(9))
        chart = XBarR(data, subgroup_size=3)
        response = chart.center_line_r()
        self.assertIsInstance(response, (float, int))

    def test_xbarr_lower_control_limit_x(self):
        data = list(range(9))
        chart = XBarR(data, subgroup_size=3)
        response = chart.lower_control_limit_x()
        self.assertIsInstance(response, (float, int))

    def test_xbarr_upper_control_limit_x(self):
        data = list(range(9))
        chart = XBarR(data, subgroup_size=3)
        response = chart.upper_control_limit_x()
        self.assertIsInstance(response, (float, int))

    def test_xbarr_lower_control_limit_r(self):
        data = list(range(9))
        chart = XBarR(data, subgroup_size=3)
        response = chart.lower_control_limit_r()
        self.assertIsInstance(response, (float, int))

    def test_xbarr_upper_control_limit_r(self):
        data = list(range(9))
        chart = XBarR(data, subgroup_size=3)
        response = chart.upper_control_limit_r()
        self.assertIsInstance(response, (float, int))

    def test_xbars_center_line_x(self):
        data = list(range(9))
        chart = XBarS(data, subgroup_size=3)
        response = chart.center_line_x
        self.assertIsInstance(response, (float, int))

    def test_xbars_center_line_s(self):
        data = list(range(9))
        chart = XBarS(data, subgroup_size=3)
        response = chart.center_line_s
        self.assertIsInstance(response, (float, int))

    def test_xbars_lower_control_limit_x(self):
        data = list(range(9))
        chart = XBarS(data, subgroup_size=3)
        response = chart.lower_control_limit_x
        self.assertIsInstance(response, (float, int))

    def test_xbars_upper_control_limit_x(self):
        data = list(range(9))
        chart = XBarS(data, subgroup_size=3)
        response = chart.upper_control_limit_x
        self.assertIsInstance(response, (float, int))

    def test_xbars_lower_control_limit_s(self):
        data = list(range(9))
        chart = XBarS(data, subgroup_size=3)
        response = chart.lower_control_limit_s
        self.assertIsInstance(response, (float, int))

    def test_xbars_upper_control_limit_s(self):
        data = list(range(9))
        chart = XBarS(data, subgroup_size=3)
        response = chart.lower_control_limit_s
        self.assertIsInstance(response, (float, int))

    def test_p_center_line(self):
        defects = list(range(9))
        chart = P(defects, sample_sizes=1)
        response = chart.center_line()
        self.assertIsInstance(response, (float, int))

    def test_p_lower_control_limit_constant_size(self):
        defects = [3, 5, 2, 4, 6, 1, 3, 2, 4, 3]
        chart = P(defects, sample_sizes=100)
        response = chart.lower_control_limit()
        self.assertIsInstance(response, (float, int))

    def test_p_lower_control_limit_variable_size(self):
        defects = [3, 5, 2, 4, 6, 1, 3, 2, 4, 3]
        sizes = [
            100,
        ] * 10
        chart = P(defects, sample_sizes=sizes)
        response = chart.lower_control_limit()
        self.assertIsInstance(response, list)

    def test_p_upper_control_limit_constant_size(self):
        defects = [3, 5, 2, 4, 6, 1, 3, 2, 4, 3]
        chart = P(defects, sample_sizes=100)
        response = chart.upper_control_limit()
        self.assertIsInstance(response, (float, int))

    def test_p_upper_control_limit_variable_size(self):
        defects = [3, 5, 2, 4, 6, 1, 3, 2, 4, 3]
        sizes = [
            100,
        ] * 10
        chart = P(defects, sample_sizes=sizes)
        response = chart.upper_control_limit()
        self.assertIsInstance(response, list)


if __name__ == "__main__":
    main()
