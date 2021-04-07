from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clidata.sqlite3'
app.config['SECRET_KEY'] = "aa20ff7c-8ad5-44a7-b0c3-8060b126e186"
db = SQLAlchemy(app)


class GithubUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    user = db.Column(db.String(80), unique=True, nullable=False)
    image_url = db.Column(db.String(1200), unique=False, nullable=False)
    profile = db.Column(db.String(1200), unique=False, nullable=False)
    typ3 = db.Column(db.String(10), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user

def update_or_insert(user_dict):
    # get all incoming ids and ids on database
    all_incoming_ids = set(user_dict.keys())
    all_ids = set(dict(db.session.query(GithubUser.id, GithubUser)))
    # which ones are already on db?
    updatable_ids = all_ids & all_incoming_ids
    # and which are new?
    insertable_ids = all_incoming_ids - updatable_ids
    # create the list of items to insert and to update in bulk
    upd = [user_dict[e] for e in updatable_ids]    
    ins = [user_dict[e] for e in insertable_ids]
    db.session.bulk_insert_mappings(GithubUser, ins)
    db.session.bulk_update_mappings(GithubUser, upd)
    db.session.commit()

    return True

def create_all():
    SQLAlchemy.create_all(db)
