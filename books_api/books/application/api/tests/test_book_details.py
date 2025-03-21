from django.urls import reverse
from rest_framework.test import APIClient
import pytest
import uuid

from books.domain.entity.book import Book


@pytest.mark.django_db
def test_get_book(book_api_fixture: dict):
    api_client: APIClient = book_api_fixture["client"]
    persisted_books: list[Book] = book_api_fixture["persisted_books"]

    for book in persisted_books:
        base_url: str = reverse("book-details", kwargs={"book_id": book.id})
        response = api_client.get(base_url)

        assert response.status_code == 200, "Book should be retrieved"
        response_data = response.json()
        assert response_data is not None, "Book should have data"
        assert response_data["id"] == book.id, "Book ID should match"
        assert response_data["title"] == book.title, "Book title should match"
        assert (
            response_data["subtitle"] == book.subtitle
        ), "Book subtitle should match"
        assert (
            response_data["description"] == book.description
        ), "Book description should match"
        assert (
            response_data["authors"] == book.authors
        ), "Book authors should match"
        assert (
            response_data["publishers"] == book.publishers
        ), "Book publishers should match"
        assert (
            response_data["isbn10"] == book.isbn10.value
        ), "Book ISBN10 should match"
        assert (
            response_data["isbn13"] == book.isbn13.value
        ), "Book ISBN13 should match"
        assert (
            response_data["publishDate"] == book.publishDate.value
        ), "Book publishDate should match"
        assert (
            response_data["numberOfPages"] == book.numberOfPages
        ), "Book numberOfPages should match"


@pytest.mark.django_db
def test_update_book(book_api_fixture: dict):
    api_client: APIClient = book_api_fixture["client"]
    persisted_books: list[Book] = book_api_fixture["persisted_books"]

    for book in persisted_books:
        base_url: str = reverse("book-details", kwargs={"book_id": book.id})
        response = api_client.put(
            base_url,
            {
                "id": book.id,
                "title": "Updated Title",
                "subtitle": "Updated Subtitle",
                "description": "Updated Description",
                "authors": ["Updated Author"],
                "publishers": ["Updated Publisher"],
                "isbn10": "1234567890",
                "isbn13": "1234567890123",
                "publishDate": "2022-01-01",
                "numberOfPages": 100,
            },
            format="json",
        )

        assert response.status_code == 200, "Book should be updated"
        response_data = response.json()
        assert response_data is not None, "Book should have data"
        assert response_data["id"] == book.id, "Book ID should match"
        assert (
            response_data["title"] == "Updated Title"
        ), "Book title should match"
        assert (
            response_data["subtitle"] == "Updated Subtitle"
        ), "Book subtitle should match"
        assert (
            response_data["description"] == "Updated Description"
        ), "Book description should match"
        assert response_data["authors"] == [
            "Updated Author"
        ], "Book authors should match"
        assert response_data["publishers"] == [
            "Updated Publisher"
        ], "Book publishers should match"
        assert (
            response_data["isbn10"] == "1234567890"
        ), "Book ISBN10 should match"
        assert (
            response_data["isbn13"] == "1234567890123"
        ), "Book ISBN13 should match"
        assert (
            response_data["publishDate"] == "2022-01-01"
        ), "Book publishDate should match"
        assert (
            response_data["numberOfPages"] == 100
        ), "Book numberOfPages should match"


@pytest.mark.django_db
def test_delete_book(book_api_fixture: dict):
    api_client: APIClient = book_api_fixture["client"]
    persisted_books: list[Book] = book_api_fixture["persisted_books"]

    for book in persisted_books:
        base_url: str = reverse("book-details", kwargs={"book_id": book.id})
        response = api_client.delete(base_url)

        assert response.status_code == 200, "Book should be deleted"
        response_data = response.json()
        assert response_data["id"] == book.id, "Book ID should match"
        assert response_data["title"] == book.title, "Book title should match"
        assert (
            response_data["subtitle"] == book.subtitle
        ), "Book subtitle should match"
        assert (
            response_data["description"] == book.description
        ), "Book description should match"
        assert (
            response_data["authors"] == book.authors
        ), "Book authors should match"
        assert (
            response_data["publishers"] == book.publishers
        ), "Book publishers should match"
        assert (
            response_data["isbn10"] == book.isbn10.value
        ), "Book ISBN10 should match"
        assert (
            response_data["isbn13"] == book.isbn13.value
        ), "Book ISBN13 should match"
        assert (
            response_data["publishDate"] == book.publishDate.value
        ), "Book publishDate should match"
        assert (
            response_data["numberOfPages"] == book.numberOfPages
        ), "Book numberOfPages should match"


@pytest.mark.django_db
def test_get_book_not_found(book_api_fixture: dict):
    api_client: APIClient = book_api_fixture["client"]
    base_url: str = reverse(
        "book-details",
        kwargs={"book_id": "00000000-0000-0000-0000-000000000000"},
    )
    response = api_client.get(base_url)

    assert response.status_code == 404, "Book should not be found"


@pytest.mark.django_db
def test_update_book_not_found(book_api_fixture: dict):
    api_client: APIClient = book_api_fixture["client"]
    base_url: str = reverse(
        "book-details",
        kwargs={"book_id": "00000000-0000-0000-0000-000000000000"},
    )
    response = api_client.put(
        base_url,
        {
            "id": "00000000-0000-0000-0000-000000000000",
            "title": "Updated Title",
            "subtitle": "Updated Subtitle",
            "description": "Updated Description",
            "authors": ["Updated Author"],
            "publishers": ["Updated Publisher"],
            "isbn10": "1234567890",
            "isbn13": "1234567890123",
            "publishDate": "2022-01-01",
            "numberOfPages": 100,
        },
        format="json",
    )

    assert response.status_code == 404, "Book should not be found"


@pytest.mark.django_db
def test_delete_book_not_found(book_api_fixture: dict):
    api_client: APIClient = book_api_fixture["client"]
    base_url: str = reverse(
        "book-details",
        kwargs={"book_id": uuid.uuid4()},
    )
    response = api_client.delete(base_url)

    assert response.status_code == 404, "Book should not be found"
