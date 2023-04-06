
from flask import  Flask,render_template,request
from flaskext.mysql import MySQL
#from flask_sqlalchemy import SQLAlchemy
#db = SQLAlchemy()
app=Flask(__name__)
db= MySQL();
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'blog'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
db.init_app(app)
conn = db.connect()
cursor =conn.cursor()


# class Contact(db.Model):
#     name = db.Column(db.String, nullable=False)
#     message = db.Column(db.String, nullable=False)
#     email = db.Column(db.String,primary_key=True)
#     phone=db.Column(db.Integer,unique=False)
@app.route("/")
def index():
    return render_template("index.html");

@app.route("/about")
def about():
    return render_template("about.html");
@app.route("/contact",methods=['GET','POST'])
def contact():
    if(request.method=='GET'):
      print("welome")
      return render_template("contact.html");
    elif request.method=='POST':
     name=request.form['name']
     email= request.form['email'];
     phone = request.form['phone'];
     message = request.form['message'];
     cursor.execute('INSERT INTO contact VALUES (% s, % s, % s ,% s)', (name, email,phone,message))
     conn.commit();
     return  render_template('index.html')
@app.route("/post")
def post():
    return render_template("post.html");
app.run(debug=True)