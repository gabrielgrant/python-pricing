#!/usr/bin/env python

import unittest2 as unittest
from decimal import Decimal

from pricing.feature_pricing import *


class FeaturePricingSchemeTests(unittest.TestCase):
    def test_clean_int_price(self):
        # 12 -> Decimal(12)
        self.assertEqual(FeaturePricingScheme.clean_price(12), Decimal(12))
    def test_clean_decimal_price(self):
        # Decimal(12) -> Decimal(12)
        self.assertEqual(
            FeaturePricingScheme.clean_price(Decimal(12)), Decimal(12)
        )
    def test_clean_floatstr_price(self):
        # '1.23' -> Decimal('1.23')
        self.assertEqual(
            FeaturePricingScheme.clean_price('1.23'), Decimal('1.23')
        )
    def test_clean_int_price(self):
        # 0.1 -> ValueError
        with self.assertRaises(ValueError):
            FeaturePricingScheme.clean_price(0.1)
    @unittest.expectedFailure
    def test_clean_floatstr_price(self):
        # 0.125 -> Decimal('0.125')  # ideally, but not necesary
        self.assertEqual(
            FeaturePricingScheme.clean_price(.125), Decimal('0.125')
        )
    def test_total_not_implemented(self):
        # 0.1 -> ValueError
        with self.assertRaises(NotImplementedError):
            FeaturePricingScheme().total(3)
    def test_free_units_not_implemented(self):
        # 0.1 -> ValueError
        with self.assertRaises(NotImplementedError):
            FeaturePricingScheme().free_units()


class FixedUnitPricingTests(unittest.TestCase):
    def test_get_unit_price(self):
        self.assertEqual(FixedUnitPricing(unit_price=12).get_unit_price(), 12)
    def test_total(self):
        self.assertEqual(FixedUnitPricing(unit_price=4).total(3), 12)
    def test_free_units_none(self):
        self.assertEqual(FixedUnitPricing(unit_price=4).free_units(), 0)
    def test_free_units_unlimited(self):
        self.assertEqual(FixedUnitPricing(unit_price=0).free_units(), UNLIMITED)


class BracketedPricingTests(unittest.TestCase):
    def test_find_bracket(self):
        bp = BracketedPricing(price_brackets=[
            (10,4),(20,3), (30,2), (INFINITY, 1)
        ])
        self.assertEqual(bp.find_bracket(5), 0)
        self.assertEqual(bp.find_bracket(15), 1)
        self.assertEqual(bp.find_bracket(25), 2)
        self.assertEqual(bp.find_bracket(35), 3)
        self.assertEqual(bp.find_bracket(20), 1)
    def test_brackets_out_of_order(self):
        with self.assertRaises(ValueError):
            BracketedPricing(price_brackets=[
                (10,4), (30,2), (INFINITY, 1),(20,3)
            ])
    def test_free_units_none(self):
        p = BracketedPricing(price_brackets=[
            (10,4),(20,3), (30,2)
        ])
        self.assertEqual(p.free_units(), 0)
    def test_free_units(self):
        p = BracketedPricing(price_brackets=[
            (10,0),(20,3), (30,2)
        ])
        self.assertEqual(p.free_units(), 10)
        

class FixedInclusionTests(unittest.TestCase):
    def setUp(self):
        self.p = FixedInclusion(included=10)
    def test_total_allowed(self):
        self.assertEqual(self.p.total(8), 0)
    def test_total_gt_inclusion(self):
        with self.assertRaises(ValueError):
            self.p.total(12)
    def test_free_units(self):
        self.assertEqual(self.p.free_units(), 10)

class VolumePricingTests(unittest.TestCase):
    @unittest.expectedFailure
    def test_it_all(self):
        self.assertEqual(1,2)


class TieredPricingTests(unittest.TestCase):
    @unittest.expectedFailure
    def test_it_all(self):
        self.assertEqual(1,2)

class StairStepPricingTests(unittest.TestCase):
    @unittest.expectedFailure
    def test_it_all(self):
        self.assertEqual(1,2)

class VolumePricingTests(unittest.TestCase):
    @unittest.expectedFailure
    def test_it_all(self):
        self.assertEqual(1,2)


class PricingTests(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    @unittest.expectedFailure
    def test_it_all(self):
        self.assertEqual(1,2)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
