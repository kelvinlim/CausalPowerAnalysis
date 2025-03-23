#! /usr/bin/env python

import math
from picause import StructuralEquationDagModel
import os

# The easiest way is to create an  instance of the StructuralEquationDagModel class, found in picause.py.
# By default, sem now contains a randomly-generated causal graph with a uniform effect size of 0.1.
#  In order to change the effect size, add the parameter beta = (the _square root_ of the desired effect size).

# default beta is 0.1
beta = math.sqrt(0.1)
seed = None
sem = StructuralEquationDagModel(num_var=15, num_edges=27, seed=seed, beta=beta)

"""
There is no guarantee that the graph generated when calling the StructuralEquationDagModel constructor meets the desired constraints, which in our simulation were that
each node would have a minimum independent random error of variance 0.1.
In this case False means that the graph meets our constraints.

sem.test_residual_overflow() 
"""
condition_violated = sem.test_residual_overflow()
print(condition_violated)

def create_single_df(effect_size=0.1, seed=None, num_vars=15, num_edges=27,
                     num_data_points=100):
    """
    create a single instance of SEM DAG model. It checks
    if the residual overflow condition is violated and if so, 
    it creates a new instance until the condition is met.
    

    Args:
        effect_size (float, optional): _description_. Defaults to 0.1.
        seed (_type_, optional): _description_. Defaults to None.
        num_vars (_type_, optional): _description_. Defaults to 15.
        num_edges (_type_, optional): _description_. Defaults to 27.
        num_data_points (_type_, optional): _description_. Defaults to 100.

    Returns:
        sem: the SEM
        count: the number of iterations needed
    """
    count = 1
    
    sem = StructuralEquationDagModel(num_var=num_vars, 
                                    num_edges=num_edges, 
                                    seed=seed, 
                                    beta=beta)
    # check if the residual overflow condition is violated - want False
    condition_violated = sem.test_residual_overflow()

    # loop until condition_violated is False
    while condition_violated:
        sem = StructuralEquationDagModel(num_var=num_vars, 
                                         num_edges=num_edges, 
                                         seed=seed, 
                                         beta=beta)
        condition_violated = sem.test_residual_overflow()
        count += 1
        
    # create the dataset 
    df = sem.generate_data(num_data_points)
    return df, sem, count


# df, sem, count = create_single_df()
# print(count)

data_dir = 'sim_data/'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

num_data_points = 100
num_iterations = 100
num_vars = 15
num_edges = 27

# try with different number of data points
for num_data_points in [30, 40, 60, 80, 100, 200]:
    # try with a different effect sizes
    for effect_size in [0.1, 0.3, 0.5, 0.7, 0.9]:
        for iter in range(num_iterations):
            df, sem, count = create_single_df(effect_size=effect_size,
                                    num_data_points=num_data_points)
            # print(f"effect_size: {effect_size} count: {count}")
            
            # create the filename based es and iteration
            filename = f"rows-{num_data_points}_vars-{num_vars}_edges-{num_edges}_es-{effect_size}_iter-{iter:03d}.csv"
            
            # save the df to a csv file
            path = os.path.join(data_dir, filename)
            df.to_csv(path, index=False)
            
            print(f"{filename} count: {count}")
            pass