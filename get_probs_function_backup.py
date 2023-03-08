import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def get_prob_and_loss( data , sample_size = None):

    proba_b_better_a = []
    expected_loss_a = []
    expected_loss_b = []



    for day in range( len ( data ) ):
        u_a , var_a = stats.beta.stats( a = 1 + data.loc[day, 'acc_clicks_A'], \
                                    b = 1 + (data.loc[day, 'acc_visits_A'] - data.loc[day, 'acc_clicks_A']), moments='mv')
        u_b , var_b = stats.beta.stats( a = 1 + data.loc[day, 'acc_clicks_B'], \
                                    b = 1 + (data.loc[day, 'acc_visits_B'] - data.loc[day, 'acc_clicks_B']), moments='mv')


        # Normal distribution Sample A and B
        x_a = np.random.normal( loc = u_a, scale = 1.25*np.sqrt( var_a ) ,size = sample_size)
        x_b = np.random.normal( loc = u_b, scale = 1.25*np.sqrt( var_b ) ,size = sample_size)


        # Norm distribution function of page A nad page B
        fa = stats.beta.pdf ( x_a, 
                            a = 1 + data.loc[day, 'acc_clicks_A'], 
                            b = 1 + ( data.loc[day, 'acc_visits_A'] - data.loc[day, 'acc_clicks_A']))

        fb = stats.beta.pdf ( x_b,
                            a = 1 + data.loc[day, 'acc_clicks_B'],
                            b = 1 + ( data.loc[day, 'acc_visits_B'] - data.loc[day, 'acc_clicks_B'] ))
        

        # Beta distribution function of page A and B
        ga = stats.norm.pdf( x_a, loc = u_a, scale = 1.25*np.sqrt( var_a ))
        gb = stats.norm.pdf( x_b, loc = u_b, scale = 1.25*np.sqrt( var_b ))
        

        # Beta / Normal
        y = ( fa*fb ) / ( ga*gb )
        yb = y[x_b >= x_a]
        
        #Calculate probabilities
        p = ( 1/ sample_size ) * np.sum(yb)

        expected_loss_A = (1 / sample_size ) * np.sum ( ( ( x_b - x_a )*y) [x_b >= x_a] )
        expected_loss_B = (1 / sample_size ) * np.sum ( ( ( x_a - x_b )*y) [x_a >= x_b] )

        proba_b_better_a.append(p)
        expected_loss_a.append( expected_loss_A )
        expected_loss_b.append( expected_loss_B )

    return proba_b_better_a, expected_loss_a, expected_loss_b