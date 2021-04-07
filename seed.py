import click
from githubusers import get_github_users
from ghdb import create_all, update_or_insert

@click.command()
@click.option('--total', default=150, show_default=True) # TODO: type=click.IntRange(1, 100)
@click.option('--page', default=0, show_default=True)
def seed(total, page):
    '''Save the users from github user list'''
    create_all()
    user_list = get_github_users(total, page)
    update_or_insert(user_list)    
    click.echo(f'%d users'%(total))
    
    