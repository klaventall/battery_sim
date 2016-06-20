import unittest
import battery_sim.const as const

class SimTestBase(unittest.TestCase):

    def setUp(self):
        super(SimTestBase, self).setUp()
        # set up mock constants for testing
        const.DAILY_UNITS = 4 * 24
        const.NUM_DAYS = 7
        const.HORIZON = 4 * 24 * 7

        const.PEAK_TIME_RANGE = [12., 18.]
        const.PART_PEAK_TIME_RANGE = [[8.5, 12.],[18., 21.5]]
        const.OFF_PEAK_TIME_RANGE =  [[0., 8.5], [21.5, 24.]]

        const.ENERGY_PEAK_CHARGE = 4
        const.ENERGY_PART_PEAK_CHARGE = 4
        const.ENERGY_OFF_PEAK_CHARGE = 4

        const.DEMAND_PEAK_CHARGE = 1
        const.DEMAND_PART_PEAK_CHARGE = 1
        const.DEMAND_MAX_CHARGE = 1