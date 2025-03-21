import pytest
import uuid

from datetime import date

from books.infrastructure.models.book_model import BookModel
from books.infrastructure.models.author_model import AuthorModel
from books.infrastructure.models.publisher_model import PublisherModel

import books.infrastructure.models.book_model_mapper as book_model_mapper


@pytest.fixture
def persisted_books_fixture():
    authors = AuthorModel.objects.bulk_create(
        [AuthorModel(name="Author 1"), AuthorModel(name="Author 2")]
    )
    publishers = PublisherModel.objects.bulk_create(
        [PublisherModel(name="Publisher 1"), PublisherModel(name="Publisher 2")]
    )

    book1 = BookModel.objects.create(
        id=str(uuid.uuid4()),
        title="Book 1",
        subtitle="Subtitle 1",
        description="Description 1",
        isbn10="1234567890",
        isbn13="1234567890123",
        publish_date=date.fromisoformat("2021-01-01"),
        number_of_pages=100,
    )
    book1.authors.set(authors)
    book1.publishers.set(publishers)

    book2 = BookModel.objects.create(
        id=str(uuid.uuid4()),
        title="Book 2",
        subtitle="Subtitle 2",
        description="Description 2",
        isbn10="1234567891",
        isbn13="1234567891123",
        publish_date=date.fromisoformat("2022-11-10"),
        number_of_pages=100,
    )
    book2.authors.set([authors[0]])
    book2.publishers.set([publishers[0]])

    book3 = BookModel.objects.create(
        id=str(uuid.uuid4()),
        title="Book 3",
        subtitle="Subtitle 3",
        description="Description 3",
        isbn10="1234567892",
        isbn13="1234567892123",
        publish_date=date.fromisoformat("2021-03-01"),
        number_of_pages=100,
    )
    book3.authors.set([authors[1]])
    book3.publishers.set([publishers[1]])

    book4 = BookModel.objects.create(
        id=str(uuid.uuid4()),
        title="Book 4",
        subtitle="Subtitle 4",
        description="Description 4",
        isbn10="1234567893",
        isbn13="1234567893123",
        publish_date=date.fromisoformat("2021-03-01"),
        number_of_pages=100,
    )
    book4.authors.set([authors[1]])
    book4.publishers.set([publishers[1]])

    book5 = BookModel.objects.create(
        id=str(uuid.uuid4()),
        title="Book 5",
        subtitle="Subtitle 5",
        description="Description 5",
        isbn10="1234567894",
        isbn13="1234567894123",
        publish_date=date.fromisoformat("2021-03-01"),
        number_of_pages=100,
    )
    book5.authors.set([authors[1]])
    book5.publishers.set([publishers[1]])

    books = [
        book_model_mapper.book_entity(book)
        for book in [book1, book2, book3, book4, book5]
    ]

    yield {"persisted_books": books}

    BookModel.objects.all().delete()
    AuthorModel.objects.all().delete()
    PublisherModel.objects.all().delete()
