from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'codeiscool'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route('/')
def root():
    '''Homepage'''

    return redirect("/users")


#User App Routes 

@app.route('/users')
def users_index():
    '''page with info on users'''

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('index.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    '''form to create a new user'''

    return render_template('new.html')


@app.route("/users/new", methods=["POST"])
def users_new():
    '''POST method gor form submission for creating a new user'''

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def users_show(user_id):
    '''Show a page with info on a specific user'''

    user = User.query.get_or_404(user_id)
    return render_template('show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    '''Show a form to edit an existing user'''

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    '''Handle form submission for updating an existing user'''

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    '''Handle form submission for deleting an existing user'''

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

# app route for Posts 

@app.route('/users/<int:user_id>/posts_new')
def new_post_form(user_id):
    """show form to add post for user"""
    user = User.query.get_or_404(user_id)
    return render_template('posts_new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods =["POST"]) 
def add_post(user_id):
    """Get the value from form and add post"""
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user_id=user.id)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts_show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show a form to edit an post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts_edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods =["POST"])
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

## App routes for tags 


@app.route('/tags')
def list_all_tags():
    tags = Tag.query.all()
    return render_template('tag_list.html', tags = tags)

@app.route('/tags/new')
def tags_new_form():
    """Show a form to create a new tag"""
    posts = Post.query.all()
    return render_template('add_tag.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tag_show.html', tag = tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tag_edit.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")