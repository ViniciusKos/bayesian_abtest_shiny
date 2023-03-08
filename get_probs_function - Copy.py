import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def get_prob_and_loss( data , sample_size = None):

    vals = {}
    proba_b_better_a = []
    expected_loss_a = []
    expected_loss_b = []


    for day in range( len ( data ) ):
        u_a , var_a = stats.beta.stats( a = 1 + data.loc[day, 'acc_clicks_A'], \
                                    b = 1 + (data.loc[day, 'acc_visits_A'] - data.loc[day, 'acc_clicks_A']), moments='mv')


        for v in ["a", "b"]:

            #Generate Beta distribution
            vals[f"u_{v}"], vals[f"var_{v}"] = stats.beta.stats( a = 1 + data.loc[day, 'acc_clicks_A'], \
                                    b = 1 + (data.loc[day, 'acc_visits_A'] - data.loc[day, 'acc_clicks_A']), moments='mv')
            
            #Generate Normal distribution
            vals[f"x_{v}"] = np.random.normal( loc = u_a, scale = 1.25*np.sqrt( var_a ) ,size = sample_size)

            #Generate Beta PDF
            vals[f"f{v}"] = stats.beta.pdf (  vals[f"x_{v}"], 
                            a = 1 + data.loc[day, 'acc_clicks_A'], 
                            b = 1 + ( data.loc[day, 'acc_visits_A'] - data.loc[day, 'acc_clicks_A']))
            
            #Generate Normal PDF
            vals[f"g{v}"] = stats.norm.pdf(  vals[f"x_{v}"], loc = u_a, scale = 1.25*np.sqrt( var_a ))


        
        # Beta / Normal
        y = ( vals['fa'] * vals['fb'] ) / ( vals['ga'] * vals['gb'] )
        yb = y[ vals['x_b'] >= vals['x_a']]
        
        #Calculate probabilities
        prob_b_better_a = ( 1/ sample_size ) * np.sum(yb)


    return prob_b_better_a, expected_loss_a, expected_loss_b