from click.testing import CliRunner
from githubusers import get_github_users

def test_first_user():
    first_user = get_github_users(1,0)
    assert first_user == {1:
    {
      "user": "mojombo",
      "id": 1,
      "image_url": "https://avatars.githubusercontent.com/u/1?v=4",
      "profile": "https://github.com/mojombo",
      "typ3": "User"
    }
    }

def test_no_users():
    no_result= get_github_users(10_000, 89_999_999)
    assert no_result == {}
