#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
import sys

from sqlalchemy import desc

from model import db_init,db, Post
from config import SQLITE_DATABASE_NAME

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + SQLITE_DATABASE_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.app = app
db.init_app(app)

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

@app.route('/guestbook.html')
def guestbook():
    posts = Post.query.order_by(desc(Post.updated_on)).all()
    return render_template("guestbook.html", posts=posts)

@app.route('/add_to_guestbook.html', methods=['GET', 'POST'])
def add_to_guestbook():
    if request.method == "POST":
        name = request.form.get('name', type=str, default='')
        text = request.form.get('text', type=str, default='')
        if not text:
            return redirect(url_for('guestbook'))
        if not name:
            name = "Аноним"
        try:
            p = Post(name=name, text=text)
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('guestbook'))
        except:
            return render_template("add_to_guestbook.html")

    return render_template("add_to_guestbook.html")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "init":
            with app.app_context():
                db_init()
                sys.exit(0)
    app.run()