import flask
from click.testing import CliRunner
from githubusers import get_github_users
from ghdb import db, GithubUser, update_or_insert, get_ghu_page
from seed import app

def test_repr():
    '''Chek the correct representation of github users.'''
    with app.app_context():
        db.init_app(app)
        uid=9_999_999_999
        user='anuser'
        image_url='https://avatars.githubusercontent.com/u/3?v=4'
        profile=f'https://github.com/%s'%user
        u = GithubUser(id=uid, user=user, image_url=image_url, profile=profile)
        assert u.id == uid
        assert u.user == user
        assert u.image_url == image_url
        assert u.profile == profile
        USER_FTM = "<User '%s'>"
        assert str(u) == USER_FTM%user
        assert repr(u) == USER_FTM%user
        assert u.__repr__() == USER_FTM%user

def test_can_update_or_insert():
    '''Test that the user can be updated.'''
    with app.app_context():
        db.init_app(app)
        first_user = get_github_users(1,0)
        upd_word = 'No profile!!!!'
        first_user[1]['profile'] = upd_word
        assert update_or_insert(first_user)
        # retrieve again from db
        first_user = dict(db.session.query(GithubUser.id, GithubUser))
        assert first_user[1].profile == upd_word

def test_pager_count():
    '''Test default and different pages/totals for the pager.'''
    with app.app_context():
        db.init_app(app)
        data1 = get_ghu_page(0, 10)
        assert 10 == len(data1[0])
        data2 = get_ghu_page(0, 1)
        assert 1 == len(data2[0])
        data3 = get_ghu_page(10, 10)
        assert 10 == len(data3[0])
        assert data3 not in data1
        # check default that is all the data
        all_data = get_ghu_page()
        assert all_data[1] == len(all_data[0])