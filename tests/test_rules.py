#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import uniform
from unittest import TestCase
from unittest import main

from easyspc.rules import RulesBase
from easyspc.rules import WECO


class RulesBaseTestCase(TestCase):
    def test_rules_base_init_x_1d_center(self) -> None:
        x = [1.0, 2.0, 3.0]
        response = RulesBase(x=x).center
        self.assertIsInstance(response, float)

    def test_rules_base_init_x_1d_sigma(self) -> None:
        x = [1.0, 2.0, 3.0]
        response = RulesBase(x=x).sigma
        self.assertIsInstance(response, float)

    def test_rules_base_init_x_2d_center(self) -> None:
        x = [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]]
        response = RulesBase(x=x).center
        self.assertIsInstance(response, list)

    def test_rules_base_init_x_2d_sigma(self) -> None:
        x = [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]]
        response = RulesBase(x=x).sigma
        self.assertIsInstance(response, list)

    def test_rules_base_init_center_error(self) -> None:
        center, sigma = None, 1.0
        with self.assertRaises(TypeError):
            RulesBase(center=center, sigma=sigma)

    def test_rules_base_init_sigma_error(self) -> None:
        center, sigma = 1.0, None
        with self.assertRaises(TypeError):
            RulesBase(center=center, sigma=sigma)


class WECOTestCase(TestCase):
    def setUp(self) -> None:
        self.data = [uniform(-1.0, 1.0) for i in range(11)]
        self.weco = WECO(center=0.0, sigma=1.0)

    def test_weco_rule_1_true(self) -> None:
        x = self.data + [
            4.0,
        ]
        response = self.weco.rule_1(x)
        self.assertTrue(response)

    def test_weco_rule_2_true(self) -> None:
        x = self.data + (
            [
                2.5,
            ]
            * 2
        )
        response = self.weco.rule_2(x)
        self.assertTrue(response)

    def test_weco_rule_3_true(self) -> None:
        x = self.data + (
            [
                1.5,
            ]
            * 4
        )
        response = self.weco.rule_3(x)
        self.assertTrue(response)

    def test_weco_rule_4_true(self) -> None:
        x = self.data + (
            [
                0.5,
            ]
            * 8
        )
        response = self.weco.rule_4(x)
        self.assertTrue(response)


if __name__ == "__main__":
    main()
