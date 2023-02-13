from flask import Flask, render_template, redirect, url_for
import numpy as np

app = Flask( __name__ )

@app.route( '/home' )
def index():
    if np.random.random() < 0.5:
        return render_template("page_blue.html")
    else:
        return render_template("page_red.html")

@app.route( "/yes", methods=['POST'] )
def yes_event():
    return redirect( url_for( "index" ))

@app.route( "/no", methods=['POST'] )
def no_event():
    return redirect( url_for( "index" ))


if __name__ == '__main__':
    app.run(debug=True)