import numpy as np
import pandas as pd

from flask import Flask, render_template, redirect, url_for


app = Flask( __name__ )

@app.route( '/home' )
def index():
    return render_template( "page_red.html" )

@app.route( "/yes", methods=['POST'] )
def yes_event():
    df = pd.read_csv("data_collected_red.csv")
    df_append = pd.DataFrame( {"click":1, "visit":1, "group":"control"} , index=[0])
    df = pd.concat( [df, df_append], ignore_index=True )
    df.to_csv("data_collected_red.csv", index=False)
    return redirect( url_for( "index" ))

@app.route( "/no", methods=['POST'] )
def no_event():
    df = pd.read_csv("data_collected_red.csv")
    df_append = pd.DataFrame( {"click":0, "visit":1, "group":"control"} , index=[0])
    df = pd.concat( [df, df_append], ignore_index=True  )
    df.to_csv("data_collected_red.csv", index=False)
    return redirect( url_for( "index" ))


if __name__ == '__main__':
    app.run( port=5000, debug=True)