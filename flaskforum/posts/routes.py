from flask import render_template, redirect, flash, request, abort, Blueprint, url_for, current_app
from flask_login import current_user, login_required
from flaskforum import db
from flaskforum.models import Post, Reply, Vote
from flaskforum.posts.forms import PostForm
from flaskforum.replies.forms import ReplyForm
import os
posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content = form.content.data, author = current_user)
		db.session.add(post)
		db.session.commit()
		# flash('Your post has been created', 'success')
		return redirect(url_for('main.home'))
	image_file = url_for('static', filename='profiles/' + current_user.image_file)
	return render_template('create_post.html', title = 'New Post',
		form = form, legend = 'New Post', action = 'Create',image_file=image_file)

@posts.route("/post/<int:post_id>/update", methods = ['GET','POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		# flash('Your post has been updated', 'success')
		return redirect(url_for('users.my_posts'))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
		image_file = url_for('static', filename='profiles/' + current_user.image_file)
	return render_template('create_post.html', title = 'Update Post',
		form = form, legend = 'New Post', action = 'Update',image_file=image_file)

@posts.route("/post/<int:post_id>/delete", methods = ['GET','POST'])
@login_required
def delete_post(post_id):
	print(post_id)
	reply = Reply.query.filter_by(post_id = post_id).all()
	print(reply)
	for replya in reply:
		a =replya.id
		print(a)
		Reply.query.filter(Reply.id == a).delete()
		db.session.commit()

	reply = Vote.query.filter_by(post_id = post_id).all()
	print(reply)
	for replya in reply:
		a =replya.id
		print(a)
		Vote.query.filter(Vote.id == a).delete()
		db.session.commit()



	reply = Post.query.get_or_404(post_id)
	print(reply)
	Post.query.filter(Post.id == post_id).delete()
	db.session.commit()
	audiosave = str(post_id) + '.mp3'
	hyy = os.path.join(current_app.root_path, 'static/music', audiosave)
	os.remove(hyy)
		# post = Post.query.get_or_404(post_id)
	# print(post)
	# db.session.delete(post)
	# db.session.commit()
	# flash('Your post has been deleted', 'info')
	return redirect(url_for('users.my_posts'))