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

    assert created_book == book, "Book should be created"
