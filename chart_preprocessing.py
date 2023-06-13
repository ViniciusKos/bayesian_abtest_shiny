import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from get_probs_function import get_prob_and_loss


df = pd.read_csv("data_experiment.csv")
df1 = df.copy()
df1['group'] = df1['group'].replace( {"treatment":"test"})
for i in ['visits','clicks']:
    df1[i] = df1[i].astype(int)
df1 = df1.reset_index().rename( columns={'index':'day'} )
df1 = df1.pivot_table( index='day', columns='group', values=df1.select_dtypes(exclude='object').columns ,aggfunc='sum')
df1 = df1.swaplevel( axis=1 )
df1 = df1.reindex(sorted(df1.columns), axis=1).fillna(0)
df1.columns = ["_".join(i) for i in df1.columns]
for i in df1.columns:
    df1[f"acc_{i}"] = df1[i].cumsum()

proba_b_better_a, expected_loss_A, expected_loss_B = get_prob_and_loss(df1, sample_size=1000)

x1 = np.arange( len(proba_b_better_a) )

df2 = pd.DataFrame( list(zip(x1, proba_b_better_a, expected_loss_A, expected_loss_B)), columns = ["x1", "proba_b_better_a", "expected_loss_A", "expected_loss_B"])
df2.to_csv("data_experiment_probas.csv", index=False)