from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from . import main 
from flask_login import login_required, current_user
from .forms import *
from .. import db
from sqlalchemy import func
from ..models import *

import datetime 
import pytz


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/',methods = ['GET', 'POST'])

def index():

    '''
    View root page function that returns the index page and its data
    '''
    # general = Pitch.query.filter_by(category="general").order_by(Pitch.posted.desc()).all()
    # project = Pitch.query.filter_by(category="project").order_by(Pitch.posted.desc()).all()
    # advertisement = Pitch.query.filter_by(category="advertisement").order_by(Pitch.posted.desc()).all()
    # sale = Pitch.query.filter_by(category="sale").order_by(Pitch.posted.desc()).all()

    # pitch = Pitch.query.filter_by().first()
    # likes = Like.get_all_likes(pitch_id=Pitch.id)
    # dislikes = Dislike.get_all_dislikes(pitch_id=Pitch.id)


    title = 'Home | One Min Pitch'
    return render_template('index.html')



@main.route('/user/<uname>')
def profile(uname):
    '''
    View profile page function that returns the profile page and its data
    '''
    user = User.query.filter_by(username = uname).first()
    title = f"{uname.capitalize()}'s Profile"

    get_pitches = Pitch.query.filter_by(author = User.id).all()
    get_comments = Comment.query.filter_by(user_id = User.id).all()
    get_likes = Like.query.filter_by(user_id = User.id).all()
    get_dislikes = Dislike.query.filter_by(user_id = User.id).all()

    if user is None:
        abort (404) 

    return render_template("profile/profile.html", user = user, title=title, pitches_no = get_pitches, comments_no = get_comments, likes_no = get_likes, dislikes_no = get_dislikes)


# @main.route('/user/<uname>/update',methods = ['GET','POST'])
# @login_required
# def update_profile(uname):
#     '''
#     View update profile page function that returns the update profile page and its data
#     '''
#     user = User.query.filter_by(username = uname).first()
#     if user is None:
#         abort(404)

#     form = UpdateProfile()

#     if form.validate_on_submit():
#         user.bio = form.bio.data

#         db.session.add(user)
#         db.session.commit()

#         return redirect(url_for('.profile',uname=user.username))

#     return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods=['POST'])
@login_required
def update_pic(uname):
    '''
    View update pic profile function that returns the uppdate profile pic page
    '''
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))



@main.route('/home', methods = ['GET', 'POST'])
@login_required
def index2():
    '''
    View index2 function that returns the home page
    '''
    advertisement = Pitch.query.filter_by(category="advertisement").order_by(Pitch.date.desc()).all()
    project = Pitch.query.filter_by(category="project").order_by(Pitch.date.desc()).all()
    general = Pitch.query.filter_by(category="general").order_by(Pitch.date.desc()).all()
    sale = Pitch.query.filter_by(category="sale").order_by(Pitch.date.desc()).all()
    pitch = Pitch.get_all_pitches()

    title = 'Home | One Min Pitch'
    return render_template('home.html', title = title, pitch = pitch, advertisement = advertisement, project = project, general = general, sale = sale)


@main.route('/pitch/new',methods = ['GET','POST'])
@login_required
def pitch():
    '''
    View pitch function that returns the pitch page and data
    '''
    pitch_form = PitchForm()
    # likes = Like.query.filter_by(pitch_id=Pitch.id)

    def generate_timestamp():
        return datetime.datetime.now(tz=pytz.utc).isoformat()


    if pitch_form.validate_on_submit():
        text = pitch_form.content.data
        title = pitch_form.pitch_title.data
        timestamp = generate_timestamp()
        author = current_user._get_current_object().id     
    
        context = {
            "title":title,
            "text": text,
            "author":author,
            "timestamp":timestamp        
        }
        
        
        pitch = Pitch(title=title, text=text, author=current_user.id, timestamp=timestamp)
        pitch.save_pitch()

        return redirect(url_for('main.index'))
    return render_template('pitch.html', pitch_form=pitch_form )


    title = 'New Pitch | One Minute Pitch'
    return render_template('pitch.html', title = title, pitch_form = pitch_form)


@main.route('/pitch/<int:pitch_id>/comment',methods = ['GET', 'POST'])
@login_required
def comment(pitch_id):
    '''
    View comments page function that returns the comment page and its data
    '''

    comment_form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    if pitch is None:
        abort(404)

    if comment_form.validate_on_submit():
        comment_body = comment_form.comment_body.data
        

        new_comment = Comment(comment=comment_body, pitch_id = pitch_id, user = current_user)
        new_comment.save_comment()

        return redirect(url_for('.comment', pitch_id=pitch_id))

    comments = Comment.query.filter_by(pitch_id=pitch_id).all()
    title = 'New Comment | One Min Pitch'

    return render_template('comment.html', title = title, pitch=pitch ,comment_form = comment_form, comment = comments )





@main.route('/pitch/<int:pitch_id>/like',methods = ['GET','POST'])
@login_required
def like(pitch_id):
    '''
    View like function that returns likes
    '''
    pitch = Pitch.query.get(pitch_id)
    user = current_user

    likes = Like.query.filter_by(pitch_id=pitch_id)


    if Like.query.filter(Like.user_id==user.id,Like.pitch_id==pitch_id).first():
        return  redirect(url_for('.index'))

    new_like = Like(pitch_id=pitch_id, user = current_user)
    new_like.save_likes()
    return redirect(url_for('.index'))



@main.route('/pitch/<int:pitch_id>/dislike',methods = ['GET','POST'])
@login_required
def dislike(pitch_id):
    '''
    View dislike function that returns dislikes
    '''
    pitch = Pitch.query.get(pitch_id)
    user = current_user

    pitch_dislikes = Dislike.query.filter_by(pitch_id=pitch_id)

    if Dislike.query.filter(Dislike.user_id==user.id,Dislike.pitch_id==pitch_id).first():
        return redirect(url_for('.index'))

    new_dislike = Dislike(pitch_id=pitch_id, user = current_user)
    new_dislike.save_dislikes()
    return redirect(url_for('.index'))



