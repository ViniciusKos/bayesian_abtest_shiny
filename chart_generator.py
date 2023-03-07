import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from get_probs_function import get_prob_and_loss


def animate( i ):

    df = pd.concat( [ pd.read_csv(f"data_collected_{i}.csv") for i in ["red","blue"] ] )
    df1 = df.copy()
    for i in ['visit','click']:
        df1[i] = df1[i].astype(int)
    df1 = df1.reset_index().rename( columns={'index':'day'} )
    df1 = df1.pivot_table( index='day', columns='group', values=df1.select_dtypes(exclude='object').columns ,aggfunc='sum')
    df1 = df1.swaplevel( axis=1 )
    df1 = df1.reindex(sorted(df1.columns), axis=1).fillna(0)
    df1.columns = ["_".join(i) for i in df1.columns]
    for i in df1.columns:
        df1[f"acc_{i}"] = df1[i].cumsum()
    df1 = df1.rename(columns={
        'control_click':"clicks_A",
        'treatment_click':"clicks_B",
        "control_visit":"visits_A",
        "treatment_visit":"visits_B",
        "acc_control_click":"acc_clicks_A",
        "acc_treatment_click":"acc_clicks_B",
        "acc_control_visit":"acc_visits_A",
        "acc_treatment_visit":"acc_visits_B"
    })


    proba_b_better_a, expected_loss_A, expected_loss_B = get_prob_and_loss(df1, sample_size=1000)

    x1 = np.arange( len(proba_b_better_a) )
 
    plt.clf()
    plt.plot( x1, proba_b_better_a, label=f"Probability B better A", color='green')
    plt.plot( x1, expected_loss_A, label='Risk Choosing A', color='blue')
    plt.plot( x1, expected_loss_B, label='Risk Choosing B', color='red')
    plt.legend( loc='upper left' )
    plt.tight_layout()

ani = FuncAnimation( plt.gcf(), animate, interval=1000 )

plt.clf()
plt.tight_layout()
plt.show()