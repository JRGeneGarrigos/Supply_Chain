Bakery_production_schedule_model
=================================
(Author JRGene)

Here is a production schedule model of a bakery. The bakery produces its own 
bread in situ, trying to cover the demand while minimizing the rest of costs.

The aim of the model consist of adjusting schedule production parameters as 
the hours of production and hours open, in order to get the best possible
results.

Each time you run the code, it plots a graph and prints the KPIs of the system
so that you can adjust schedule parameters manually in order to improve the
performance of the system.




Output parameters:
------------------
- units lost: hourly and daily. Related with exceed the buffer size.
- Sales lost: hourly and daily. When demand can no be covered.
- Stock position: hourly and daily. Number of units in the buffer.
- Demand Units: hourly and daily units of bread demanded. (1 customer = 1 bread)

Input parameters:
-----------------
Here is the declaration of the 'SimulationBlock' function. Which has (7) seven
parameters. 
def SimulationBlock(production_schedule, bakery_schedule, production_rate, 
                    weighted_hour_demand, buffer_size, cycle_time=30, 
                    MC_iterations=100)
The first (5) five are model specifications. 
The last (2) are 'cycle_time' (by default 30 days) and 'MC_iterations', that
is the number of Monte Carlo in order to get long term picture of the 
behavior of the model specified in long term (law of large/big numbers).

Model specifications:
---------------------

You can define the production schedule 'production_schedule' and the hours 
that the bakery is open named as 'bakery_schedule'. Example: 
From 7:00 to 19:00 the bakery is producing bread:
production_schedule = [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0]
From 7:00 to 21:00 the bakery is open to the public:
    bakery_schedule = [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0]
	
You can define the mean number of visits that receives per day the bakery.
Example: we have an average of 20 from 14:00 to 15:00
weighted_hour_demand = [1,0,0,0,0,0,0,1,6,6,8,14,11,
						12,20,14,12,7,14,12,10,6,4,2]
						
Define the production rate of bread of the bakery, for instance
a production_rate = 10, means that the bakery produces 10 breads an hour.

Define the 'buffer_size' the max number of bread that you can hold. What means
that if you produce an extra unit while the 'buffer_size' = 50 units and
there is no demand, the 'sales_lost' counter increases by 1.


Next steps:
------------
1. Establish cost of lost sales, sale price, cost of unit lost and cost of 
   shop open. In order to be able to adjust the optimal value in $.
2. Make a Markov system of two stages in series.
3. Implement strategies, periodic or continuous replenishment systems.
4. Over the simulation create a optimization, in order to find the optimum.


Installation:
-------------

This script has been tested with Python 3.6

Required modules include:

- numpy
- pandas