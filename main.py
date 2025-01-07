from datetime import date
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from forms import CreatePostForm
import os
import requests
import json
import pyperclip
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

ckeditor = CKEditor(app)
Bootstrap5(app)

try:
    blog_data = requests.get(f"https://api.npoint.io/{os.getenv("NPOINT")}").json()
except Exception:
    with open("static/assets/content/backup-latest.json", "r") as file:
        blog_data = json.load(file)

@app.route('/')
def get_all_posts():
    page = int(request.args.get("page", 1))
    posts_per_page = 10
    start = (page - 1) * posts_per_page
    end = page * posts_per_page
    posts = blog_data[start:end]
    max_page = (len(blog_data) + posts_per_page - 1) // posts_per_page 

    if page < 1 or page > max_page:
        return redirect(url_for("home"))

    return render_template("index.html", all_posts=posts, page=page, max_page=max_page)


@app.route("/<post_title>", methods=["GET", "POST"])
def show_post(post_title):
    # Convert the post_title to lowercase and replace spaces with dashes
    post_title = post_title.lower().replace(' ', '-')

    # Find the requested post
    requested_post = [post for post in blog_data if
                      post["title"].lower().replace(' ', '-') == post_title]

    return render_template("post.html", post=requested_post[0])

@app.route("/new", methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():

        new_post_data = {
            "id": 0,
            "title": form.title.data,
            "subtitle": form.subtitle.data,
            "date": date.today().strftime("%B %d, %Y"),
            "author": form.author.data,
            "image_url": form.img_url.data,
            "body": form.body.data,
        }

        dump_and_copy(new_post_data)

        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)

@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = [post for post in blog_data if post["id"] == post_id][0]
    form = CreatePostForm(
        title=post["title"],
        subtitle=post["subtitle"],
        img_url=post["image_url"],
        author=post["author"],
        body=post["body"]
    )
    if form.validate_on_submit():
        post["title"] = form.title.data
        post["subtitle"] = form.subtitle.data
        post["image_url"] = form.img_url.data
        post["author"] = form.author.data
        post["body"] = form.body.data

        dump_and_copy(post)

        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)

def dump_and_copy(data: dict):
    # Convert the dictionary to a JSON string
    json_data = json.dumps(data, indent=2)

    try:
        # Copy the JSON data to the clipboard
        pyperclip.copy(json_data)
        flash(f"Post copied to clipboard as json.")
    except pyperclip.PyperclipException:
        flash("Failed to copy post to clipboard. Please copy manually.")


if __name__ == "__main__":
    app.run(debug=False)


