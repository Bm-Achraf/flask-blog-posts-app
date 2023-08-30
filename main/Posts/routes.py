from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from main import db
from main.models.posts import Posts
from main.Posts.forms import CreatePost

posts = Blueprint('posts', __name__)



@posts.route("/createPost", methods=['GET', 'POST'])
@login_required
def createPost():

    form = CreatePost()

    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, user_id=current_user.id) #type: ignore

        db.session.add(post)
        db.session.commit()
        flash(f'New post created', 'success')
        return redirect(url_for('home.home'))

    return render_template('create_post.html', title='Create Posts', form=form)



@posts.route("/post/<int:postID>/update", methods=['GET', 'POST'])
@login_required
def updatePost(postID):

    form = CreatePost()
    post = Posts.query.get_or_404(postID)

    if post.author != current_user:
        abort(403)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'post updated', 'success')
        return redirect(url_for('home.home'))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Create Posts', form=form)


@posts.route("/post/<int:postID>/delete", methods=['GET'])
@login_required
def deletePost(postID):
    
    post = Posts.query.get_or_404(postID)

    if post and post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted susccessfuly', 'success')

    return redirect(url_for('home.home'))