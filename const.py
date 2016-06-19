"""
Helper class to store global static values
"""

class const:
    class ConstError(TypeError): pass
    def __setattr__(self,name,value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind const(%s)"%name
        self.__dict__[name]=value


def set_const(const):
    const.DAILY_UNITS = 4 * 24
    const.NUM_DAYS = 7
    const.HORIZON = 4 * 24 * 7

    const.PEAK_TIME_RANGE = [12., 18.]
    const.PART_PEAK_TIME_RANGE = [[8.5, 12.],[18., 21.5]]
    const.OFF_PEAK_TIME_RANGE =  [[0., 8.5], [21.5, 24.]]

    const.ENERGY_PEAK_CHARGE = 0.14683
    const.ENERGY_PART_PEAK_CHARGE = 0.10671
    const.ENERGY_OFF_PEAK_CHARGE = 0.08014

    const.DEMAND_PEAK_CHARGE = 18.74
    const.DEMAND_PART_PEAK_CHARGE = 5.23
    const.DEMAND_MAX_CHARGE = 15.96