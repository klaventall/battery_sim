import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt

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


    def run(self, util_rate_generator, load, horizon):
        # renamaing vars for readibility
        C = self.max_capacity
        M = self.max_power_output
        T = horizon
        a = self.acdc_eff
        b = self.dcac_eff

        s = cvx.Variable(T+1)
        u = cvx.Variable(T)

        states = []
        for t in range(T):
            cost = util_rate[t] * (load[t] + b*u[t])
            constr = [s[t+1] == s[t] + a*u[t], 
                      s[t] <= C,
                      s[t] >= 0,
                      u[t] <= M,
                      u[t] >= -M,
                     load[t] + u[t]>= 0]
            states.append( cvx.Problem(cvx.Minimize(cost), constr) )
        # sums problem objectives and concatenates constraints.
        prob = sum(states)
        prob.constraints += [s[T] == 0, s[0] == 0]

        self.optimal_cost = prob.solve()
        self.optimal_s = s
        self.optimal_u = u

    def cost_function(self, u, load, urg, dcac_eff, t):
        cost = 0
        # energy rate costs
        cost += urg.energy_peak_charge * urg.peak_mat[t,t] * (load[t] + dcac_eff * u[t])
        cost += urg.energy_part_peak_charge * urg.part_peak_mat[t,t] * (load[t] + dcac_eff * u[t])
        cost += urg.energy_off_peak_charge * urg.off_peak_mat[t,t] * (load[t] + dcac_eff * u[t])
        # demand rate costs
        

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
        plt.subplot(3,1,1)
        plt.plot(ts, load, 'r');
        plt.plot(ts, self.optimal_u.value, 'b');
        plt.xlabel('t')
        plt.ylabel('load, battey power')
        plt.legend(['load', 'u(t)'])
        plt.subplot(3,1,2)
        plt.plot(ts, util_rate, 'b');
        plt.xlabel('t')
        plt.ylabel('util rate ($/kwH)')

        plt.subplot(3,1,3)
        plt.plot(ts, self.optimal_s.value[0:-1], 'b');
        plt.xlabel('t')
        plt.ylabel('kWh')
        plt.ylim((0, 40))
        plt.show()
