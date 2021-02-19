from flask import Flask,render_template,url_for,request,redirect

from flask_ckeditor import CKEditor

from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config["CKEDITOR_PKG_TYPE"]='basic'
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///app.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


db=SQLAlchemy(app)

ckeditor=CKEditor(app)

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(255),nullable=False)
    body=db.Column(db.UnicodeText())

    def __repr__(self):
        return f"<Post {self.title}>"

@app.route('/',methods=['GET','POST'])
def index():
    if request.method =="POST":
        title=request.form.get('title')
        body=request.form.get('ckeditor')

        new_post=Post(title=title,body=body)

        db.session.add(new_post)
        db.session.commit()

        return redirect('/posts')

    return render_template('index.html')


@app.route('/posts',methods=["GET"])
def post_list():
    posts=Post.query.all()

    return render_template('posts.html',posts=posts)


@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit_post(id):

    post_to_edit=Post.query.get_or_404(id)
    
    if request.method == 'POST':
        post_to_edit.title=request.form.get('title')
        post_to_edit.body=request.form.get('ckeditor')

        db.session.commit()

        return redirect('/posts')

    return render_template('edit.html',post=post_to_edit)


@app.route('/delete/<int:id>')
def delete(id):
    post_to_delete=Post.query.get_or_404(id)
    db.session.delete(post_to_delete)
    db.session.commit()

    return redirect('/posts')

@app.shell_context_processor
def make_shell_context():
    return {
        "app":app,
        "db":db,
        "Post":Post
    }


if __name__ == '__main__':
    app.run(debug=True)