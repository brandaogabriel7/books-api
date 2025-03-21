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

    book_record = BookModel.objects.get(id=created_book.id)
    assert book_record is not None, "Book record should be created"

    assert book_record.title == book.title, "Book title should match"
    assert book_record.subtitle == book.subtitle, "Book subtitle should match"
    assert (
        book_record.description == book.description
    ), "Book description should match"
    assert book_record.authors.count() == 2, "Number of authors should match"
    assert (
        book_record.publishers.count() == 2
    ), "Number of publishers should match"
    assert book_record.isbn10 == book.isbn10.value, "ISBN10 should match"
    assert book_record.isbn13 == book.isbn13.value, "ISBN13 should match"
    assert book_record.publish_date == date.fromisoformat(
        book.publishDate.value
    ), "Publish date should match"
    assert (
        book_record.number_of_pages == book.numberOfPages
    ), "Number of pages should match"


@pytest.mark.django_db
def test_get_book(django_book_repository: DjangoBookRepository):
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

    retrieved_book = django_book_repository.get(created_book.id)
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
def test_get_book_notFound(django_book_repository: DjangoBookRepository):
    with pytest.raises(BookModel.DoesNotExist):
        django_book_repository.get(str(uuid.uuid4()))


@pytest.mark.django_db
def test_update_book(django_book_repository: DjangoBookRepository):
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

    book = book_factory(
        {
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
    updated_book = django_book_repository.update(created_book.id, book)

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
def test_update_book_notFound(django_book_repository: DjangoBookRepository):
    with pytest.raises(BookModel.DoesNotExist):
        django_book_repository.update(
            str(uuid.uuid4()),
            book_factory(
                {
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
def test_delete_book(django_book_repository: DjangoBookRepository):
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

    django_book_repository.delete(created_book.id)

    with pytest.raises(BookModel.DoesNotExist):
        BookModel.objects.get(id=created_book.id)


@pytest.mark.django_db
def test_delete_book_notFound(django_book_repository: DjangoBookRepository):
    with pytest.raises(BookModel.DoesNotExist):
        django_book_repository.delete(str(uuid.uuid4()))
