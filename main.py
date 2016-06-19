import sys

import argparse

import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt

from controller.test import run_control
from battery_simulator import BatterySimulator
from utility_rate_generator import UtilityRateGenerator
import const


def scratch():
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

    urg = UtilityRateGenerator()
    #urg.plot_peak_periods()
    load = np.array([15] * const.HORIZON).reshape(const.HORIZON,1)

    battery_controller = BatterySimulator(max_capacity=35, max_power_output=5, acdc_eff=1, dcac_eff = 1)
    battery_controller.run(util_rate_generator=urg, load=load)

    print battery_controller.optimal_cost
    cost = battery_controller.cost_over_time(battery_controller.optimal_u.value, load, urg)


    battery_controller.plot_output(util_rate=cost, load=load, horizon=const.HORIZON)


def example_run():
    np.random.seed(1)

    T = 100
    t = np.linspace(1, T, num=T).reshape(T,1)

    price = np.exp(-np.cos((t-15)*2*np.pi/T)+0.01*np.random.randn(T,1))
    load = 2*np.exp(-0.6*np.cos((t+40)*np.pi/T) - \
        0.7*np.cos(t*4*np.pi/T)+0.01*np.random.randn(T,1))
    
    price = np.asmatrix(price)
    load = np.asmatrix(load)

    battery_controller = BatterySimulator(max_capacity=35, max_power_output=5, acdc_eff=1, dcac_eff = 1)
    battery_controller.run(util_rate=price, load=load, horizon=T)
    battery_controller.plot_output(util_rate=price, load=load, horizon=T)


def sanity_check():
    T = 10

    p = 10*np.ones([T,1])
    l = 10*np.ones([T,1])

    p = np.asmatrix(p)
    l = np.asmatrix(l)

    battery_controller = BatterySimulator(max_capacity=0, max_power_output=0, acdc_eff=1, dcac_eff = 1)
    battery_controller.run(util_rate=p, load=l, horizon=T)


def main(argv=None):

    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count',
                        help="Increase verbosity of output")
    subparsers = parser.add_subparsers(help='test subcommands')
    
    parser_web_app = subparsers.add_parser('run-sim', help="displays results in local browser")
    parser_web_app.set_defaults(cmd='run-sim')

    parser_web_app = subparsers.add_parser('sanity-check', help="runs a simplified model to illustrate simulator dynamics")
    parser_web_app.set_defaults(cmd='sanity-check')

    args = parser.parse_args(argv[1:])

    if args.cmd == "sanity-check":
        return scratch()
    elif args.cmd =="run-sim":
        return testcvxopt()
    else:
        raise NotImplementedError("Unknown command: {!r}".format(args.cmd))

       

if __name__ == "__main__":
    sys.exit(main())