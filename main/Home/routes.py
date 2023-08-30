from flask import Blueprint, render_template, request

from main.models.posts import Posts

mainHome = Blueprint('home', __name__)


@mainHome.route("/home")
@mainHome.route("/")
def home():
    page = request.args.get('page', default=1, type=int)

    #page = int(str(request.args.get('page')).split('=',1)[1])

    posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=1)

    return render_template("home.html", posts=posts)





@mainHome.route("/about")
def about():
    return render_template("about.html", title="About")