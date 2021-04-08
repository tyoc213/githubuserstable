#!/usr/bin/env python

import click
import flask
from flask_sqlalchemy import SQLAlchemy
from githubusers import get_github_users
from ghdb import db, create_all, update_or_insert
from flask_caching import Cache

def create_app():
    '''Create app with sqlalchemy (without events) and simple cache.'''
    app = flask.Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clidata.sqlite3'
    app.config['SECRET_KEY'] = "aa20ff7c-8ad5-44a7-b0c3-8060b126e186"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CACHE_TYPE'] = "SimpleCache"
    app.config['CACHE_DEFAULT_TIMEOUT']= 300
    return app
print('creating app')
app=create_app()
print('app created')
db=SQLAlchemy(app)
print('database craeted')
cache = Cache(app)


@click.command()
@click.option('--total', default=150, show_default=True) # TODO: type=click.IntRange(1, 100)
@click.option('--page', default=0, show_default=True)
def seed(total, page):
    '''Save the users from github user list'''
    create_all()
    user_list = get_github_users(total, page)
    update_or_insert(user_list)    
    click.echo(f'%d users'%(total))

if __name__ == '__main__':
    with app.app_context():
        seed()