# authenticated-flask-api template

## Development Environment

There are some development scripts included in the `bin` directory to aid with
the development process.

* `bin/run-api-server` will start up a docker compose environment
including a postgres container and a Python container to run the Flask app. The Python
container exposes port `5000` for access to the webservice.
* `bin/refresh` will shut down the currently running docker compose environment
and bring it back up from scratch. This is useful for resetting the database
for bringing in changes to sqlalchemy models.

The flask development server uses a watchdog to monitor for any code changes, it
will automatically restart when you write to any of the api files. However if you
make changes/add new SQLAlchemy models you will need to need to perform a refresh
so the database tables are updated appropriately.

## Postgres Setup

When the Postgres server starts up it will run the `database-setup.sql`
script for initial setup. It creates a database called `api` and a super
user `flask` which has permissions on that database. This file can be
edited to provide any additional setup needed for your database.

## Available Routes

* `/auth/register` Allows for creating a new user, takes two form parameters
`email` and `password`
* `/auth/login` Logs a user in and adds session cookies to the HTTP response
* `/auth/logout` Invalidates a users session cookies
* `/auth/protected` Test route which requires user authentication to access

## Authentication

Two different forms of authentication are available for protected routes, either
session cookies which can be retrieved using the `/auth/login` route or basic
authentication through the `Authorization` header.
