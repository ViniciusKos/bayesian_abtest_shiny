import numpy as np
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request


app = Flask( __name__ )

prob_reward = None
df = pd.read_csv(f"data_experiment.csv")

@app.route( '/home' )
def index():

    global prob_reward, df
    df = pd.read_csv(f"data_experiment.csv")

    df['no_clicks'] = df['visits'] - df['clicks']
    alpha = df.groupby( "group" )[['clicks', 'no_clicks']].sum()
    print( alpha )

    # Thompson Agent - Draw random beta sample from pages conversion
    prob_reward = np.random.beta( alpha['clicks'], alpha['no_clicks'] )

    # check which page has the highest conversion and return it
    if np.argmax( prob_reward ) == 0:
        return render_template( "page_red.html" )
    else:
        return render_template( "page_blue.html" )


@app.route( "/yes", methods=['POST'] )
def yes_event():

    global prob_reward, df

    # check which page has the highest conversion and create new row
    if np.argmax( prob_reward ) == 0:
        new_row = {"clicks":1, "visits":1, "group":"control"}
    else:
        new_row = {"clicks":1, "visits":1, "group":"treatment"} 

    #append and save data
    df = df.append( new_row, ignore_index=True )
    df.to_csv( "data_experiment.csv", index=False)
    return redirect( url_for( "index" ))


@app.route( "/no", methods=['POST'] )
def no_event():

    global prob_reward, df

    # check which page has the highest conversion and create new row
    if np.argmax( prob_reward ) == 0:
        new_row = {"clicks":0, "visits":1, "group":"control"}
    else:
        new_row = {"clicks":0, "visits":1, "group":"treatment"}

    #append and save data
    df = df.append( new_row, ignore_index=True )
    df.to_csv( "data_experiment.csv", index=False)
    return redirect( url_for( "index" ))


if __name__ == '__main__':
    app.run( port=5000, debug=True)