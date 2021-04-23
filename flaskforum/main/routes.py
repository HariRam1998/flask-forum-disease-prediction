from flask import render_template, current_app, url_for, flash, redirect, request, Blueprint
from flask import render_template, request, Blueprint
from flaskforum.models import Post, Vote, Reply, User
from flask_login import current_user, login_required
from flaskforum.replies.forms import ReplyForm
from gtts import gTTS
import os

main = Blueprint('main',__name__)
imagefile = "static/download.jpg"
@main.route("/")
@main.route("/home")
def home():

	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	votes = Vote.query.all()
	form = ReplyForm()
	replies = Reply.query.all()
	if current_user.is_authenticated:
		imagefile1 = url_for('static', filename='profiles/' + current_user.image_file)
		return render_template('home.html', title='Home',
							   posts=posts, votes=votes, form=form, replies=replies, page=page, image_file=imagefile1)
	else:
		return render_template('home.html', title = 'Home',
			posts = posts, votes = votes, form = form, replies = replies, page = page,image_file=imagefile)

@main.route("/post_expand/<int:post_id>", methods = ['GET','POST'])
def post_expand(post_id):
	page = request.args.get('page', 1, type=int)
	a = post_id
	posts = Post.query.filter_by(id = a)\
		.order_by(Post.date_posted.desc())\
		.paginate()
	a3 = posts
	audiosave = str(post_id) + '.mp3'
	hyy = os.path.join(current_app.root_path, 'static/music', audiosave )
	if os.path.isfile(hyy) != True:
		for a5 in a3.items:
			a6 = str(a5.content)
			obj = gTTS(text=a6, slow=False, lang='en')
			audio_path = os.path.join(current_app.root_path, 'static/music', audiosave )
			obj.save(audio_path)
			break
	votes = Vote.query.all()
	form = ReplyForm()
	replies = Reply.query.all()
	if current_user.is_authenticated:
		imagefile1 = url_for('static', filename='profiles/' + current_user.image_file)
		return render_template('home1.html', title='Search',
							   posts=posts, votes=votes, form=form, replies=replies,page=page, image_file=imagefile1, hey=audiosave)
	else:
		return render_template('home1.html', title='Search',
							   posts=posts, votes=votes, form=form, replies=replies,page=page, image_file=imagefile, hey=audiosave)


@main.route("/about")
def about():
	if current_user.is_authenticated:
		imagefile1 = url_for('static', filename='profiles/' + current_user.image_file)
		return render_template('about.html', title='About', image_file=imagefile1)
	else:
		return render_template('about.html', title = 'About',image_file=imagefile)

@main.route("/home/search", methods=['GET', 'POST'])
def search():
	search1 = request.form['searching']
	print(search1)
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter(Post.title.contains(search1))\
		.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=5)
	print(posts)
	votes = Vote.query.all()
	form = ReplyForm()
	replies = Reply.query.all()
	if current_user.is_authenticated:
		imagefile1 = url_for('static', filename='profiles/' + current_user.image_file)
		return render_template('home.html', title='Search',
							   posts=posts, votes=votes, form=form, replies=replies, page=page, image_file=imagefile1)
	else:
		return render_template('home.html', title = 'Search',
			posts = posts, votes = votes, form = form, replies = replies, page = page,image_file=imagefile)


