from flask import Flask, render_template
app = Flask( __name__ )

@app.route( '/home' )
def index():
    return render_template("page_blue.html")
    
if __name__ == '__main__':
    app.run()