#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest import main
from unittest.mock import patch

from easyspc.chart import load_template
from easyspc.chart import imr
from easyspc.chart import xbarr
from easyspc.chart import xbars


class ChartTestCase(TestCase):
    @patch("easyspc.chart.get_data")
    def test_load_template(self, get_data_mock):
        get_data_mock.return_value = b"{}"
        load_template("test")
        get_data_mock.assert_called_once()

    def test_imr(self):
        x = [1, 2, 3]
        response = imr(x=x)
        self.assertIsInstance(response, dict)

    def test_xbarr(self):
        x = [
            list(range(3)),
        ] * 3
        response = xbarr(x=x)
        self.assertIsInstance(response, dict)

    def test_xbars(self):
        x = [
            list(range(9)),
        ] * 3
        response = xbars(x=x)
        self.assertIsInstance(response, dict)


if __name__ == "__main__":
    main()
