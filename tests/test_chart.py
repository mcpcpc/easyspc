#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest import main
from unittest.mock import patch

from easyspc.chart import batched
from easyspc.chart import ChartBase
from easyspc.chart import IMR
from easyspc.chart import XBarR
from easyspc.chart import XBarS


class ChartTestCase(TestCase):
    def test_batched(self):
        iterable = list(range(6))
        response = list(batched(iterable, n=2))
        self.assertEqual(len(response), 3)

    @patch("easyspc.chart.get_data")
    def test_chart_base_get_template(self, get_data_mock):
        get_data_mock.return_value = b"{}"
        base = ChartBase()
        base.get_template()
        get_data_mock.assert_called_once()

    def test_xbarr_center_line_x(self):
        data = list(range(9))
        chart = XBarR(data, subgroup_size=3)
        response = chart.center_line_x
        self.assertIsInstance(response, (float, int))

    def test_xbarr_center_line_r(self):
        data = list(range(9))
        chart = XBarR(data, subgroup_size=3)
        response = chart.center_line_r
        self.assertIsInstance(response, (float, int))

    def test_xbarr_lower_control_limit_x(self):
        data = list(range(9))
        chart = XBarR(data, subgroup_size=3)
        response = chart.lower_control_limit_x
        self.assertIsInstance(response, (float, int))

    def test_xbarr_upper_control_limit_x(self):
        data = list(range(9))
        chart = XBarR(data, subgroup_size=3)
        response = chart.upper_control_limit_x
        self.assertIsInstance(response, (float, int))

    def test_xbarr_lower_control_limit_r(self):
        data = list(range(9))
        chart = XBarR(data, subgroup_size=3)
        response = chart.lower_control_limit_r
        self.assertIsInstance(response, (float, int))

    def test_xbarr_upper_control_limit_r(self):
        data = list(range(9))
        chart = XBarR(data, subgroup_size=3)
        response = chart.lower_control_limit_r
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


if __name__ == "__main__":
    main()
