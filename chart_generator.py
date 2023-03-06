import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation





def bayesian_inference( data ):

    return p, expected_loss_a, expected_loss_b
    


def animate( i ):
    df0 = pd.concat( [ pd.read_csv(f"data_collected_{i}.csv") for i in ["red","blue"] ] )
    df1 = df0.copy()
    #data pivot
    for i in ['visit','click']:
        df1[i] = df1[i].astype(int)
    df1 = df1.reset_index().rename( columns={'index':'day'} )
    df1 = df1.pivot_table( index='day', columns='group', values=['click','visit'], aggfunc='sum')
    df1 = df1.swaplevel( axis=1 )
    df1 = df1.reindex(sorted(df1.columns), axis=1).fillna(0)
    df1.columns = ["_".join(i) for i in df1.columns]
    for i in df1.columns:
        df1[f"acc_{i}"] = df1[i].cumsum()

    
    # for group in ["control", "treatment"]:
    #     df_filtered = df1[df1['group']==group]
    #     df_filtered['click'] = df_filtered['click'].astype(int)
    #     df_filtered['visit'] = df_filtered['visit'].astype(int)

        x1 = np.arange( p )

        plt.plot( x1, p, label=f"Probability B better A")
        plt.plot( x1, expected_loss_a, label='Risk Choosing A')
        plt.plot( x1, expected_loss_b, label='Risk Choosing B')
        plt.legend( loc='upper left' )
        plt.tight_layout()

ani = FuncAnimation( plt.gcf(), animate, interval=1000 )

plt.tight_layout()
plt.show()