class computed_property:
    def __init__(self, *dependencies):
        self.dependencies = dependencies # dependencies ('x', 'y', 'z')
        self.cache_name = f"__{id(self)}_cache__" # name of the cache using instance id to avoid conflict
        self.dep_hash_name = f"__{id(self)}_dep_hash__" # dependencies hash to compare received values when calling func
        self.func = None # ref to func
        self.setter_func = None # ref to setter
        self.deleter_func = None # ref to deleter

    def __call__(self, func):
        """When attributed to a function, set it in the reference and copy docs to keep documentation consistency"""
        self.func = func
        self.__doc__ = func.__doc__
        return self

    def __get__(self, instance, owner):
        """Check if is being called from an instance. 
            If is not, return self. If it is, check for cache and deps hash existance and.
            Check if deps hash changed with the received params. If so, recalculate the cached value.

            Returns the cached value.
            """
        if instance is None:
            return self
        # Create cache and dependency hash attributes if they do not exist
        if not hasattr(instance, self.cache_name):
            setattr(instance, self.cache_name, None)
            setattr(instance, self.dep_hash_name, None)

        cache = getattr(instance, self.cache_name)
        dep_hash = getattr(instance, self.dep_hash_name)

        # Compute current dependency hash
        current_hash = tuple(getattr(instance, dep, None) for dep in self.dependencies)

        # If dependency hash changed, recompute and update the cache
        if current_hash != dep_hash:
            cache = self.func(instance)
            setattr(instance, self.cache_name, cache)
            setattr(instance, self.dep_hash_name, current_hash)

        return cache

    def __set__(self, instance, value):
        """Execute func setter"""
        if self.setter_func:
            self.setter_func(instance, value)
        else:
            raise AttributeError("can't set attribute")

    def __delete__(self, instance):
        """Execute func deleter"""
        if self.deleter_func:
            self.deleter_func(instance)
        else:
            raise AttributeError("can't delete attribute")

    def setter(self, func):
        """Set ref to func setter"""
        self.setter_func = func
        return self

    def deleter(self, func):
        """Set ref to func deleter"""
        self.deleter_func = func
        return self
