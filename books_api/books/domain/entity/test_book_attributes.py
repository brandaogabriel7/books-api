import pytest

from .book import Book

from ..value_object.isbn10 import ISBN10
from ..value_object.isbn13 import ISBN13

from ..value_object.publish_date import PublishDate


@pytest.mark.parametrize("title", ["New title", "Another title"])
def test_changeBookTitle_success(title: str):
    book = Book("123", "Old title")
    book.changeTitle(title)
    assert book.title == title, "Title should be updated"


@pytest.mark.parametrize("title", [None, "", "   "])
def test_changeBookTitle_shouldFailWithoutTitle(title: str):
    book = Book("123", "Old title")
    with pytest.raises(ValueError) as e:
        book.changeTitle(title)
    assert str(e.value) == "Book title is required", "Should fail without title"


@pytest.mark.parametrize("subtitle", ["new subtitle", "other subtitle"])
def test_bookSubtitle(subtitle: str):
    book = Book("123", "Title", "old subtitle")
    book.changeSubtitle(subtitle)
    assert (
        book.subtitle == subtitle
    ), f"Subtitle should be updated to '{subtitle}'"


@pytest.mark.parametrize(
    "description", ["new description", "other description"]
)
def test_bookDescription(description: str):
    book = Book("123", "Title", "Subtitle", "old description")
    book.changeDescription(description)
    assert (
        book.description == description
    ), f"Description should be updated to '{description}'"


def test_numberOfPages():
    book = Book("123", "Title")
    numberOfPages = 100
    book.changeNumberOfPages(numberOfPages)
    assert (
        book.numberOfPages == numberOfPages
    ), f"Number of pages should be updated to '{numberOfPages}'"

    numberOfPages = 200
    book.changeNumberOfPages(numberOfPages)
    assert (
        book.numberOfPages == numberOfPages
    ), f"Number of pages should be updated to '{numberOfPages}'"


@pytest.mark.parametrize("numberOfPages", [-2, 0, -123])
def test_numberOfPages_shouldFailWithInvalidValue(numberOfPages: int):
    book = Book("123", "Title")
    with pytest.raises(ValueError):
        book.changeNumberOfPages(numberOfPages)


def test_bookISBN10():
    book = Book("123", "Title")
    isbn10 = ISBN10("1234567890")
    book.changeISBN10(isbn10)
    assert book.isbn10 == isbn10, f"ISBN10 should be updated to '{isbn10}'"

    isbn10 = ISBN10("0987654321")
    book.changeISBN10(isbn10)
    assert book.isbn10 == isbn10, f"ISBN10 should be updated to '{isbn10}'"


def test_bookISBN13():
    book = Book("123", "Title")
    isbn13 = ISBN13("1234567890123")
    book.changeISBN13(isbn13)
    assert book.isbn13 == isbn13, f"ISBN13 should be updated to '{isbn13}'"

    isbn13 = ISBN13("0987654321098")
    book.changeISBN13(isbn13)
    assert book.isbn13 == isbn13, f"ISBN13 should be updated to '{isbn13}'"


def test_publishDate():
    book = Book("123", "Title")
    publishDate = PublishDate("2021-10-01")
    book.changePublishDate(publishDate)
    assert (
        book.publishDate == publishDate
    ), f"Publish date should be updated to '{publishDate}'"

    publishDate = PublishDate("2021-10-02")
    book.changePublishDate(publishDate)
    assert (
        book.publishDate == publishDate
    ), f"Publish date should be updated to '{publishDate}'"
