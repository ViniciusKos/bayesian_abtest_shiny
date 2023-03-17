import numpy as np
import pandas as pd
from flask import Flask, render_template, redirect, url_for


app = Flask( __name__ )

@app.route( '/home' )
def index():
    # get data

    df = pd.concat( [ pd.read_csv(f"../bayesian_abtest/data_collected_{i}.csv") for i in ["red","blue"] ] )
    df['no_click'] = df['visit'] - df['click']

    click_array = df.groupby( "group" ).sum().reset_index()[['click', 'no_click']].T.to_numpy()


    print( click_array )
    # Thompson Agent
    prob_reward = 
    

index()