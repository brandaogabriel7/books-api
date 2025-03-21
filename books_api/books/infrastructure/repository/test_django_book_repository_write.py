import pytest
import uuid

from datetime import date

from books.domain.entity.book import Book

from books.domain.factory.book_factory import book_factory
from books.infrastructure.repository.django_book_repository import (
    DjangoBookRepository,
)

from books.infrastructure.models.book_model import BookModel
from books.infrastructure.models.author_model import AuthorModel
from books.infrastructure.models.publisher_model import PublisherModel

import books.infrastructure.models.book_model_mapper as book_model_mapper


@pytest.mark.django_db
def test_create_book(book_repository_fixture: dict):
    book_repository: DjangoBookRepository = book_repository_fixture[
        "repository"
    ]
    book = book_factory(
        {
            "title": "New book",
            "subtitle": "New subtitle",
            "description": "This is the book description",
            "authors": ["Author 1", "Author 2", "New Author"],
            "publishers": ["Publisher 1", "Some other publisher"],
            "isbn10": "1234567894",
            "isbn13": "1234567894123",
            "publishDate": "2022-09-02",
            "numberOfPages": 100,
        }
    )
    created_book = book_repository.create(book)

    book_record = BookModel.objects.get(id=created_book.id)
    assert book_record is not None, "Book record should be created"

    assert book_record.title == book.title, "Book title should match"
    assert book_record.subtitle == book.subtitle, "Book subtitle should match"
    assert (
        book_record.description == book.description
    ), "Book description should match"
    assert [
        author.name for author in book_record.authors.all()
    ] == book.authors, "Authors should match"
    assert [
        publisher.name for publisher in book_record.publishers.all()
    ] == book.publishers, "Publishers should match"
    assert book_record.isbn10 == book.isbn10.value, "ISBN10 should match"
    assert book_record.isbn13 == book.isbn13.value, "ISBN13 should match"
    assert book_record.publish_date == date.fromisoformat(
        book.publishDate.value
    ), "Publish date should match"
    assert (
        book_record.number_of_pages == book.numberOfPages
    ), "Number of pages should match"


@pytest.mark.django_db
def test_update_book(book_repository_fixture: dict):
    book_repository: DjangoBookRepository = book_repository_fixture[
        "repository"
    ]

    book_to_update: Book = book_repository_fixture["persisted_books"][0]

    book = book_factory(
        {
            "id": book_to_update.id,
            "title": "New title",
            "subtitle": "New subtitle",
            "description": "New description",
            "authors": ["Author 1", "Author 2"],
            "publishers": ["Publisher"],
            "isbn10": "0987654321",
            "isbn13": "0987654321098",
            "publishDate": "2021-10-01",
            "numberOfPages": 200,
        }
    )
    updated_book = book_repository.update(book_to_update.id, book)

    updated_book_record = BookModel.objects.get(id=updated_book.id)
    assert updated_book_record is not None, "Book record should be updated"

    assert updated_book_record.title == book.title, "Book title should match"
    assert (
        updated_book_record.subtitle == book.subtitle
    ), "Book subtitle should match"
    assert (
        updated_book_record.description == book.description
    ), "Book description should match"
    assert [
        author.name for author in updated_book_record.authors.all()
    ] == book.authors, "Authors should match"
    assert [
        publisher.name for publisher in updated_book_record.publishers.all()
    ] == book.publishers, "Publishers should match"
    assert (
        updated_book_record.isbn10 == book.isbn10.value
    ), "ISBN10 should match"
    assert (
        updated_book_record.isbn13 == book.isbn13.value
    ), "ISBN13 should match"
    assert updated_book_record.publish_date == date.fromisoformat(
        book.publishDate.value
    ), "Publish date should match"
    assert (
        updated_book_record.number_of_pages == book.numberOfPages
    ), "Number of pages should match"


@pytest.mark.django_db
def test_update_book_notFound(book_repository_fixture: dict):
    book_repository: DjangoBookRepository = book_repository_fixture[
        "repository"
    ]
    with pytest.raises(BookModel.DoesNotExist):
        non_existent_book_id = str(uuid.uuid4())
        book_repository.update(
            non_existent_book_id,
            book_factory(
                {
                    "id": non_existent_book_id,
                    "title": "New title",
                    "subtitle": "New subtitle",
                    "description": "New description",
                    "authors": ["Author 1", "Author 2"],
                    "publishers": ["Publisher"],
                    "isbn10": "0987654321",
                    "isbn13": "0987654321098",
                    "publishDate": "2021-10-01",
                    "numberOfPages": 200,
                }
            ),
        )


@pytest.mark.django_db
def test_delete_book(book_repository_fixture: dict):
    book_repository: DjangoBookRepository = book_repository_fixture[
        "repository"
    ]

    book_to_delete: Book = book_repository_fixture["persisted_books"][0]

    book_repository.delete(book_to_delete.id)

    with pytest.raises(BookModel.DoesNotExist):
        BookModel.objects.get(id=book_to_delete.id)


@pytest.mark.django_db
def test_delete_book_notFound(book_repository_fixture: dict):
    book_repository: DjangoBookRepository = book_repository_fixture[
        "repository"
    ]
    with pytest.raises(BookModel.DoesNotExist):
        book_repository.delete(str(uuid.uuid4()))
