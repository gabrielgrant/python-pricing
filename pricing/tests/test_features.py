#!/usr/bin/env python

import unittest2 as unittest
from decimal import Decimal
from mock import Mock


from pricing.features import *
from pricing.feature_pricing import FixedInclusion


class FeatureTests(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    @unittest.expectedFailure
    def test_it_all(self):
        self.assertEqual(1,2)

class FeatureValueTests(unittest.TestCase):
    def setUp(self):
        self.f = FeatureValue()
    def test_clean_value(self):
        with self.assertRaises(NotImplementedError):
            self.f.clean_value(3)
    def test_in_use(self):
        account = Mock(name='account')
        with self.assertRaises(NotImplementedError):
            self.f.in_use(account)
    @unittest.expectedFailure
    def test_initial_value(self):
        self.assertEqual(self.f.get_initial_value(), None)
    def test_get_name(self):
        self.assertEqual(self.f.get_instance_name(), 'feature_value')


class BooleanFeatureTests(unittest.TestCase):
    def setUp(self):
        self.f = BooleanFeature()
    def test_clean_value_int(self):
        with self.assertRaises(ValueError):
            self.f.clean_value(3)
    def test_clean_value_bool(self):
        self.assertEqual(self.f.clean_value(True), True)

class IntegerFeatureTests(unittest.TestCase):
    def setUp(self):
        self.f = IntegerFeature()
    def test_clean_value_str(self):
        with self.assertRaises(ValueError):
            self.f.clean_value('a str')
    def test_clean_value_int(self):
        self.assertEqual(self.f.clean_value(3), 3)
    def test_clean_value_whole_float(self):
        self.assertEqual(self.f.clean_value(3.0), 3)
    def test_clean_value_fractional_float(self):
        with self.assertRaises(ValueError):
            self.f.clean_value(1.25)

class SingleChoiceFeatureTests(unittest.TestCase):
    def setUp(self):
        self.f = SingleChoiceFeature(choices=[(1, 'one'), (2, 'two')])
    def test_clean_value_not_a_k_or_v(self):
        with self.assertRaises(ValueError):
            self.f.clean_value(3)
    def test_clean_value_key(self):
        self.assertEqual(self.f.clean_value(2), 2)
    def test_clean_value_value(self):
        with self.assertRaises(ValueError):
            self.f.clean_value('two')

#TODO
class MultiChoiceFeatureTests(unittest.TestCase):
    def setUp(self):
        pass
        #self.f = MultiChoiceFeature(choices=[(1, 'one'), (2, 'two')])
    @unittest.expectedFailure
    def test_clean_value_not_a_k_or_v(self):
        with self.assertRaises(ValueError):
            #self.f.clean_value(3)
            pass

class FeatureProvisioningSchemeTests(unittest.TestCase):
    def setUp(self):
        self.pricing_scheme = Mock(name='pricing_scheme')
        self.f = FeatureProvisioningScheme(pricing_scheme=self.pricing_scheme)
    def test_init(self):
        f = FeatureProvisioningScheme()
        self.assertIsInstance(f, FeatureProvisioningScheme)
    def test_pricing_scheme(self):
        self.assertEqual(self.f.pricing_scheme, self.pricing_scheme)

class AllocatedFeatureTests(unittest.TestCase):
    def setUp(self):
        self.pricing_scheme = Mock(name='pricing_scheme')
        self.pricing_scheme.free_units.return_value = 3
        self.f = AllocatedFeature(pricing_scheme=self.pricing_scheme)
    def test_init(self):
        f = AllocatedFeature()
        self.assertIsInstance(f, FeatureProvisioningScheme)
    def test_get_initial_allocation_default(self):
        self.assertEqual(self.f.get_initial_allocation(), 3)
    def test_get_initial_allocation_custom(self):
        self.f.initial_allocation = 2
        self.assertEqual(self.f.get_initial_allocation(), 2)
    def test_get_initial_allocation_default_real(self):
        f = AllocatedFeature(pricing_scheme=FixedInclusion(included=3))
        self.assertEqual(self.f.get_initial_allocation(), 3)

class MeteredFeatureTests(unittest.TestCase):
    def setUp(self):
        pass
    def test_init(self):
        f = MeteredFeature()
        self.assertIsInstance(f, FeatureProvisioningScheme)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
