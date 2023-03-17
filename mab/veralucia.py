
import numpy as np
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request



df = pd.read_csv(f"data_experiment.csv")
df['no_click'] = df['visit'] - df['click']

click_array = df.groupby( "group" ).sum().reset_index()[['click', 'no_click']].T.to_numpy()
print( click_array )
