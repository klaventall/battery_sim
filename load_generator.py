import csv
import numpy as np
import const
import matplotlib.pyplot as plt

def generate_load_data():
    """
    Generate the net load post solar for one week of data.
    Assuming the solar load (wH) is evenly distributed over the full hour
    """

    with open('load_data.csv', 'rU') as csvfile:
        rowreader = csv.reader(csvfile)
        next(rowreader)  # skip header row
        raw_load = [float(row[1]) for row in rowreader]

    with open('generation_data.csv', 'rU') as csvfile:
        rowreader = csv.reader(csvfile)
        next(rowreader)  # skip header row
        raw_solar_load = [float(row[1]) for row in rowreader]

    # convert the solar load to kwH and extrapolate to 15-min intervals
    solar_load = np.repeat(raw_solar_load, 4) / 1000.

    return np.array(raw_load - solar_load).reshape(const.HORIZON, 1)

def plot_load_data(load):
    T = const.HORIZON
    t = np.linspace(1, T, num=T).reshape(T,1)
   
    plt.figure(1)
    plt.plot(t/4, load, 'r', label=r"$u$");
    plt.ylabel("load (kW)")
    plt.xlabel("t")
    plt.legend()
    plt.show()
