from click.testing import CliRunner
from ghdb import db
from seed import app, seed


def test_no_params():
    '''It should output 150 as default result'''
    with app.app_context():
        db.init_app(app)
        runner = CliRunner()
        result = runner.invoke(seed)
        assert result.exit_code == 0
        assert result.output == '150 users\n'

def test_total():
    '''It should display the number requested elements'''
    with app.app_context():    
        db.init_app(app)
        runner = CliRunner()
        result = runner.invoke(seed, ['--total',800])
        assert result.exit_code == 0
        assert result.output == '800 users\n'