#!/usr/bin/env python

import unittest2 as unittest
from decimal import Decimal

from pricing.products import Product
from pricing.features import IntegerFeature
from .product_mocks import get_storage_in_use, account, get_projects_in_use
from .product_helpers import GoldPlan

class ProductTests(unittest.TestCase):
    def setUp(self):
        class MySaaSAppAccount(Product):
            class Projects(IntegerFeature):
                def in_use(self, account):
                    return Projects.objects.filter(account=account).count()
        self.p = MySaaSAppAccount
        
    def tearDown(self):
        pass
    
    def test_create(self):
        feature_classes = self.p.features.values()
        self.assertIn(self.p.Projects, feature_classes)
    def test_feature_init(self):
        self.assertIsInstance(self.p().projects, self.p.Projects)

class ProductSubclassTests(unittest.TestCase):
    def setUp(self):
        self.p = GoldPlan()
        self.p_cls = GoldPlan
    def test_requires_payment_details_absent(self):
        with self.assertRaises(AttributeError):
            self.p.get_requires_payment_details()
    def test_requires_payment_details_free(self):
        self.p_cls.base_price = 0
        self.assertFalse(self.p_cls.get_requires_payment_details())
    def test_requires_payment_details_non_free(self):
        self.p_cls.base_price = 100
        self.assertTrue(self.p_cls.get_requires_payment_details())
    def test_requires_payment_details_free_forced_true(self):
        self.p_cls.base_price = 0
        self.p_cls.requires_payment_details = True
        self.assertTrue(self.p_cls.get_requires_payment_details())
    def test_requires_payment_details_non_free_forced_false(self):
        self.p_cls.base_price = 100
        self.p_cls.requires_payment_details = False
        self.assertFalse(self.p.get_requires_payment_details())
    def test_name(self):
        self.assertEqual(self.p.name, 'GoldPlan')
    def test_verbose_name(self):
        self.assertEqual(self.p.verbose_name, 'gold plan')

def main():
    unittest.main()

if __name__ == '__main__':
    main()
