from flask import Flask, request, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thiranex-akhila-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# MODELS
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref='posts')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post = db.relationship('Post', backref='comments')
    author = db.relationship('User')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# HTML TEMPLATE BASE
BASE = """
<html><head><style>
body{font-family:sans-serif; max-width:800px; margin:20px auto; padding:20px}
a{margin-right:10px} .card{border:1px solid #ccc; padding:15px; margin:10px 0; border-radius:8px}
input,textarea{width:100%; padding:8px; margin:5px 0} button{padding:8px 15px; background:#2563eb; color:white; border:none; border-radius:5px}
</style></head><body>
<h1><a href="/">BlogSphere 🚀</a></h1>
{% if current_user.is_authenticated %}
Hello {{current_user.username}}! <a href="/create">+ New Post</a> <a href="/logout">Logout</a>
{% else %}
<a href="/login">Login</a> <a href="/register">Register</a>
{% endif %}<hr>{{content|safe}}</body></html>
"""

@app.route('/')
def home():
    posts = Post.query.order_by(Post.date.desc()).all()
    html = ""
    for p in posts:
        html += f"<div class='card'><h2><a href='/post/{p.id}'>{p.title}</a></h2><p>{p.content[:200]}...</p><small>By {p.author.username} on {p.date.strftime('%d-%m-%Y')} | {len(p.comments)} comments</small><br>"
        if current_user.is_authenticated and p.user_id == current_user.id:
            html += f"<a href='/edit/{p.id}'>Edit</a> <a href='/delete/{p.id}'>Delete</a>"
        html += "</div>"
    return render_template_string(BASE, content=html or "<p>No posts yet. Create one!</p>")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        hashed = generate_password_hash(request.form['password'])
        u = User(username=request.form['username'], email=request.form['email'], password=hashed)
        db.session.add(u); db.session.commit(); return redirect('/login')
    return render_template_string(BASE, content="<h2>Register</h2><form method='POST'><input name='username' placeholder='Username' required><input name='email' placeholder='Email' required><input type='password' name='password' placeholder='Password' required><button>Register</button></form>")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        u = User.query.filter_by(email=request.form['email']).first()
        if u and check_password_hash(u.password, request.form['password']):
            login_user(u); return redirect('/')
        return "Invalid login"
    return render_template_string(BASE, content="<h2>Login</h2><form method='POST'><input name='email' placeholder='Email' required><input type='password' name='password' placeholder='Password' required><button>Login</button></form>")

@app.route('/logout')
def logout():
    logout_user(); return redirect('/')

@app.route('/create', methods=['GET','POST'])
@login_required
def create():
    if request.method=='POST':
        p = Post(title=request.form['title'], content=request.form['content'], user_id=current_user.id)
        db.session.add(p); db.session.commit(); return redirect('/')
    return render_template_string(BASE, content="<h2>Create Post</h2><form method='POST'><input name='title' placeholder='Title' required><textarea name='content' placeholder='Content' rows='6' required></textarea><button>Post</button></form>")

@app.route('/post/<int:id>', methods=['GET','POST'])
def view_post(id):
    p = Post.query.get_or_404(id)
    if request.method=='POST':
        if not current_user.is_authenticated: return redirect('/login')
        c = Comment(content=request.form['comment'], post_id=p.id, user_id=current_user.id)
        db.session.add(c); db.session.commit()
    comments = "".join([f"<div class='card'><p>{c.content}</p><small>By {c.author.username}</small></div>" for c in p.comments])
    html = f"<div class='card'><h2>{p.title}</h2><p>{p.content}</p><small>By {p.author.username}</small></div><h3>Comments ({len(p.comments)})</h3>{comments}<hr>"
    if current_user.is_authenticated:
        html += "<form method='POST'><textarea name='comment' placeholder='Add a comment' required></textarea><button>Comment</button></form>"
    else:
        html += "<a href='/login'>Login to comment</a>"
    return render_template_string(BASE, content=html)

@app.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
    p = Post.query.get_or_404(id)
    if p.user_id != current_user.id: return "Not allowed"
    if request.method=='POST':
        p.title = request.form['title']; p.content = request.form['content']; db.session.commit(); return redirect('/')
    return render_template_string(BASE, content=f"<h2>Edit</h2><form method='POST'><input name='title' value='{p.title}' required><textarea name='content' rows='6' required>{p.content}</textarea><button>Update</button></form>")

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    p = Post.query.get_or_404(id)
    if p.user_id == current_user.id:
        db.session.delete(p); db.session.commit()
    return redirect('/')

# RESTful APIs
@app.route('/api/posts', methods=['GET'])
def api_posts():
    posts = Post.query.all()
    return {"posts": [{"id":p.id, "title":p.title, "content":p.content, "author":p.author.username} for p in posts]}

with app.app_context():
    db.create_all()

if __name__=='__main__':
    app.run()
