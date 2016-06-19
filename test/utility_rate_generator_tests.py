import os
import unittest
import numpy as np
from base import SimTestBase
from battery_sim.utility_rate_generator import UtilityRateGenerator
import battery_sim.const as const

class UtilityRateGeneratorTest(SimTestBase):
    
    def setUp(self):
        super(UtilityRateGeneratorTest, self).setUp()

    def test_util_matricies(self):
        """
        Evaluate the correctness of our util matricies
        """
        urg = UtilityRateGenerator()
        load = np.ones([const.HORIZON,1])

        self.assertEquals(np.linalg.norm(np.dot(urg.peak_mat, load),1), 120)
        self.assertEquals(np.linalg.norm(np.dot(urg.part_peak_mat, load),1), 140)
        self.assertEquals(np.linalg.norm(np.dot(urg.off_peak_mat, load),1), 412)

