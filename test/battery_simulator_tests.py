import os
import unittest
import numpy as np
import battery_sim.const as const
from battery_sim.battery_simulator import BatterySimulator
from battery_sim.utility_rate_generator import UtilityRateGenerator

class BatterySimulatorTest(unittest.TestCase):
    delta = float(10e-5)

    def setUp(self):
        super(BatterySimulatorTest, self).setUp()

        const.DAILY_UNITS = 4 * 24
        const.NUM_DAYS = 7
        const.HORIZON = 4 * 24 * 7

        const.PEAK_TIME_RANGE = [12., 18.]
        const.PART_PEAK_TIME_RANGE = [[8.5, 12.],[18., 21.5]]
        const.OFF_PEAK_TIME_RANGE =  [[0., 8.5], [21.5, 24.]]

        const.ENERGY_PEAK_CHARGE = 1
        const.ENERGY_PART_PEAK_CHARGE = 1
        const.ENERGY_OFF_PEAK_CHARGE = 1

        const.DEMAND_PEAK_CHARGE = 1
        const.DEMAND_PART_PEAK_CHARGE = 1
        const.DEMAND_MAX_CHARGE = 1

    def test_cost_function(self):
        """
        Evaluate the correctness of our objective function
        """
        battery_controller = BatterySimulator(max_capacity=0, max_power_output=0, acdc_eff=1, dcac_eff = 1, cvxmode=False)
        
        urg = UtilityRateGenerator()
        load = np.ones([const.HORIZON,1])
        u = np.zeros([const.HORIZON, 1])

        # shoule be 675 (672 + 3)
        expected_cost = float(np.linalg.norm(np.dot(urg.peak_mat,load),1)
                        + np.linalg.norm(np.dot(urg.part_peak_mat,load),1)
                        + np.linalg.norm(np.dot(urg.off_peak_mat,load),1)
                        + np.linalg.norm(np.dot(urg.peak_mat,load), np.inf)
                        + np.linalg.norm(np.dot(urg.part_peak_mat,load), np.inf)
                        + np.linalg.norm(np.dot(urg.off_peak_mat,load),np.inf)
                        )
        # cost metrics for enery and demand
        energy_metric = lambda x : np.linalg.norm(x,1)
        demand_metric = lambda x : np.linalg.norm(x, np.inf)

        # verify the cost function directly
        cost = battery_controller.cost_function(u, load, urg, energy_metric, demand_metric)
        self.assertAlmostEquals(cost, expected_cost, self.delta)
        
    def test_basic_sim(self):
        """
        Evaluate a trivial scenario with no battery and constant load
        """

        urg = UtilityRateGenerator()
        load = np.ones([const.HORIZON,1])

        # shoule be 675 (672 + 3)
        expected_cost = float(np.linalg.norm(np.dot(urg.peak_mat,load),1)
                        + np.linalg.norm(np.dot(urg.part_peak_mat,load),1)
                        + np.linalg.norm(np.dot(urg.off_peak_mat,load),1)
                        + np.linalg.norm(np.dot(urg.peak_mat,load), np.inf)
                        + np.linalg.norm(np.dot(urg.part_peak_mat,load), np.inf)
                        + np.linalg.norm(np.dot(urg.off_peak_mat,load),np.inf)
        )

    # now run the simulation. Results should be the same
        battery_controller = BatterySimulator(max_capacity=0, max_power_output=0, acdc_eff=1, dcac_eff = 1, cvxmode=True)
        battery_controller.run(urg,load)
        self.assertTrue( abs(expected_cost - battery_controller.optimal_cost) <= self.delta)
    
    def test_active_battery(self):
        """
        Evaluate a trivial scenario with the battery active
        """

        urg = UtilityRateGenerator()
        load = np.ones([const.HORIZON,1])
        # add in some discount time so we can utilize the battery
        load[10:50] = 0.5

        # This is the theoritical cost if there was no battery
        upper_bound_cost = float(np.linalg.norm(np.dot(urg.peak_mat,load),1)
                        + np.linalg.norm(np.dot(urg.part_peak_mat,load),1)
                        + np.linalg.norm(np.dot(urg.off_peak_mat,load),1)
                        + np.linalg.norm(np.dot(urg.peak_mat,load), np.inf)
                        + np.linalg.norm(np.dot(urg.part_peak_mat,load), np.inf)
                        + np.linalg.norm(np.dot(urg.off_peak_mat,load),np.inf)
        )

        # now run the simulation. Results should less than the upper_bound_cost
        battery_controller = BatterySimulator(max_capacity=10, max_power_output=5, acdc_eff=1, dcac_eff = 1, cvxmode=True)
        battery_controller.run(urg,load)

        self.assertGreaterEqual( battery_controller.optimal_cost, upper_bound_cost)

        print battery_controller.problem.constraints

        self.assertTrue(False)

