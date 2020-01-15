from . import db
from . import login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))


    @property
    def password(self):
        raise AttributeError('You Cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'User {self.username}'



#Post, Comment, Upvote, Downvote
class Pitch(db.Model):
    __tablename__='posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    text = db.Column(db.String(140))
    author = db.Column(db.Integer())
    timestamp = db.Column(db.DateTime(), index=True)

    
    def save_pitch(self):
        db.session.add(self)
        db.session.commit()
        pass

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    author = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime(), index=True)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'{self.text}'

class Upvote(db.Model):
    __tablename__='upvotes'
    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Integer, default=0)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pitch = db.Column(db.Integer, db.ForeignKey('posts.id'),nullable=False)

    def save_likes(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

    def __str__(self):
        return self.user.username


class Downvote(db.Model):
    __tablename__= 'downvotes'

    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Integer, default=0)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pitch = db.Column(db.Integer, db.ForeignKey('posts.id'),nullable=False)

    

    def save_dislikes(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

    def __str__(self):
        return self.user.username
    
