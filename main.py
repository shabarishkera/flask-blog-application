from flask import Flask, render_template, request, session
from flaskext.mysql import MySQL

# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
app = Flask(__name__)
db = MySQL();
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'blog'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
db.init_app(app)
conn = db.connect()
cursor = conn.cursor()
app.secret_key = '234432W99*()_)^%'


@app.route("/")
def index():
    param = [];
    cursor.execute('select title,content,date,author,slug from post');
    for (title, content, date, author, slug) in cursor:
        obj = {};
        obj['title'] = title;
        obj['date'] = date;
        obj['author'] = author;
        obj['content'] = content;
        obj['slug'] = slug;
        param.append(obj)

    return render_template("index.html", data=param);


@app.route("/about")
def about():
    return render_template("about.html");


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method == 'GET'):

        return render_template("contact.html");
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email'];
        phone = request.form['phone'];
        message = request.form['message'];
        cursor.execute('INSERT INTO contact VALUES (% s, % s, % s ,% s)', (name, email, phone, message))
        conn.commit();
        return render_template('index.html')


@app.route("/post/<slug>")
def post(slug):
    cursor = conn.cursor();
    param = list({});
    cursor.execute('select title,content,date,author,slug from post');

    for (title, content, date, author, slugrec) in cursor:
        if slugrec == slug:
            obj = {};
            obj['title'] = title;
            obj['content'] = content;
            obj['date'] = date;
            obj['author'] = author;
            param.append(obj)

    return render_template("post.html", data=param);


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if (request.method == 'GET'):
        return render_template('adminlogin.html');
    param = [];
    cursor.execute('select sl, title,content,date,author,slug from post');
    for (sl, title, content, date, author, slug) in cursor:
        obj = {};
        obj['title'] = title;
        obj['date'] = date;
        obj['author'] = author;
        obj['content'] = content;
        obj['slug'] = slug;
        obj['sl'] = sl;
        param.append(obj)

    email = request.form['email']
    password = request.form['password'];
    if 'logged-email' in session and session['logged-email'] == email:
        return render_template('dashboard.html', data=param);

    cursor.execute('select * from admins where email=\'%s\' and password=\'%s\'' % (email, password))
    if (cursor.rowcount == 0):
        return render_template('adminlogin.html');

    session['logged-email'] = email;
    return render_template('dashboard.html', data=param);


@app.route("/edit/<sl>", methods=['POST', 'GET'])
def edit(sl):
    if (request.method == 'POST'):
        ntitle = request.form['title'];
        ncontent = request.form['content']
        nsl = request.form['sl'];
        cursor.execute('update post set title=%s , content=%s where sl=%s', (ntitle, ncontent, nsl));
        conn.commit();
        return render_template("index.html")
    cursor.execute('select title,content from post where sl=%s ' % (sl));
    row = cursor.fetchone();

    title, content = row;

    return render_template("edit.html", title=title, content=content, sl=sl)


@app.route("/logout")
def logout():
    session.pop('logged-email');
    return render_template("adminlogin.html")
@app.route("/addpost",methods=['GET','POST'])
def addpost():
    if(request.method=='GET'):
     return  render_template('addpost.html')
    title=request.form['title'];
    slug=request.form['slug'];
    content=request.form['content'];
    date=request.form['date'];
    author=request.form['author'];
    cursor.execute('INSERT INTO post (title,content,author,date,slug)  VALUES (% s, % s, % s ,% s ,% s)', (title,content,author, date,slug))
    conn.commit();
    param = [];
    cursor.execute('select sl, title,content,date,author,slug from post');
    for (sl, title, content, date, author, slug) in cursor:
        obj = {};
        obj['title'] = title;
        obj['date'] = date;
        obj['author'] = author;
        obj['content'] = content;
        obj['slug'] = slug;
        obj['sl'] = sl;
        param.append(obj)
    return  render_template('dashboard.html',data=param);
app.run(debug=True)
