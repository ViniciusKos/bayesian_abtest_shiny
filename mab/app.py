import numpy as np
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request


app = Flask( __name__ )

prob_reward=None

@app.route( '/home' )
def index():

    df = pd.read_csv(f"data_experiment.csv")
    df['no_click'] = df['visit'] - df['click']
    alpha = df.groupby( "group" )[['click', 'no_click']].sum()

    print( alpha )


    # Thompson Agent
    prob_reward = np.random.beta( alpha['click'], alpha['no_click'] )

    if np.argmax( prob_reward ) == 0:
        return render_template( "page_red.html" )
    else:
        return render_template( "page_blue.html" )


@app.route( "/yes", methods=['POST'] )
def yes_event():
    df0 = pd.read_csv("data_experiment.csv" )
    if np.argmax( prob_reward ) == 0:
        new_row = {"click":1, "visit":1, "group":"control"}
        df0 = df0.append( new_row, ignore_index=True )
    else:
        new_row = {"click":1, "visit":1, "group":"treatment"}
        df0 = df0.append( new_row, ignore_index=True )

    df0.to_csv( "data_experiment.csv", index=False)
    return redirect( url_for( "index" ))



@app.route( "/no", methods=['POST'] )
def no_event():
    df0 = pd.read_csv(f"data_experiment.csv")
    print(request.form )
    if np.argmax( prob_reward ) == 0:
        new_row = {"click":0, "visit":1, "group":"control"}
        df0 = df0.append( new_row, ignore_index=True )
    else:
        new_row = {"click":0, "visit":1, "group":"treatment"}
        df0 = df0.append( new_row, ignore_index=True )

    df0.to_csv( "data_experiment.csv", index=False)
    return redirect( url_for( "index" ))



if __name__ == '__main__':
    app.run( port=5000, debug=True)