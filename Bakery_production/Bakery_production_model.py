# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 14:42:23 2017

@author: JRGene
"""

import pandas as pd
import numpy as np
# import seaborn as sns


def ChangeSchedule():
    """
    To ask to the user if s/he wants to change the production schedule.
    """
    question = input("Do you want to change the schedule? (Y/N) ")
    if question == "Y" or question == "y":
        return True
    return False
        
def AskHourToChange(schedule):
    """
    To ask to the hour to be change and shows the current production schedule.
    """
    hour = int(input("Introduce an hour (0-23) to change: "))
    schedule[hour] = not(schedule[hour])
    print("Current schedule:\n{}".format(pd.DataFrame(schedule).T))
    return schedule
    
def DefineProductionSchedule(schedule=[0,0,0,0,0,0,1,1,1,1,1,1,
                                       1,1,1,1,1,1,1,0,0,0,0,0]):
    """
    To define the production schedule, which has a value by default. It first
    prints the current schedule and then asks if you want to change it, using
    the function 'AskHourToChange'.
    """
    schedule = pd.Series(schedule)
    print("Current schedule:\n{}".format(pd.DataFrame(schedule).T))
    while ChangeSchedule():
        schedule = AskHourToChange(schedule)
    return schedule
        
def DefineBakeryOpenHours(schedule=[0,0,0,0,0,0,0,1,1,1,1,1,
                                    1,1,1,1,1,1,1,1,1,0,0,0]):
    """
    To define the bakery open schedule, which has a value by default. It first
    prints the current schedule and then asks if you want to change it, using
    the function 'AskHourToChange'.
    """
    schedule = pd.Series(schedule)
    print("Current schedule:\n{}".format(pd.DataFrame(schedule).T))
    while ChangeSchedule():
        schedule = AskHourToChange(schedule)
    return schedule

def RandomArray():
    """
    It creates a pandas series composed of 3 blocks, which defines-models the 
    behaviour of the daily demand.
    """
    a = pd.Series(np.random.rand(5))
    b = pd.Series(np.random.randn(12)).abs()
    c = pd.Series(np.random.rand(7))
    frames = [a, b, c]
    random_array = pd.Series(list(pd.concat(frames)))
    return random_array

def ReturnCloseHour(bakery_schedule):
    """
    Returns the closing hour of the bakery.
    """
    aux = pd.Series(list(bakery_schedule)[::-1])
    index = aux[aux == 1].index[0]
    return (len(aux)- index)


def SimulationBlock(production_schedule, bakery_schedule, production_rate, 
                    weighted_hour_demand, buffer_size, cycle_time=30, 
                    MC_iterations=100):
    """
    This is an Activity-flow
    """
    production_per_hour = pd.Series(production_schedule) * production_rate
    close_hour = ReturnCloseHour(bakery_schedule)
    
    m_avg_units_lost = pd.DataFrame()
    m_avg_sales_lost = pd.DataFrame()
    m_avg_stock_position = pd.DataFrame()
    m_avg_demand_units = pd.DataFrame()
    
# this is Monte_Carlo, that uses the law of big numbers    
    for i in range(MC_iterations):
# this is like the time step of the clock in Simulink
# what means that inside of it all the blocks are created, since each
# time step the outcome of a previous task influences the input of his
# posterior. like a Markow Chain.
        monthly_units_lost = pd.DataFrame()
        monthly_sales_lost = pd.DataFrame()
        monthly_stock_position = pd.DataFrame()
        monthly_demand_units = pd.DataFrame()
    
        for j in range(cycle_time):
            daily_demand = np.round(RandomArray() * weighted_hour_demand 
                                    * bakery_schedule)
            Buffer = []
            daily_lost_units = []
            daily_lost_sales = []
            stock_position = []
# How is going the connection output input in terms of lattency
# Obviously inside the hours should be implemented
            for hour in range(24):
                hour_lost_units = 0
                hour_lost_sales = 0
                
# This block represents the consumption of bread from the buffer
                for c in range(int(daily_demand[hour])):
                    if len(Buffer) == 0:
                        hour_lost_sales += 1
                    else:
                        Buffer.pop()
                
# This block represents the production of bread, we are filling the buffer
                for p in range(int(production_per_hour[hour])):
                    bread = 1
                    Buffer.append(bread)
                while len(Buffer) > buffer_size:
                    Buffer.pop()
                    hour_lost_units += 1
                    
# This block represents the remove of all bread inventory when the bakery close
                if hour == close_hour:
                    hour_lost_units += len(Buffer)
                    Buffer = []
                    
# This block is fulfilling the hourly metrics of each day
                daily_lost_units.append(hour_lost_units)
                daily_lost_sales.append(hour_lost_sales)
                stock_position.append(len(Buffer))
                
# This block is recording the daily results per the month
            monthly_units_lost[str(j)] = daily_lost_units
            monthly_sales_lost[str(j)] = daily_lost_sales
            monthly_stock_position[str(j)] = stock_position
            monthly_demand_units[str(j)] = daily_demand        

# This block is recording the average monthly results
        m_avg_units_lost[str(i)] = monthly_units_lost.mean(numeric_only=True, axis=1)
        m_avg_sales_lost[str(i)] = monthly_sales_lost.mean(numeric_only=True, axis=1)
        m_avg_stock_position[str(i)] = monthly_stock_position.mean(numeric_only=True, axis=1)
        m_avg_demand_units[str(i)] = monthly_demand_units.mean(numeric_only=True, axis=1)

# MonteCarlo approximation (using the law of big numbers)
    avg_units_lost = m_avg_units_lost.mean(numeric_only=True, axis=1)
    avg_sales_lost = m_avg_sales_lost.mean(numeric_only=True, axis=1)
    avg_stock_position = m_avg_stock_position.mean(numeric_only=True, axis=1)
    avg_demand_units = m_avg_demand_units.mean(numeric_only=True, axis=1)
    return pd.DataFrame([avg_units_lost, avg_sales_lost, avg_stock_position,
                         avg_demand_units], index=['Units_lost', 'Sales_lost', 
                                         'Stock_position', 'Demand_units'])

if __name__ == "__main__":
    production_schedule = [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0]
    bakery_schedule = [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0]
    production_rate = 10
    weighted_hour_demand = [1,0,0,0,0,0,0,1,6,6,8,14,11,
                            12,20,14,12,7,14,12,10,6,4,2]
    buffer_size = 50
    result = SimulationBlock(production_schedule, bakery_schedule, production_rate, 
                        weighted_hour_demand, buffer_size)
    df = result.T
    print(df)
    df_sum = df.sum(numeric_only=True, axis=0)
    print('\n'+ str(df_sum))
    df.plot()
 