import pytest
import uuid


from books.domain.entity.book import Book

from books.infrastructure.repository.django_book_repository import (
    DjangoBookRepository,
)
from books.infrastructure.models.book_model import BookModel


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


@pytest.mark.django_db
@pytest.mark.parametrize("page_size, filters", [(1, {}), (2, {})])
def test_list_books_pagination(
    book_repository_fixture: dict, page_size: int, filters: dict
):
    book_repository: DjangoBookRepository = book_repository_fixture[
        "repository"
    ]
    persisted_books: list[Book] = book_repository_fixture["persisted_books"]

    pesisted_pages = [
        persisted_books[i * page_size : (i + 1) * page_size]
        for i in range(len(persisted_books) // page_size)
    ]

    pages = [
        book_repository.list(page=i + 1, page_size=page_size, filters=filters)
        for i in range(len(pesisted_pages))
    ]

    for i in range(len(pages)):
        assert pages[i] is not None, f"Page {i+1} should be retrieved"
        for j in range(len(pages[i])):
            assert (
                pages[i][j] is not None
            ), f"Book {j} from page {i+1} should be retrieved"
            assert (
                pages[i][j].id == pesisted_pages[i][j].id
            ), f"Book ID {j} from page {i+1} should match"
            assert (
                pages[i][j].title == pesisted_pages[i][j].title
            ), f"Book title {j} from page {i+1} should match"
            assert (
                pages[i][j].subtitle == pesisted_pages[i][j].subtitle
            ), f"Book subtitle {j} from page {i+1} should match"
            assert (
                pages[i][j].description == pesisted_pages[i][j].description
            ), f"Book description {j} from page {i+1} should match"
            assert (
                pages[i][j].authors == pesisted_pages[i][j].authors
            ), f"Book authors {j} from page {i+1} should match"
            assert (
                pages[i][j].publishers == pesisted_pages[i][j].publishers
            ), f"Book publishers {j} from page {i+1} should match"
            assert (
                pages[i][j].isbn10 == pesisted_pages[i][j].isbn10
            ), f"ISBN10 {j} from page {i+1} should match"
            assert (
                pages[i][j].isbn13 == pesisted_pages[i][j].isbn13
            ), f"ISBN13 {j} from page {i+1} should match"
            assert (
                pages[i][j].publishDate == pesisted_pages[i][j].publishDate
            ), f"Publish date {j} from page {i+1} should match"
            assert (
                pages[i][j].numberOfPages == pesisted_pages[i][j].numberOfPages
            ), f"Number of pages {j} from page {i+1} should match"
