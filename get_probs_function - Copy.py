import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def get_prob_and_loss( data , sample_size = None):

    dic_val = {}
    proba_b_better_a = []
    expected_loss_a = []
    expected_loss_b = []


    for day in range( len ( data ) ):
        u_a , var_a = stats.beta.stats( a = 1 + data.loc[day, 'acc_clicks_A'], \
                                    b = 1 + (data.loc[day, 'acc_visits_A'] - data.loc[day, 'acc_clicks_A']), moments='mv')


        for v in ["a", "b"]:
            dic_val[f"u_{v}"], dic_val[f"var_{v}"] = stats.beta.stats( a = 1 + data.loc[day, 'acc_clicks_A'], \
                                    b = 1 + (data.loc[day, 'acc_visits_A'] - data.loc[day, 'acc_clicks_A']), moments='mv')
            dic_val[f"x_{v}"] = np.random.normal( loc = u_a, scale = 1.25*np.sqrt( var_a ) ,size = sample_size)
            dic_val[f"f{v}"] = stats.beta.pdf (  dic_val[f"x_{v}"], 
                            a = 1 + data.loc[day, 'acc_clicks_A'], 
                            b = 1 + ( data.loc[day, 'acc_visits_A'] - data.loc[day, 'acc_clicks_A']))
            dic_val[f"{v}"] = stats.norm.pdf(  dic_val[f"x_{v}"], loc = u_a, scale = 1.25*np.sqrt( var_a ))


        
        # Beta / Normal
        y = ( fa*fb ) / ( ga*gb )
        yb = y[x_b >= x_a]
        
        #Calculate probabilities
        p = ( 1/ sample_size ) * np.sum(yb)


    return proba_b_better_a, expected_loss_a, expected_loss_b