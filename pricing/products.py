import dsl_tools

from pricing.features import FeatureValue

def name_set_callback(declaration, name):
    declaration.name = name

def filter_func(obj):
    return type(obj) == type and issubclass(obj, FeatureValue)

ProductMetaclass = dsl_tools.make_declarative_metaclass(
    filter_func=filter_func,
    declarations_name='features',
    set_declaration_name_callback=name_set_callback,
    remove_declaration=False,
)
            
class Product(object):
    __metaclass__ = ProductMetaclass
    manual_intervention = None
    def __init__(self):
        for f_cls in self.features.values():
            f = f_cls()
            setattr(self, f.get_instance_name(), f)
    @classmethod
    def get_requires_payment_details(cls):
        """
        Returns whether or not payment details are required for this product.

        Uses `requires_payment_details` if set, else it falls back to
        returning whether `base_price > 0`
        """
        return getattr(cls, 'requires_payment_details', cls.base_price > 0)
    @dsl_tools.ReadOnlyClassProperty
    def name(cls):
        return cls.__name__
    @dsl_tools.ReadOnlyClassProperty
    def verbose_name(cls):
        cls_name = cls.__name__
        def unclassy(c):
            return c.islower() and c or ' %s' % c.lower()
        return ''.join(unclassy(c) for c in cls_name).strip(' ')
