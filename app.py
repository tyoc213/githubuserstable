import flask
from flask import request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from ghdb import db, get_ghu_page
from flask_caching import Cache
from flask_paginate import Pagination, get_page_args
import os

def create_app():
    '''Create app with sqlalchemy (without events) and simple cache.'''
    app = flask.Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clidata.sqlite3'
    app.config['SECRET_KEY'] = "aa20ff7c-8ad5-44a7-b0c3-8060b126e186"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # disable sqlalchemy events
    app.config['CACHE_TYPE'] = "SimpleCache"
    app.config['CACHE_DEFAULT_TIMEOUT']= 300
    return app

app = create_app()
db=SQLAlchemy(app)
cache = Cache(app)

@app.route('/favicon.ico')
def favicon():
    '''Returns the favicon.'''
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET'])
@cache.cached(timeout=10, query_string=True)
def main():
    '''Displays a specific `page` with `total` users'''
    total=5000 # TODO: get from db
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='total')
    pagination = Pagination(page=page, per_page=per_page, total=total)
    data = get_ghu_page(page, per_page)
    user_list = data[0]
    total_pages = data[1]
    return(flask.render_template('main.html', user_list=user_list, total_pages=total_pages,
                            total=total, 
                            page=page,
                           per_page=per_page,
                           pagination=pagination))

@app.route('/all', methods=['POST', 'GET'])
@cache.memoize(10)
def all_users():
    '''JSON response with all users.'''
    data = get_ghu_page()
    user_list = data[0]
    # total_pages = data[1]
    user_list = [o.serialize() for o in user_list]
    return flask.json.jsonify(user_list)

@app.route('/dt', methods=['GET'])
def show_datatable():
    '''Renders datatable.'''
    return flask.render_template('datatable.html')

if __name__ == '__main__':
    app.run(debug=True)
