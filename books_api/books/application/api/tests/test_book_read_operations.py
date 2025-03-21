from django.urls import reverse
from rest_framework.test import APIClient
import pytest

from books.domain.entity.book import Book


@pytest.mark.django_db
@pytest.mark.parametrize("page_size", [1, 2])
def test_list_books_pagination(book_api_fixture: dict, page_size: int):
    base_url: str = reverse("book-list")
    api_client: APIClient = book_api_fixture["client"]
    persisted_books: list[Book] = book_api_fixture["persisted_books"]

    pesisted_pages = [
        persisted_books[i * page_size : (i + 1) * page_size]
        for i in range(len(persisted_books) // page_size)
    ]

    responses = [
        api_client.get(f"{base_url}?page={i+1}&page_size={page_size}")
        for i in range(len(pesisted_pages))
    ]

    for i in range(len(responses)):
        assert (
            responses[i].status_code == 200
        ), f"Page {i+1} should be retrieved"
        response_data = responses[i].json()
        assert response_data is not None, f"Page {i+1} should have data"
        assert len(response_data) == len(
            pesisted_pages[i]
        ), f"Page {i+1} should have the correct number of books"

        for j in range(len(response_data)):
            assert (
                response_data[j] is not None
            ), f"Book {j} from page {i+1} should be retrieved"
            assert (
                response_data[j]["id"] == pesisted_pages[i][j].id
            ), f"Book ID {j} from page {i+1} should match"
            assert (
                response_data[j]["title"] == pesisted_pages[i][j].title
            ), f"Book title {j} from page {i+1} should match"
            assert (
                response_data[j]["subtitle"] == pesisted_pages[i][j].subtitle
            ), f"Book subtitle {j} from page {i+1} should match"
            assert (
                response_data[j]["description"]
                == pesisted_pages[i][j].description
            ), f"Book description {j} from page {i+1} should match"
            assert (
                response_data[j]["authors"] == pesisted_pages[i][j].authors
            ), f"Book authors {j} from page {i+1} should match"
            assert (
                response_data[j]["publishers"]
                == pesisted_pages[i][j].publishers
            ), f"Book publishers {j} from page {i+1} should match"
            assert (
                response_data[j]["isbn10"] == pesisted_pages[i][j].isbn10.value
            ), f"ISBN10 {j} from page {i+1} should match"
            assert (
                response_data[j]["isbn13"] == pesisted_pages[i][j].isbn13.value
            ), f"ISBN13 {j} from page {i+1} should match"
            assert (
                response_data[j]["publishDate"]
                == pesisted_pages[i][j].publishDate.value
            ), f"Publish date {j} from page {i+1} should match"
            assert (
                response_data[j]["numberOfPages"]
                == pesisted_pages[i][j].numberOfPages
            ), f"Number of pages {j} from page {i+1} should match"


@pytest.mark.django_db
def test_list_books_filter_isbn(book_api_fixture: dict):
    base_url: str = reverse("book-list")
    api_client: APIClient = book_api_fixture["client"]
    persisted_books: list[Book] = book_api_fixture["persisted_books"]

    isbn = persisted_books[0].isbn13.value
    response = api_client.get(f"{base_url}?isbn={isbn}")

    assert response.status_code == 200, "Response should be successful"
    response_data = response.json()
    assert response_data is not None, "Response should have data"
    assert len(response_data) == 1, "Response should have one book"
    assert (
        response_data[0]["isbn13"] == isbn
    ), "Book ISBN13 should match the filter"
    assert (
        response_data[0]["id"] == persisted_books[0].id
    ), "Book ID should match the filter"

    isbn = persisted_books[1].isbn10.value
    response = api_client.get(f"{base_url}?isbn={isbn}")

    assert response.status_code == 200, "Response should be successful"
    response_data = response.json()
    assert response_data is not None, "Response should have data"
    assert len(response_data) == 1, "Response should have one book"
    assert (
        response_data[0]["isbn10"] == isbn
    ), "Book ISBN10 should match the filter"
    assert (
        response_data[0]["id"] == persisted_books[1].id
    ), "Book ID should match the filter"


@pytest.mark.django_db
def test_list_books_filter_isbn_not_found(book_api_fixture: dict):
    base_url: str = reverse("book-list")
    api_client: APIClient = book_api_fixture["client"]
    persisted_books: list[Book] = book_api_fixture["persisted_books"]

    isbn = "0000000000000"
    response = api_client.get(f"{base_url}?isbn={isbn}")

    assert response.status_code == 200, "Response should be successful"
    response_data = response.json()
    assert response_data is not None, "Response should have data"
    assert len(response_data) == 0, "Response should have no books"


@pytest.mark.django_db
def test_list_books_filters(book_api_fixture: dict):
    base_url: str = reverse("book-list")
    api_client: APIClient = book_api_fixture["client"]
    persisted_books: list[Book] = book_api_fixture["persisted_books"]

    title = persisted_books[0].title
    subtitle = persisted_books[0].subtitle
    description = persisted_books[0].description
    authors = persisted_books[0].authors
    publishers = persisted_books[0].publishers
    publish_date = persisted_books[0].publishDate.value
    number_of_pages = persisted_books[0].numberOfPages

    response = api_client.get(
        f"{base_url}?title={title}&subtitle={subtitle}&description={description}&authors={authors[0]}&publishers={publishers[0]}&publishDate={publish_date}&numberOfPages={number_of_pages}"
    )

    assert response.status_code == 200, "Response should be successful"
    response_data = response.json()
    assert response_data is not None, "Response should have data"
    assert len(response_data) == 1, "Response should have one book"
    assert (
        response_data[0]["id"] == persisted_books[0].id
    ), "Book ID should match the filter"
