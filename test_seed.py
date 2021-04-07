from click.testing import CliRunner
from seed import seed


def test_no_params():
    runner = CliRunner()
    result = runner.invoke(seed)
    assert result.exit_code == 0
    assert result.output == '150 users\n'

def test_total():
    runner = CliRunner()
    result = runner.invoke(seed, ['--total',800])
    assert result.exit_code == 0
    assert result.output == '800 users\n'