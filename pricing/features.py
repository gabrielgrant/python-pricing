"""
Features are composed by mixing in a FeatureValue type with a
FeatureProvisioningScheme type.
"""
from dsl_tools import KWArgAutoSaver

class FeatureValue(object):
    def clean_value(self, value):
        raise NotImplementedError('clean_value function must be overridden')
    def in_use(self, account):
        """ returns the current value for the given account """
        raise NotImplementedError('in_use function must be overridden')
    def get_instance_name(self):
        cls_name = self.__class__.__name__
        def unclassy(c):
            return c.islower() and c or '_%s' % c.lower()
        auto_instance_name = ''.join(unclassy(c) for c in cls_name).strip('_')
        name = getattr(self, 'instance_name', auto_instance_name)
        return name

class BooleanFeature(FeatureValue):
    def clean_value(self, value):
        if not bool(value) == value:
            raise ValueError('value must cleanly convert to a bool')
        return bool(value)

class IntegerFeature(FeatureValue):
    def clean_value(self, value):
        if not int(value) == value:
            raise ValueError('value must cleanly convert to an int')
        return int(value)

class SingleChoiceFeature(FeatureValue):
    """ choose one of many """
    def __init__(self, choices=None, *args, **kwargs):
        if choices is not None:
            print 'setting choices:', choices
            self.choices = choices
        # check choices for validity
        for k,v in self.choices:
            pass
        super(SingleChoiceFeature, self).__init__(*args, **kwargs)
    def clean_value(self, value):
        keys = zip(*self.choices)[0]
        if not value in keys:
            raise ValueError('value must be in choice keys')
        return value

#TODO
class MultiChoiceFeature(FeatureValue):
    """ choose X of many """
    def __init__(self, choices):
        raise NotImplementedError


class FeatureProvisioningScheme(KWArgAutoSaver):
    pass

class AllocatedFeature(FeatureProvisioningScheme):
    def get_initial_allocation(self):
        max_free_allocation = self.pricing_scheme.free_units()
        return getattr(self, 'initial_allocation', max_free_allocation)

class MeteredFeature(FeatureProvisioningScheme):
    pass  
