import pytest

from books.domain.entity.book import Book


@pytest.mark.parametrize("authorName", [["Author name", "Another author name"]])
def test_addBookAuthors(authorName: str):
    book = Book("123", "Title", "Description")
    for name in authorName:
        book.addAuthor(name)
        assert name in book.authors, f"Author '{name}' should be added"


def test_removeAuthors():
    authors = [
        "Author name",
        "Another author name",
        "One more author name",
        "Last author name",
    ]

    book = Book("123", "Title", "Description")

    for name in authors:
        book.addAuthor(name)
        assert name in book.authors, f"Author '{name}' should be added"

    for name in authors:
        book.removeAuthor(name)
        assert name not in book.authors, f"Author '{name}' should be removed"


def test_removeAuthors_shouldNotRemoveUnexistingAuthor():
    authors = [
        "Author name",
        "Another author name",
        "One more author name",
        "Last author name",
    ]

    book = Book("123", "Title", "Description")

    for name in authors:
        book.addAuthor(name)
        assert name in book.authors, f"Author '{name}' should be added"

    book.removeAuthor("Unexisting author")
    assert len(book.authors) == len(authors), "Authors should not be removed"
