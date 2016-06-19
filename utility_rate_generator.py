import numpy as np
import matplotlib.pyplot as plt
from numpy import matlib 
from scipy.linalg import block_diag

class UtilityRateGenerator(object):
    """
    Generates an object which describes utility charges for 
    every 15-min interval for a week
    """
    # number of quarter-hours in a day
    N = 4 * 24
    PEAK_TIME_RANGE = [12., 18.]
    PART_PEAK_TIME_RANGE = [[8.5, 12.],[18., 21.5]]
    OFF_PEAK_TIME_RANGE =  [[0., 8.5], [21.5, 24.]]

    ENERGY_PEAK_CHARGE = 0.14683
    ENERGY_PART_PEAK_CHARGE = 0.10671
    ENERGY_OFF_PEAK_CHARGE = 0.08014

    DEMAND_PEAK_CHARGE = 18.74
    DEMAND_PART_PEAK_CHARGE = 5.23
    DEMAND_MAX_CHARGE = 15.96


    def __init__(self):
        # energy and demand charges
        self.energy_peak_charge = ENERGY_PEAK_CHARGE 
        self.energy_part_peak_charge = ENERGY_PART_PEAK_CHARGE 
        self.energy_off_peak_charge = ENERGY_OFF_PEAK_CHARGE 

        self.demand_peak_charge = DEMAND_PEAK_CHARGE 
        self.demand_part_peak_charge = DEMAND_PART_PEAK_CHARGE 
        self.demand_max_charge = DEMAND_MAX_CHARGE 

        # N x N matricies which select quarter-hours in peak, part-peak and off-peak
        self.peak_mat = None
        self.part_peak_mat= None
        self.off_peak_mat = None
        self.all_peak_mat = None
        # populate the matricies
        self.generate_time_of_use_periods()

    def generate_time_of_use_periods(self):
        """
        time of use periods will be described by NxM indicator matricies

        """
        quarters = self.generate_quarter_hours()
        
        peak_indicator = [1 if ( (t >= self.PEAK_TIME_RANGE[0]) & (t < self.PEAK_TIME_RANGE[1])) else 0 for t in quarters]

        part_peak_indicator = [1 if ( (t >= self.PART_PEAK_TIME_RANGE[0][0]) and (t < self.PART_PEAK_TIME_RANGE[0][1])
                                        or t >= self.PART_PEAK_TIME_RANGE[1][0]) and (t < self.PART_PEAK_TIME_RANGE[1][1]) else 0 for t in quarters]

        off_peak_indicator = [1 if ( (t >= self.OFF_PEAK_TIME_RANGE[0][0]) and (t < self.OFF_PEAK_TIME_RANGE[0][1])
                                        or t >= self.OFF_PEAK_TIME_RANGE[1][0]) and (t < self.OFF_PEAK_TIME_RANGE[1][1]) else 0 for t in quarters]

        peak_day = np.diag(peak_indicator)
        part_peak = np.diag(part_peak_indicator)
        off_peak_weekday = np.diag(off_peak_indicator) 

        off_peak_weekend_off = np.zeros([self.N,self.N]) # used for peak, part_peak
        off_peak_weekend_on  = np.diag([1]*self.N) # used for off_peak

        # each of these will block_diag 5 week day indicators and 2 weekend indicators
        self.peak_mat= block_diag(peak_day, peak_day, peak_day, peak_day, peak_day,
                                        off_peak_weekend_off, off_peak_weekend_off)
        self.part_peak_mat= block_diag(part_peak, part_peak, part_peak, part_peak, part_peak,
                                        off_peak_weekend_off,off_peak_weekend_off)
        self.off_peak_mat = block_diag(off_peak_weekday, off_peak_weekday, off_peak_weekday, off_peak_weekday, off_peak_weekday,
                                        off_peak_weekend_on, off_peak_weekend_on)

    def generate_quarter_hours(self):
        # generate a day's worth of of quarter-hours
        hour = 0
        quarters = [0] * self.N
        for idx in range(1, self.N):
            quarters[idx] = quarters[idx-1] + 0.25

        return quarters

    def plot_peak_periods(self):
        quarters = self.generate_quarter_hours()
        u = np.ones([self.N * 7, 1])

        peak = np.dot(self.peak_mat, u)
        part_peak = np.dot(self.part_peak_mat, u)
        off_peak = np.dot(self.off_peak_mat, u)


        plt.figure(1)
        x = range(len(u))
        plt.subplot(3,2,1)
        plt.plot(x, peak)
        plt.title("peak hours")
        plt.ylim((-0.1, 1.1))

        plt.subplot(3,2,2)
        plt.plot(quarters, peak[0:len(quarters)])
        plt.title("daily peak")
        plt.ylim((-0.1, 1.1))

        plt.subplot(3,2,3)
        plt.plot(x, part_peak)
        plt.title("part-peak hours")
        plt.ylim((-0.1, 1.1))

        plt.subplot(3,2,4)
        plt.plot(quarters, part_peak[0:len(quarters)])
        plt.title("daily part-peak")
        plt.ylim((-0.1, 1.1))

        plt.subplot(3,2,5)
        plt.plot(x, off_peak)
        plt.title("off-peak hours")
        plt.ylim((-0.1, 1.1))

        plt.subplot(3,2,6)
        plt.plot(quarters, off_peak[0:len(quarters)])
        plt.title("daily off-peak (week)")
        plt.ylim((-0.1, 1.1)) 
        
        plt.show()




