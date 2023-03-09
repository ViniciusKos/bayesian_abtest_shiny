import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def get_prob_and_loss( data , sample_size = None):

    vals = {}
    prob_b_better_a = []
    expected_loss_a = []
    expected_loss_b = []


    for day in range( len ( data ) ):

        for v in ["a", "b"]:

            #Generate Beta distributin params
            vals[f"u_{v}"] , vals[f"var_{v}"] = stats.beta.stats( a = 1 + data.loc[day, f'acc_clicks_{v.upper()}'], \
                    b = 1 + (data.loc[day, f'acc_visits_{v.upper()}'] - data.loc[day, f'acc_clicks_{v.upper()}']), moments='mv')


            #Generate Beta distribution
            vals[f"u_{v}"], vals[f"var_{v}"] = stats.beta.stats( a = 1 + data.loc[day, f'acc_clicks_{v.upper()}'], \
                                    b = 1 + (data.loc[day, f'acc_visits_{v.upper()}'] - data.loc[day, f'acc_clicks_{v.upper()}']), moments='mv')
            
            #Generate Normal distribution
            vals[f"x_{v}"] = np.random.normal( loc = vals[f"u_{v}"], scale = 1.25*np.sqrt( vals[f"var_{v}"] ) ,size = sample_size)

            #Generate Beta PDF
            vals[f"f{v}"] = stats.beta.pdf ( vals[f"x_{v}"], 
                            a = 1 + data.loc[day, f'acc_clicks_{v.upper()}'], 
                            b = 1 + (data.loc[day, f'acc_visits_{v.upper()}'] - data.loc[day, f'acc_clicks_{v.upper()}']) )
            
            #Generate Normal PDF
            vals[f"g{v}"] = stats.norm.pdf( vals[f"x_{v}"], loc = vals[f"u_{v}"], scale = 1.25*np.sqrt( vals[f"var_{v}"] ) )


        
            # Beta / Normal
            y = ( vals['fa'] * vals['fb'] ) / ( vals['ga'] * vals['gb'] )
            yb = y[ vals['x_b'] >= vals['x_a'] ]
            
            #Calculate probabilities
            p = ( 1/ sample_size ) * np.sum(yb)


            expected_loss_A = (1 / sample_size ) * np.sum ( ( ( vals['x_b'] - vals['x_a'] )*y) [vals['x_b'] >= vals['x_a']] )
            expected_loss_B = (1 / sample_size ) * np.sum ( ( ( vals['x_a'] - vals['x_b'] )*y) [vals['x_a'] >= vals['x_b']] )

            prob_b_better_a.append(p)
            expected_loss_a.append( expected_loss_A )
            expected_loss_b.append( expected_loss_B )


    return prob_b_better_a, expected_loss_a, expected_loss_b