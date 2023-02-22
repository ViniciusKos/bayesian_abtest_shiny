import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

def bayesian_inference( data ):
    return p, expected_loss_a, expected_loss_b
    


def animate( i ):
    df0 = pd.concat( [ pd.read_csv(f"data_collected_{i}.csv") for i in ["red","blue"] ] )

    plt.cla()
    for group in ["control", "treatment"]:

        df_filtered = df0[df0['group']==group]
        df_filtered['click'] = df_filtered['click'].astype(int)
        df_filtered['visit'] = df_filtered['visit'].astype(int)

        x1 = np.arange( len(df_filtered) )
        y1 = df_filtered['click'].cumsum()/df_filtered['visit'].cumsum()

        plt.plot( x1, y1, label=f"{group} Group")
        plt.legend( loc='upper left' )
        plt.tight_layout()
        plt.show()

ani = FuncAnimation( plt.gcf(), animate, interval=1000 )

plt.tight_layout()
plt.show()