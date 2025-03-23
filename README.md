## Books API

This project is an API for handling books built with Django. It provides CRUD operations for the `book` resource, an enrichment service that fetches book info using its ISBN code (either 10 or 13), and a cache layer to avoid too many requests to the 3rd party API.

## Table of contents

- [Setup](#setup)
  - [Pre-requisites](#pre-requisites)
  - [Start the application development environment](#start-the-application-development-environment)
  - [Seed the database](#seed-the-database)
- [Postman collection](#postman-collection)
- [Stack](#stack)
- [Data enrichment](#data-enrichment)
- [Cache](#cache)
- [Tests](#tests)
- [Useful commands](#useful-commands)

## Setup

### Pre-requisites

In order to run this project, you need to have the following tools installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose plugin](https://docs.docker.com/compose/install/#scenario-two-install-the-docker-compose-plugin)
- [Make](https://www.gnu.org/software/make/)

I set up docker-compose for this project, so you don't need to install anything else. Also, I created a Makefile with some useful commands to help you run the project.

### Start the application development environment

To start the application development environment, run the following command:

```bash
make up
```

That will start the Django application, the PostgreSQL database, and the Redis cache. The application will be available at `http://localhost:8000`.

### Seed the database

To seed the database with some books, run the following command:

```bash
make seed-db
```

## Postman collection

I created a Postman collection with all the requests you can make to the API. You can import it by clicking the button below:

<!-- TODO: create postman collection -->

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/1f3b3b3b3b3b3b3b3b3b)

## Stack

This project was built using the following technologies and tools:

- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Make](https://www.gnu.org/software/make/)
- [Pytest](https://docs.pytest.org/en/stable/)
- Github Actions

## Data enrichment

I designed the app to use the [Open Library API](https://openlibrary.org/dev/docs/api/books) to fetch book information using its ISBN code. The API provides a lot of information about books, such as title, author, number of pages, publish date, and more.

Whenever you create or update a book, the app will try to fetch its information from the Open Library API using the ISBN code. If no ISBN code is provided, the app will not try to fetch the information.

## Cache

I used Redis to cache the book information fetched from the Open Library API. The cache layer is used to avoid too many requests to the 3rd party API, which could lead to rate limiting.

Since book information doesn't change frequently, I set the cache expiration time to 1 day.

## Tests

I wrote some unit and integration tests to ensure the app works as expected. You can run the tests by running the following command:

```bash
make test
```

## Useful commands

Besides the commands mentioned above, I created some other useful commands to help you work with the project:

- `make rebuid`: Rebuild the application development environment
- `make migrate`: Run the Django migrations
- `make logs`: Show the application logs
  - `make logs-web`: Show the Django logs
  - `make logs-db`: Show the PostgreSQL logs
  - `make logs-redis`: Show the Redis logs
- `make shell`: Access the Django container shell
- `make format`: Format the code using `black`
- `make up-prod`: Start the application production environment (the Docker image is optimized for production and there's no volume mounted for the code)
- `make rebuild-prod`: Rebuild the application production environment
- `make down`: Stop all services (works for both development and production environments)
- `make clean`: Stop all services and remove all volumes (works for both development and production environments)
