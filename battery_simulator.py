import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt
import const

class BatterySimulator(object):
    """
    An object which can simulate control of the charge and discharge 
    of a battery such that energy costs are minimized.
    """
    def __init__(self, max_capacity=40, max_power_output=20, acdc_eff=0.95, dcac_eff=0.9):
        self.max_capacity = max_capacity
        self.max_power_output = max_power_output
        self.acdc_eff = acdc_eff
        self.dcac_eff = dcac_eff

        self.optimal_battery_u = None
        self.optimal_battery_s = None
        self.optimal_cost = None


    def run(self, util_rate_generator, load):
        # renamaing vars for readibility
        T = const.HORIZON
        # battery params
        C = self.max_capacity
        M = self.max_power_output
        acdc_eff = self.acdc_eff
        dcac_eff = self.dcac_eff
        # energy storage of the battery
        s = cvx.Variable(T+1)
        # power output of the battery
        u = cvx.Variable(T)
        # state matrix
        A = np.diag([1]*(T), k=-1)

        cost = cvx.Minimize(self.cost_function(u,load,util_rate_generator,dcac_eff))
        #cost = cvx.Minimize(.2*load.T*(load + u))
        constraints = [
            s == A*s + cvx.vstack(0, acdc_eff*u),
            s <= C,
            s >= 0,
            u <= M,
            u >= -M,
            u + load >=0
        ]
        # sums problem objectives and concatenates constraints.
        prob = cvx.Problem(cost, constraints)

        prob.constraints += [s[T] == 0, s[0] == 0]

        optval = prob.solve()
        self.optimal_cost = optval
        self.optimal_s = s
        self.optimal_u = u

    def cost_function(self, u, load, urg, dcac_eff):
        cost = 0
        tot_load = load + self.dcac_eff * u
        # energy rate costs
        cost += cvx.sum_entries(urg.energy_peak_charge * urg.peak_mat * tot_load)
        cost += cvx.sum_entries(urg.energy_part_peak_charge * urg.part_peak_mat * tot_load)
        cost += cvx.sum_entries(urg.energy_off_peak_charge * urg.off_peak_mat * tot_load)
        # demand rate costs
        cost += cvx.max_entries(urg.demand_peak_charge * urg.peak_mat * tot_load)
        cost += cvx.max_entries(urg.demand_part_peak_charge * urg.part_peak_mat * tot_load)
        cost += cvx.max_entries(urg.demand_max_charge * urg.all_peak_mat * tot_load)

        return cost

    def cost_over_time(self, u, load, urg):
        cost = np.zeros([const.HORIZON,1])
        uno = np.ones([const.HORIZON,1])
        # energy rate costs
        tot_load = load + self.dcac_eff * u
        cost += urg.energy_peak_charge * np.dot(urg.peak_mat, tot_load)
        cost += urg.energy_part_peak_charge * np.dot(urg.part_peak_mat, tot_load)
        cost += urg.energy_off_peak_charge  * np.dot(urg.off_peak_mat, tot_load)
        # demand rate costs
        cost += np.amax(urg.demand_peak_charge * np.dot(urg.peak_mat, tot_load)) * uno
        cost += np.amax(urg.demand_part_peak_charge * np.dot(urg.peak_mat, tot_load)) * uno
        cost += np.amax(urg.demand_max_charge * np.dot(urg.peak_mat, tot_load)) * uno

        return cost

    def plot_output(self,util_rate, load, horizon):

        T = horizon
        # plt.figure(1)
        # t = np.linspace(1, T, num=T).reshape(T,1)
        # plt.plot(t/4, util_rate, 'g', label=r"$p$");
        # plt.plot(t/4, load, 'r', label=r"$u$");
        
        # plt.ylabel("$")
        # plt.xlabel("t")
        # plt.legend()
        # plt.show()

        plt.figure(1)
        ts = np.linspace(1, T, num=T).reshape(T,1)/4
        
        plt.subplot(4,1,1)
        plt.plot(ts, self.optimal_u.value, 'r');
        plt.plot(ts, 0*np.ones([T,1]), color='b', linestyle='--')
        plt.xlabel('t')
        plt.ylabel('u(t)')
        
        plt.subplot(4,1,2)
        plt.plot(ts, util_rate, 'b');
        plt.xlabel('t')
        plt.ylabel('cost')
        
        plt.subplot(4,1,3)
        plt.plot(ts, load, 'r');
        plt.xlabel('t')
        plt.ylabel('load')

        plt.subplot(4,1,4)
        plt.plot(ts, self.optimal_s.value[0:-1], 'b');
        plt.xlabel('t')
        plt.ylabel('kWh')
        plt.ylim((0, 40))
        plt.show()
