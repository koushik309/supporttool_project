class TargetFactory:
    _drivers = []

    @classmethod
    def reg_driver(cls, driver_cls):
        cls._drivers.append(driver_cls)
        return driver_cls

target_factory = TargetFactory
