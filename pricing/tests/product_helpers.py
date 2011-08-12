from pricing.products import Product
from pricing.features import IntegerFeature
from pricing.features import AllocatedFeature, MeteredFeature
from pricing.feature_pricing import FixedInclusion, FixedUnitPricing

class MySaaSAppAccount(Product):
    class Projects(IntegerFeature):
        def in_use(self, account):
            return Projects.objects.filter(account=account).count()
    
    class StorageSpace(IntegerFeature):
        """ 
        Assume we get hourly ticks that update how much storage is used
        at that moment. If we got real-time updates every time storage
        usage changed, then the billing scheme would be Allocated instead.
        
        """
        def in_use(self, account):
            return get_storage_in_use(account.user)


class GoldPlan(MySaaSAppAccount):
    class Projects(MySaaSAppAccount.Projects, AllocatedFeature):
        pricing_scheme=FixedInclusion(included=10)
    class StorageSpace(MySaaSAppAccount.StorageSpace, MeteredFeature):
        pricing_scheme=FixedUnitPricing(unit_price='0.10')
        

