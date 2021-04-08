# import os
# import tempfile
# import pytest
from app import app, db
from ghdb import GithubUser


def test_favicon():
    '''Teset favicon is there.'''
    with app.test_client() as test_client:
        response = test_client.get('/favicon.ico')
        assert response.status_code == 200

def test_home_page():
    '''Check the title of the index.'''
    with app.test_client() as test_client:
            response = test_client.get('/')
            assert response.status_code == 200
            assert b'Github user list' in response.data

def test_pagination():
    '''Test different pagination combinations'''
    with app.test_client() as test_client:
        response = test_client.get('/?total=1')
        assert response.status_code == 200
        assert 2 == str(response.data).count('</tr>')
        assert b'mojombo' in response.data
        response = test_client.get('/?total=1&page=1')
        assert response.status_code == 200
        assert 2 == str(response.data).count('</tr>')
        assert b'mojombo' in response.data
        response = test_client.get('/?total=1&page=2')
        assert response.status_code == 200
        assert 2 == str(response.data).count('</tr>')
        assert b'defunkt' in response.data
        

def test_all_json_list():
    '''Test that it returns all users in database.'''
    with app.test_client() as test_client:
        response = test_client.post('/all')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert len(response.json) == len(dict(db.session.query(GithubUser.id, GithubUser)))

def test_json_filter():
    '''If `username` is set, it should only return 1 element.'''
    with app.test_client() as test_client:
        response = test_client.post('/all?username=defunkt&pagination=20&order_by=id')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert len(response.json) == 1

def test_pager_json_list():
    '''Paging should work'''
    with app.test_client() as test_client:
        response0 = test_client.post('/all?total=20&page=1')
        assert response0.status_code == 200
        assert response0.content_type == 'application/json'
        assert len(response0.json) == 20
        assert response0.json[0]['id'] == 1

        response1 = test_client.post('/all?total=20&page=1&order_by=user')
        assert response1.status_code == 200
        assert response1.content_type == 'application/json'
        assert len(response1.json) == 20
        assert response1.json[0]['id'] > 1 # The first user is not `mojombo`

        response2 = test_client.post('/all?total=20&page=3&order_by=profile')
        assert response2.status_code == 200
        assert response2.content_type == 'application/json'
        assert len(response2.json) == 20
        assert response1.json[0] != response2.json[0]
        assert response1.json[-1] != response2.json[-1]

        response3 = test_client.post('/all?total=20&page=3&order_by=type')
        assert response3.status_code == 200
        assert response3.content_type == 'application/json'
        assert len(response3.json) == 20
        assert response1.json[0] != response3.json[0]
        assert response1.json[-1] != response3.json[-1]

def test_datatables():
    with app.test_client() as test_client:
        response = test_client.get('/dt')
        assert response.status_code == 200