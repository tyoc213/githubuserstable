from click.testing import CliRunner
from githubusers import get_github_users
from ghdb import db, GithubUser, update_or_insert


def test_can_update_or_insert():
    first_user = get_github_users(1,0)
    upd_word = 'No profile!!!!'
    first_user[1]['profile'] = upd_word
    assert update_or_insert(first_user)
    # retrieve again from db
    first_user = dict(db.session.query(GithubUser.id, GithubUser))
    assert first_user[1].profile == upd_word