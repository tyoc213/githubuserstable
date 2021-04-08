# log

The first thing I implemented was the command line client that creates the
database and pulls github users to the DB, after I had this command created
with the test cases I proceeded to create the webapp and implemented: an html
table, a json endpoint (that can order and filter by user) and an html that can
render the json with a `datatable` component.

## command line

The purpose of the command is to retrieve and fill the database that the webapp
will use as datasource, to retrieve the data it request certain number of users
as with paging. The code is inside `seed.py`, it uses `click` to parse arguments
and `SQLAlchemy` to access the `sqlite` database. This allows to share the model
from `SQLAlchemy` between the `seed` command and the webapp. It creates the
database, fetches the github users and insert or update them on the database.
## web app

The `Flask` webapp exposes for get: `/`, `/dt` and for post: `/all`.

* The index is an implementation of an html table that can paginate and on each
next or back request the data from the server.
* `dt` exposes a javascript datatable that request the data to `/all` with
`post` and is pretty fast in displaying the data.

As performance features I have cached some of the request including the
parameters and let the images load when needed.

## unit testing

Both the command and the webapp have tests that check the basic things and where
used to guide the development of this two components.

## comments

Flask being new to me is quite interesting that all components are separated
from each other and that you need to organize and connect things all is there to
choose from. The difficult parts where sharing the db between the command and
the webapp, I'm sure there is a better way to handle this. Also I think the
organization is not optimal, but it shows how it grew.

To fill the database the command should be used first some like:

`./seed.py  --total 100 --page 6600`

And so on to feed the table with data then the webapp will have data to show.

# Heroku

https://githubuserstable.herokuapp.com/
https://githubuserstable.herokuapp.com/?total=1000&page=1
https://githubuserstable.herokuapp.com/?total=1000&page=2
POST https://githubuserstable.herokuapp.com/all?total=1000&page=0&order_by=user
POST https://githubuserstable.herokuapp.com/all?total=1000&page=0&order_by=type
https://githubuserstable.herokuapp.com/dt

# github

https://github.com/tyoc213/githubuserstable-flask/tree/main
