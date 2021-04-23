from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required, login_user, current_user, logout_user
from flaskforum import db
from flaskforum.models import User, Post, Vote, Reply
from flaskforum.replies.forms import ReplyForm

replies = Blueprint('replies', __name__)

@replies.route("/reply/<int:post_id>/", methods = ['GET','POST'])
@login_required
def reply_post(post_id):
	#reply = Reply.query.filter_by(user_id = user_id, post_id = post_id).first()
	form = ReplyForm()
	# print('hey11')
	# print(form.content.data)
	# if form.validate_on_submit():
	post = Post.query.get_or_404(post_id)
	# print('hey')
	# print(form.content.data)
	reply = Reply(content = form.content.data, user = current_user, post = post)
	db.session.add(reply)
	db.session.commit()
	return redirect(url_for('main.post_expand', post_id = post_id))