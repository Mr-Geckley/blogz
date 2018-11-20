from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://builds-a-blog:buildsablog@localhost:8889/builds-a-blog'
app.config['SQLALCHEMY_ECHO']=True
db = SQLAlchemy(app)

app.secret_key = '8jsu7YchIOpwKmd8'

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    body = db.Column(db.String(300))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect('/blog')
    
@app.route('/blog', methods=['POST', 'GET'])
def display_blogs():

    all_posts = Post.query.all()
    id = request.query_string

    if request.method == 'GET':
        if not id:
            return render_template('blog.html', all_posts=all_posts)
        else: 
            e = int(request.args.get('e'))
            post = Post.query.get(e)
            return render_template('solo_posto.html', post=post)

@app.route('/newpost', methods= ['GET'])
def display_newpost_form():
    return render_template('newpost.html')

@app.route('/newpost', methods=['POST'])
def create_post():

    title = request.form['title']
    body = request.form['body']

    if not title and not body:
        return render_template('newpost.html', title_error="Need a title, fam", body_error="Look at all that empty")     

    elif not title:
        return render_template('newpost.html', title_error="Need a title, fam", body=body)    
        
    elif not body:
        return render_template('newpost.html', body_error="Look at all that empty", title=title)  
        
        return render_template('/blog?id={0}'.format(Post))

    else:
        new_post = Post(title, body)
        db.session.add(new_post)
        db.session.commit()
        
        post = new_post
    
    return render_template('solo_posto.html', post=post)
    
if __name__ == '__main__':
    app.run()