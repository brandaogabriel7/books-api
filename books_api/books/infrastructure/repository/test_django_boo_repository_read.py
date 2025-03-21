import pytest
import uuid

from datetime import date

from books.domain.entity.book import Book

from books.infrastructure.repository.django_book_repository import (
    DjangoBookRepository,
)
from books.infrastructure.models.book_model import BookModel
from books.infrastructure.models.author_model import AuthorModel
from books.infrastructure.models.publisher_model import PublisherModel


@pytest.mark.django_db
def test_get_book(book_repository_fixture: dict):
    book_repository: DjangoBookRepository = book_repository_fixture[
        "repository"
    ]
    book_to_retrieve: Book = book_repository_fixture["persisted_books"][0]

    retrieved_book = book_repository.get(book_to_retrieve.id)
    assert retrieved_book is not None, "Book should be retrieved"
    assert retrieved_book.id == book_to_retrieve.id, "Book ID should match"
    assert (
        retrieved_book.title == book_to_retrieve.title
    ), "Book title should match"
    assert (
        retrieved_book.subtitle == book_to_retrieve.subtitle
    ), "Book subtitle should match"
    assert (
        retrieved_book.description == book_to_retrieve.description
    ), "Book description should match"
    assert (
        retrieved_book.authors == book_to_retrieve.authors
    ), "Book authors should match"
    assert (
        retrieved_book.publishers == book_to_retrieve.publishers
    ), "Book publishers should match"
    assert (
        retrieved_book.isbn10 == book_to_retrieve.isbn10
    ), "ISBN10 should match"
    assert (
        retrieved_book.isbn13 == book_to_retrieve.isbn13
    ), "ISBN13 should match"
    assert (
        retrieved_book.publishDate == book_to_retrieve.publishDate
    ), "Publish date should match"
    assert (
        retrieved_book.numberOfPages == book_to_retrieve.numberOfPages
    ), "Number of pages should match"


@pytest.mark.django_db
def test_get_book_notFound(book_repository_fixture: dict):
    book_repository: DjangoBookRepository = book_repository_fixture[
        "repository"
    ]
    with pytest.raises(BookModel.DoesNotExist):
        book_repository.get(str(uuid.uuid4()))
