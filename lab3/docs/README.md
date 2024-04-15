A quick presentation of how the code works :


1. Every important parameter relative to the movement are in param.py

2. In the main, there are 5 main steps
   1. Create the sensors with given the noise models (in param.py)
   2. Generate measurements from sensors
   3. Create the simulation cases with the measurements
   4. Generate the trajectories with the simulation cases and an order of integration
   5. Plot the results

3. About the measurements and the sensors:
   1. For each of them there is a class, and a collection class. 
   2. The collection class allows to manipulate a group of sensors/measurements all at once