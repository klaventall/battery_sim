import os
import unittest
import numpy as np
import battery_sim.const as const
from battery_sim.battery_simulator import BatterySimulator
from battery_sim.utility_rate_generator import UtilityRateGenerator
from base import SimTestBase

class BatterySimulatorTest(SimTestBase):
    delta = float(10e-5)

    def setUp(self):
        super(BatterySimulatorTest, self).setUp()
        self.urg = UtilityRateGenerator()
    
    # This is the theoritical cost if there was no battery for a given load
    def expected_cost(self,load):
        return float(np.linalg.norm(np.dot(self.urg.peak_mat,load),1)/120
                        + np.linalg.norm(np.dot(self.urg.part_peak_mat,load),1)/140
                        + np.linalg.norm(np.dot(self.urg.off_peak_mat,load),1)/412
                        + np.linalg.norm(np.dot(self.urg.peak_mat,load), np.inf)
                        + np.linalg.norm(np.dot(self.urg.part_peak_mat,load), np.inf)
                        + np.linalg.norm(np.dot(self.urg.off_peak_mat,load),np.inf)
        )   

    def test_cost_function(self):
        """
        Evaluate the correctness of our objective function
        """
        battery_controller = BatterySimulator(max_capacity=0, max_power_output=0, acdc_eff=1, dcac_eff = 1)
        
        load = np.ones([const.HORIZON,1])
        u = np.zeros([const.HORIZON, 1])

        # cost metrics for enery and demand
        energy_metric = lambda x : np.linalg.norm(x,1)
        demand_metric = lambda x : np.linalg.norm(x, np.inf)

        # verify the cost function directly
        cost = battery_controller.cost_function(u, load, self.urg, energy_metric, demand_metric)
        self.assertAlmostEquals(cost, self.expected_cost(load), self.delta)
        
    def test_basic_sim(self):
        """
        Evaluate a trivial scenario with no battery and constant load
        """
        load = np.ones([const.HORIZON,1])
        # now run the simulation. Results should be the same
        battery_controller = BatterySimulator(max_capacity=0, max_power_output=0, acdc_eff=1, dcac_eff = 1)
        battery_controller.run(self.urg,load)

        print self.expected_cost(load), battery_controller.optimal_cost

        self.assertTrue( abs(self.expected_cost(load) - battery_controller.optimal_cost) <= self.delta)
    
    def test_active_battery(self):
        """
        Evaluate a trivial scenario with the battery active
        """
        load = np.ones([const.HORIZON,1])
        # add in some discount time so we can utilize the battery
        load[10:50] = 0.5
        # now run the simulation. Results should less than the upper_bound_cost
        battery_controller = BatterySimulator(max_capacity=10, max_power_output=5, acdc_eff=1, dcac_eff = 1)
        battery_controller.run(self.urg,load)

        self.assertGreaterEqual(self.expected_cost(load), battery_controller.optimal_cost)

  