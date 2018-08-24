runSimFn.py: Function which executes the simulation and returns a structure containing relevant results. Currently, its only voltage magnitude and angle, but probably we will add more signals
later on
input_data.py: Looks at the input file and harnesses the data to be used by mainFile.py
mainFile.py: Main script which runs the simulations, generates the results and tries to reconstruct the real world data. Currently, it compares real world sim with TS3ph simulation and gathers new 
events by comparing voltage magnitude data. Every time a new event is detected, TS3ph simulation is run again.

Old Files:
batch_plot_v_0922.py: File from which batch_get_v.py is derived (copied from 'CAPE-TS Simulations' project)
batch_get_v.py: Original file to get all the complex voltage info (mag and angle) under a structure with the bus number as the key
batch_get_v_fault.py: Basically tries to simulate the real world cases, where some event happens. (derived from batch_get_v.py)
batch_get_v_nodist.py: Tries to simulate TS3ph running, so no disturbance (derived from batch_get_v.py)