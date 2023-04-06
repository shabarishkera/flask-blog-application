
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

@app.route("/")
def index():
    param = [];
    cursor.execute('select title,content,date,author,slug from post');
    for (title, content,date,author,slug) in cursor:
        obj = {};
        obj['title'] = title;
        obj['date']=date;
        obj['author']=author;
        obj['content'] = content;
        obj['slug']=slug;
        param.append(obj)
        print(slug)
    return render_template("index.html",data=param);

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
@app.route("/post/<slug>")
def post(slug):
    cursor = conn.cursor();
    param=list({});
    cursor.execute('select title,content,date,author,slug from post');
    print(slug)
    for (title,content,date,author,slugrec )in cursor:
        if slugrec==slug :
         obj={};
         obj['title']=title;
         obj['content']=content;
         obj['date']=date;
         obj['author']=author;
         param.append(obj)
         print(title,content)
    return render_template("post.html",data=param);

app.run(debug=True)