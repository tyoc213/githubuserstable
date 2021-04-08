from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

class GithubUser(db.Model):
    '''GithubUser is the default model to store github profiles.'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    user = db.Column(db.String(80), unique=True, nullable=False)
    image_url = db.Column(db.String(1200), unique=False, nullable=False)
    profile = db.Column(db.String(1200), unique=False, nullable=False)
    typ3 = db.Column(db.String(10), unique=False, nullable=False)

    def serialize(self):
        '''Return a dict of the members that canbe serialized.'''
        return {
            'id': self.id,
            'user': self.user,
            'image_url': self.image_url,
            'profile': self.profile,
            'type': self.typ3
            }

    def __repr__(self):
        '''User representation for printing.'''
        return '<User %r>' % self.user

def update_or_insert(user_dict):
    '''Fetch github users and upsert them on DB.'''
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

def get_ghu_page(page=0, total=None, username=None,order_by=None):
    '''Get a specific page with `total` users.'''
    # TODO: GithubUser.id.asc() throws error
    if username:
        print('username', username)
        postlist = GithubUser.query.filter_by(user=username)
    elif total is None:
        postlist = GithubUser.query.filter(GithubUser.id).offset(page).all()
    else:
        # calculate an offset to the page, but at start of page
        page_offset = page * total
        if order_by is not None:
            if order_by == 'id': order_by = GithubUser.id
            elif order_by == 'user': order_by = GithubUser.user
            elif order_by == 'profile': order_by = GithubUser.profile
            elif order_by == 'type': order_by = GithubUser.typ3
        postlist = GithubUser.query.filter(GithubUser.id).order_by(order_by).offset(page_offset).limit(total).all()
    count = db.session.query(GithubUser).count()
    return postlist, count

def get_ghu_total():
    '''Get the `total` users.'''
    return db.session.query(GithubUser).count()