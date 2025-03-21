import pytest
import uuid

from datetime import date

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
    created_book = BookModel.objects.create(
        id=str(uuid.uuid4()),
        title="Old title",
        subtitle="Old subtitle",
        description="Old description",
        isbn10="1234567890",
        isbn13="1234567890123",
        publish_date=date.fromisoformat("2021-01-01"),
        number_of_pages=100,
    )

    author1 = AuthorModel.objects.create(name="Author 1")
    author2 = AuthorModel.objects.create(name="Author 2")
    created_book.authors.set([author1, author2])

    publisher = PublisherModel.objects.create(name="Publisher")
    created_book.publishers.set([publisher])

    retrieved_book = book_repository.get(created_book.id)
    assert retrieved_book is not None, "Book should be retrieved"
    assert retrieved_book.id == created_book.id, "Book id should match"
    assert retrieved_book.title == created_book.title, "Book title should match"
    assert (
        retrieved_book.subtitle == created_book.subtitle
    ), "Book subtitle should match"
    assert (
        retrieved_book.description == created_book.description
    ), "Book description should match"
    assert retrieved_book.authors == [
        "Author 1",
        "Author 2",
    ], "Authors should match"
    assert retrieved_book.publishers == ["Publisher"], "Publishers should match"
    assert (
        retrieved_book.isbn10.value == created_book.isbn10
    ), "ISBN10 should match"
    assert (
        retrieved_book.isbn13.value == created_book.isbn13
    ), "ISBN13 should match"
    assert (
        retrieved_book.publishDate.value
        == created_book.publish_date.isoformat()
    ), "Publish date should match"
    assert (
        retrieved_book.numberOfPages == created_book.number_of_pages
    ), "Number of pages should match"


@pytest.mark.django_db
def test_get_book_notFound(book_repository_fixture: dict):
    book_repository: DjangoBookRepository = book_repository_fixture[
        "repository"
    ]
    with pytest.raises(BookModel.DoesNotExist):
        book_repository.get(str(uuid.uuid4()))
