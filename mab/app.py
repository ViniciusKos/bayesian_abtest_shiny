import numpy as np
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request


app = Flask( __name__ )

@app.route( '/home' )
def index():
    # get data

    df = pd.concat( [ pd.read_csv(f"data_collected_{i}.csv") for i in ["red","blue"] ] )
    df['no_click'] = df['visit'] - df['click']

    click_array = df.groupby( "group" ).sum().reset_index()[['click', 'no_click']].T.to_numpy()


    print( click_array )
    # Thompson Agent
    prob_reward = np.random.beta( click_array[0], click_array[1] )

    if np.argmax( prob_reward ) == 0:
        return render_template( "page_blue.html" )
    else:
        return render_template( "page_red.html" )



@app.route( "/yes", methods=['POST'] )
def yes_event():
    df0 = pd.concat( [ pd.read_csv(f"data_collected_{i}.csv") for i in ["red","blue"] ] )
    if request.form['yescheckbox'] =='blue':
        new_row = {"click":1, "visit":1, "group":"treatment"}
        df0 = df0.append( new_row, ignore_index=True )
    else:
        new_row = {"click":1, "visit":1, "group":"control"}
        df0 = df0.append( new_row, ignore_index=True )

    df0.to_csv( "data_experiment.csv", index=False)
    return redirect( url_for( "index" ))



@app.route( "/no", methods=['POST'] )
def no_event():
    df0 = pd.concat( [ pd.read_csv(f"data_collected_{i}.csv") for i in ["red","blue"] ] )
    if request.form['nocheckbox'] =='blue':
        new_row = {"click":0, "visit":1, "group":"treatment"}
        df0 = df0.append( new_row, ignore_index=True )
    else:
        new_row = {"click":0, "visit":1, "group":"control"}
        df0 = df0.append( new_row, ignore_index=True )

    df0.to_csv( "data_experiment.csv", index=False)
    return redirect( url_for( "index" ))



if __name__ == '__main__':
    app.run( port=5000, debug=True)