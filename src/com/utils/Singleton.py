def singleton(cls):
    instance = None

    def class_instanciation_or_not(*args, **kwargs):
        nonlocal instance
        if not instance:
            instance = cls(*args, **kwargs)
        return instance
    return class_instanciation_or_not
