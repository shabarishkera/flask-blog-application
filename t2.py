from flask import  Flask,render_template
app=Flask(__name__);
@app.route("/")
def boot():
    return  render_template("bootsrap.html")
app.run()