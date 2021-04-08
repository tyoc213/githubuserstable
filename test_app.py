# import os
# import tempfile
# import pytest
from app import app, db
from ghdb import GithubUser


def test_favicon():
    with app.test_client() as test_client:
        response = test_client.get('/favicon.ico')
        assert response.status_code == 200

def test_home_page():
    '''Check the title of the index'''
    # with app.app_context():
    #     # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
            response = test_client.get('/')
            assert response.status_code == 200
            assert b'Github user list' in response.data

def test_pagination():
    with app.test_client() as test_client:
        response = test_client.get('/?total=1&page=0')
        assert response.status_code == 200
        assert 2 == str(response.data).count('</tr>')
        assert b'mojombo' in response.data
        response = test_client.get('/?total=1&page=1')
        assert response.status_code == 200
        assert 2 == str(response.data).count('</tr>')
        assert b'defunkt' in response.data
        

def test_json_list():
    with app.test_client() as test_client:
        response = test_client.get('/all')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert len(response.json) == len(dict(db.session.query(GithubUser.id, GithubUser)))

def test_datatables():
    with app.test_client() as test_client:
        response = test_client.get('/dt')
        assert response.status_code == 200