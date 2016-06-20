import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt
import const

class BatterySimulator(object):
    """
    An object which can simulate control of the charge and discharge 
    of a battery such that energy costs are minimized.
    """
    def __init__(self, max_capacity=40, max_power_output=20, acdc_eff=0.95, dcac_eff=0.9, cvxmode=True):
        self.max_capacity = max_capacity
        self.max_power_output = max_power_output
        self.acdc_eff = acdc_eff
        self.dcac_eff = dcac_eff

        self.optimal_battery_u = None
        self.optimal_battery_s = None
        self.optimal_cost = None
        self.problem = None

    def run(self, util_rate_generator, load):
        """
        Given a load and a pricing scheme, computes the optimal
        charge/discharge schedule for the battery which minimizes
        total cost.
        """

        # renamaing vars for readibility
        T = const.HORIZON
        # battery constraint params
        C = self.max_capacity
        M = self.max_power_output
        # energy storage of the battery
        s = cvx.Variable(T+1)
        # power output of the battery
        u = cvx.Variable(T)
        # state matrix
        A = np.diag([1]*(T), k=-1)

        # cost metrics for enery and demand
        energy_metric = lambda x : cvx.norm(x,1)
        demand_metric = lambda x : cvx.norm(x, 'inf')

        cost = cvx.Minimize(self.cost_function(u, load , util_rate_generator, energy_metric, demand_metric))
        #cost = cvx.Minimize(.2*load.T*(load + u))
        constraints = [
            s == A*s + cvx.vstack(0, self.acdc_eff*u),
            s <= C,
            s >= 0,
            u <= M,
            u >= -M,
            u + load >=0
        ]
        # sums problem objectives and concatenates constraints.
        prob = cvx.Problem(cost, constraints)
        # add final stopping conditions on the battery
        prob.constraints += [s[T] == 0, s[0] == 0]

        optval = prob.solve()
        self.optimal_cost = optval
        self.optimal_s = s
        self.optimal_u = u
        self.problem = prob

    def cost_function(self, u, load, urg, energy_metric, demand_metric):
        cost = 0
        tot_load = load + self.dcac_eff * u
       
        # select out the load during time-of-use periods
        peak_load = self.matrix_multiply(urg.peak_mat , tot_load) 
        pt_peak_load  = self.matrix_multiply(urg.part_peak_mat , tot_load) 
        off_peak_load = self.matrix_multiply(urg.off_peak_mat , tot_load)
        all_peak_load = self.matrix_multiply(urg.all_peak_mat, tot_load)

        # This is a hack. Finding the length of the non-zero entries
        # energy rate costs
        cost += energy_metric(urg.energy_peak_charge * peak_load) / np.sum(urg.peak_mat)
        cost += energy_metric(urg.energy_part_peak_charge * pt_peak_load) / np.sum(urg.part_peak_mat)
        cost += energy_metric(urg.energy_off_peak_charge * off_peak_load) / np.sum(urg.off_peak_mat)

        # demand rate costs
        cost += demand_metric(urg.demand_peak_charge * peak_load)
        cost += demand_metric(urg.demand_part_peak_charge * pt_peak_load)
        cost += demand_metric(urg.demand_max_charge * all_peak_load)

        return cost

    def matrix_multiply(self, A, B):
        """
        helper function to select multiplacation method. 
        for some reason, cvxpy does not accept np.dot, 
        but numpy doesn't accept '*'.
        """
        cvxmode = isinstance(A, cvx.atoms.affine.add_expr.AddExpression) or isinstance(B, cvx.atoms.affine.add_expr.AddExpression)
        return A*B if cvxmode else np.dot(A, B)

    def plot_output(self, urg, load):
        T = const.HORIZON
 
        uno = np.ones([T, 1])
        peak = np.dot(urg.peak_mat, uno)
        part_peak = np.dot(urg.part_peak_mat, uno)
        off_peak = np.dot(urg.off_peak_mat, uno)


        plt.figure(1)
        ts = np.linspace(1, T, num=T).reshape(T,1)/4
        
        ax1 = plt.subplot(3,1,1)
        plt.plot(ts, load, 'b', label='load');
        plt.plot(ts, load + self.optimal_u.value, 'r', label='adj. load');
        plt.ylabel("load (kW)")
        plt.xlabel("t")
        plt.title("Load")
        #plt.axis("tight")
        ax1.legend()
        
        ax2 = plt.subplot(3,1,2)
        plt.plot(ts, self.optimal_u.value,'r.-')
        plt.plot(ts, np.zeros([T,1]), color='k', linestyle='--')
        ax2.legend()

        plt.ylabel("u (kW)")
        plt.xlabel('t')
        plt.title("Battery Schedule (control output)")
        #plt.axis("tight")

        plt.subplot(3,1,3)
        plt.plot(ts, self.optimal_s.value[0:-1], 'b')
        plt.xlabel('t')
        plt.ylabel('s (kWqH)')
        plt.title("Battery State (charge)")
        #plt.axis("tight")

        fig = plt.figure(2)
 
        # and the first axes using subplot populated with data 
        ax1 = fig.add_subplot(111)
        line1 = ax1.plot(ts, self.optimal_u.value,'r.-', label='bat. load')
        ax1.plot(ts, np.zeros([T,1]), color='k', linestyle='--')
        plt.ylabel("u (kW)")

        # now, the second axes that shares the x-axis with the ax1
        ax2 = fig.add_subplot(111, sharex=ax1, frameon=False)
        line2 = ax2.plot(ts, load, label='sys. load')
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("right")
        plt.ylabel("load (kW)")
        
        ax1.legend(line1, 'bat. load')

        lns = line1+line2
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc=0)

        plt.title("Battery Load vs. Main Load")

        # plt.figure(3)
        # c_raw = np.ndarray.cumsum(raw_cost)
        # c_opt = np.transpose(np.ndarray.cumsum(cost))
        # ax = plt.subplot(2,1,1)
        # plt.plot(ts, c_raw, 'r', label='max. cost')
        # plt.plot(ts, c_opt, 'b', label='cost');
        # plt.xlabel('t')
        # plt.ylabel('cost ($)')
        # plt.title("Cumulative Cost")
        # ax.legend(loc='lower right')
        
        # plt.subplot(2,1,2)
        # plt.plot(ts, raw_cost-cost, 'r');
        # plt.xlabel('t')
        # plt.ylabel('residulal ($)')
        # plt.title("Marginal Cost Savings Over Time")

        plt.show()
