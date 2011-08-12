from decimal import Decimal

from dsl_tools import KWArgAutoSaver

UNLIMITED = Decimal('inf')
INFINITY = Decimal('inf')

class FeaturePricingScheme(KWArgAutoSaver):
    @staticmethod
    def clean_price(price):
        try:
            clean_price_as_str = str(Decimal(price))
        except TypeError:
            clean_price_as_str = None
        if Decimal(str(price)) == price:
            return Decimal(str(price))
        elif clean_price_as_str == price:
            return Decimal(price)
        else:
            raise ValueError('price must cleanly convert to a Decimal')
    def total(self, units):
        raise NotImplementedError('the "total" function should be overridden')
    def free_units(self):
        raise NotImplementedError(
            'the "free_units" function should be overridden'
        )




class FixedUnitPricing(FeaturePricingScheme):
    """
    Fixed price per unit
    
    eg. $1 / GB
    
    note that "units" don't have to be increments of one -- they could be, for
    example, 5GB blocks, so pricing could be $3 / 5GB
    
    required settings:
        unit_price or override get_unit_price function
    """
    def get_unit_price(self):
        """ 
        returns the unit price as an integer or Decimal
        
        returns self.unit_price by default
        """
        return self.unit_price
    def total(self, units):
        return units * self.get_unit_price()
    def free_units(self):
        if self.unit_price == 0:
            return UNLIMITED
        else:
            return 0

class BracketedPricing(FeaturePricingScheme):
    """
    Price per unit depends on number of units purchased
    
    "brackets" is a list of (quantity, price) tuples
    
    "quantity" is the upper end of the bracket
    the final quantity can be billing.INFINITE
    
    BracketedPricing(price_brackets, start_quantity)
    """
    def __init__(self, *args, **kwargs):
        super(BracketedPricing, self).__init__(*args, **kwargs)
        self.validate_price_brackets()
    def find_bracket(self, units):
        for i, (b, p) in enumerate(self.price_brackets):
            if units <= b:
                return i
    def validate_price_brackets(self):
        zipped_brackets = zip(self.price_brackets, self.price_brackets[1:])
        for (b1, p1), (b2, p2) in zipped_brackets:
            if not b1 < b2:
                raise ValueError(
                    'price brackets must be monotonically increasing')
    def free_units(self):
        free = 0
        for b, p in self.price_brackets:
            if p == 0:
                free = b
        return free
    

class FixedInclusion(FeaturePricingScheme):
    """
    A fixed number of units are included at no cost. No more units
    can be used beyond that initial maximum.
    
    "included" is the number of units to include
    """
    def total(self, value):
        if value > self.included:
            raise ValueError('used value exceeds number included')
        return 0
    def free_units(self):
        return self.included
