"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/checkmark-png-28.png"


class User(db.Model):
    """user"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)
    post = db.relationship('Post')

    @property
    def full_name(self):
        """Return name of user."""

        return f"{self.first_name} {self.last_name}"


def connect_db(app):
 

    db.app = app
    db.init_app(app)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key = True, autoincrement =True)
    title = db.Column(db.String(40), nullable = False, unique = True)
    content = db.Column(db.Text, nullable = False, unique = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('User')

class Tag(db.Model):
    __tablename__ ='tag'
    id = db.Column(db.Integer, primary_key = True, unique = False)
    name = db.Column(db.Text, nullable=False, unique=True)
    
    #Create the relationship with post_tag table
    post_tags= db.relationship('PostTag', backref = 'tag')
    

class PostTag(db.Model):
    __tablename__ = 'post_tag'
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key = True, unique = False)