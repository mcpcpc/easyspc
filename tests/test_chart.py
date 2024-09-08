#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest import main
from unittest.mock import patch

from easyspc.chart import batched
from easyspc.chart import load_template
from easyspc.chart import IMR
from easyspc.chart import XBarR
from easyspc.chart import XBarS


class ChartTestCase(TestCase):
    def test_batched(self):
        iterable = list(range(6))
        response = batched(iterable, n=2)
        self.assertEqual(len(response), 3)

    def test_batched_error(self):
        iterable = list(range(6))
        with self.assertRaises(ValueError):
            batched(iterable, n=0)

    @patch("easyspc.chart.get_data")
    def test_load_template(self, get_data_mock):
        get_data_mock.return_value = b"{}"
        load_template("test")
        get_data_mock.assert_called_once()

    @patch("easyspc.chart.get_data")
    def test_load_template_error(self, get_data_mock):
        get_data_mock.return_value = None
        with self.assertRaises(Exception):
            load_template("test")

    def test_i_mr(self):
        data = list(range(3))
        imr = IMR(data=data)
        response = imr.plot()
        self.assertIsInstance(response, dict)

    def test_x_bar_r(self):
        data = list(range(9))
        xbarr = XBarR(subgroup_size=3, data=data)
        response = xbarr.plot()
        self.assertIsInstance(response, dict)

    def test_x_bar_s(self):
        data = list(range(9))
        xbars = XBarS(subgroup_size=3, data=data)
        response = xbars.plot()
        self.assertIsInstance(response, dict)


if __name__ == "__main__":
    main()
