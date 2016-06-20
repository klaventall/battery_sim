import sys
import argparse
import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt

from battery_simulator import BatterySimulator
from utility_rate_generator import UtilityRateGenerator
from load_generator import generate_load_data, plot_load_data
import const
from const import set_const

def run_sim(plot_on=False):
    # set up global static constants
    set_const(const)
 
    urg = UtilityRateGenerator()
    #urg.plot_peak_periods()
    load = generate_load_data()

    battery_controller = BatterySimulator(max_capacity=4*40, max_power_output=20, acdc_eff=1, dcac_eff = 1)
    battery_controller.run(util_rate_generator=urg, load=load)
    print "OPT VAL: ", battery_controller.optimal_cost

    if plot_on:
        #plot_load_data(load)
        battery_controller.plot_output(urg=urg, load=load)


def example_run(plot_on=False):
    set_const(const)
    np.random.seed(1)

    T = const.HORIZON
    # generate mock data
    load = 150*np.ones([T,1])
    load = np.asmatrix(load)

    urg = UtilityRateGenerator()
    battery_controller = BatterySimulator(max_capacity=40*4, max_power_output=20, acdc_eff=1, dcac_eff = 1)
    battery_controller.run(util_rate_generator=urg, load=load)
    print "OPT VAL: ", battery_controller.optimal_cost
 
    if plot_on:
        #urg.plot_peak_periods()
        #plot_load_data(load)
        battery_controller.plot_output(urg=urg, load=load)

def main(argv=None):

    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='test subcommands')
    
    parser_sim = subparsers.add_parser('run-sim', help="displays results in local browser")
    parser_sim.set_defaults(cmd='run-sim')
    parser_sim.add_argument('--plot', action='store_true', help='Displays plots')

    parser_sanity = subparsers.add_parser('sanity-check', help="runs a simplified model to illustrate simulator dynamics")
    parser_sanity.set_defaults(cmd='sanity-check')
    parser_sanity.add_argument('--plot', action='store_true', help='Displays plots')

    args = parser.parse_args(argv[1:])

    if args.cmd == "sanity-check":
        return example_run(args.plot)
    elif args.cmd =="run-sim":
        return run_sim(args.plot)
    else:
        raise NotImplementedError("Unknown command: {!r}".format(args.cmd))

       

if __name__ == "__main__":
    sys.exit(main())