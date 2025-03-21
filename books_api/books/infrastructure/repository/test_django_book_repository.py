import pytest

from books.domain.entity.book import Book
from books.domain.factory.book_factory import book_factory
from books.infrastructure.repository.django_book_repository import (
    DjangoBookRepository,
)


@pytest.fixture
def django_book_repository():
    return DjangoBookRepository()


@pytest.mark.django_db
def test_create_book(django_book_repository: DjangoBookRepository):
    book = book_factory(
        {
            "title": "New title",
            "subtitle": "New subtitle",
            "description": "New description",
            "authors": ["Author 1", "Author 2"],
            "publishers": ["Publisher 1", "Publisher 2"],
            "isbn10": "1234567890",
            "isbn13": "1234567890123",
            "publishDate": "2021-01-01",
            "numberOfPages": 100,
        }
    )
    created_book = django_book_repository.create(book)

    assert created_book.id == book.id, "Book id should be the same"
    assert created_book.title == book.title, "Book title should be the same"
    assert (
        created_book.subtitle == book.subtitle
    ), "Book subtitle should be the same"
    assert (
        created_book.description == book.description
    ), "Book description should be the same"
    # assert (
    #     created_book.authors == book.authors
    # ), "Book authors should be the same"
    # assert (
    #     created_book.publishers == book.publishers
    # ), "Book publishers should be the same"
    assert created_book.isbn10 == book.isbn10, "Book isbn10 should be the same"
    assert created_book.isbn13 == book.isbn13, "Book isbn13 should be the same"
    assert (
        created_book.publishDate == book.publishDate
    ), "Book publish date should be the same"
    assert (
        created_book.numberOfPages == book.numberOfPages
    ), "Book numbers of pages should be the same"
