from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://builds-a-blog:buildsablog@localhost:8889/builds-a-blog'
app.config['SQLALCHEMY_ECHO']=True
db = SQLAlchemy(app)

class Title(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    did_read = db.Column(db.Boolean, default=False)

    def __init__(self, title):
        self.title = title
        self.completed = False

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog = db.Column(db.String(300))

    def __init__(self, blog):
        self.blog = blog






@app.route('/blog', methods=['POST', 'GET'])
def index():

    title_and_blog = ''
    if request.method == 'POST':
        title_name = request.form['title']
        new_title = Title(title_name)
        db.session.add(new_title)
        db.session.commit()
        title_and_blog = title_and_blog + title_name
        
        blog_name = request.form['blog']
        new_blog = Blog(blog_name)
        db.session.add(new_blog)
        db.session.commit()
        title_and_blog = title_and_blog + blog_name
        
    
    titles = Title.query.filter_by(did_read=False).all()
    read_titles = Title.query.filter_by(did_read=True).all()
    blogs = Blog.query.all()
    return render_template('blog.html', title="BUILD-A-BLOG", 
        titles=titles, read_titles=read_titles, blogs=blogs)

@app.route("/newpost")
def new_post_form():
    return render_template('newpost.html')



if __name__ == '__main__':
    app.run()