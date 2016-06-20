# battery_sim

This document will show you how to run this application. 

It is recommended you run this application from a virtual environment.


Install dependencies 
-------------------------------
Prequisites:
* python 2.7
* pip, virtualenv


Install Requirements

    $ pip install -r requirements.txt

You probably need to change the permission on "/usr/local/lib/pkgconfig".

    $ sudo chmod g+wx /usr/local/lib/pkgconfig

If you run into the issue "Could not find any downloads that satisfy the requirement..." run

    $ sudo pip install --upgrade -r requirements.txt

Running the simulation
-------------------------------
To run the simulation with default load and solar data enter:
    $ python main.py run-sim

To generate plots:
    $ python main.py run-sim --plots

If you want to past in custom load and solar data: 
    $ python main.py run-sim --load_data somedatafile.csv --solar_data anotherdatafile.csv

Note there are default data files included with the application. I had some trouble parsing the original files so
the default files have been reformatted. Note that this simulation probably won't work with data of a different timescale 
or a different length. 

Running the unit tests
---------------------------------
Unit tests are run via nose:
    $ nosetests