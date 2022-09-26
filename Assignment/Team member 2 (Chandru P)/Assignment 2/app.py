from flask import Flask,render_template,request,url_for,redirect,flash 
from markupsafe import escape

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/home.html")
def hello():
    return render_template("home.html")

@app.route("/about.html")
def profile():
    return render_template("about.html")

@app.route("/signup.html")
def signup():
    return render_template("signup.html")


@app.route("/signin.html")
def signin():
    return render_template("signin.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404


# @app.route("/chat")
# def chat():
#     return render_template("chat.html", messages=messages)

# messages =[{"title":"message one", "content":"message one content"},{"title":"message one", "content":"message one content"},{"title":"message two","content":"message two content"}]

# @app.route("/create/", methods=('GET','POST'))
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
        
        
#         if not title:
#             flash('Title is required!')
#         elif not content:
#             flash('Content is required!')
#         else:
#             messages.append({'title':title, 'content':content})
#             name= 'ganesh'
#             return redirect(url_for('index', messages=messages ))
#     return render_template('create.html')
















# @app.route("/creat/" , methods=('GET','POST'))
# def create():
#     if request.method=='POST':
#         title = request.form['title']


# @app.route('/')
# def index():
#     return render_template('index.html', messages=messages)

# @app.route('/admin')
# def hello_admin():
#     return 'hello admin'

# @app.route('/guest/<guest>')
# def hello_guest(guest):
#     return 'hello %s as Guest' % guest

# @app.route('/user/<name>')
# def hello_user(name):
#     if name== 'admin':
#         return redirect(url_for('hello_adimin'))
