import pytest

from .book import Book


@pytest.mark.parametrize("id", [None, "", "   "])
def test_createBook_shouldFailWithoutId(id: str):
    with pytest.raises(ValueError) as e:
        Book(id, None)
    assert str(e.value) == "Book id is required", "Should fail without id"


@pytest.mark.parametrize("title", [None, "", "   "])
def test_createBook_shouldFailWithoutTitle(title: str):
    with pytest.raises(ValueError) as e:
        Book("123", title)
    assert str(e.value) == "Book title is required", "Should fail without title"


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


def test_bookISBN10():
    book = Book("123", "Title")
    isbn10 = "1234567890"
    book.changeISBN10(isbn10)
    assert book.isbn10 == isbn10, f"ISBN10 should be updated to '{isbn10}'"

    isbn10 = "0987654321"
    book.changeISBN10(isbn10)
    assert book.isbn10 == isbn10, f"ISBN10 should be updated to '{isbn10}'"


def test_bookISBN13():
    book = Book("123", "Title")
    isbn13 = "1234567890123"
    book.changeISBN13(isbn13)
    assert book.isbn13 == isbn13, f"ISBN13 should be updated to '{isbn13}'"

    isbn13 = "0987654321098"
    book.changeISBN13(isbn13)
    assert book.isbn13 == isbn13, f"ISBN13 should be updated to '{isbn13}'"


@pytest.mark.parametrize(
    "id,title,subtitle,description",
    [
        ["book-id-1", "Title", "Subtitle", "Some book description"],
        [
            "book-id-2",
            "Another title",
            "Another subtitle",
            "Another description",
        ],
        ["book-id-3", "One more title", None, "One more description"],
        ["book-id-4", "Last title", "Last subtitle", None],
        ["book-id-5", "Title", None, None],
    ],
)
def test_createBook_success(
    id: str, title: str, subtitle: str, description: str
):
    book = Book(id, title, subtitle, description)
    assert book.id == id, f"Id should be '{id}'"
    assert book.title == title, f"Title should be '{title}'"
    assert book.subtitle == subtitle, f"Subtitle should be '{subtitle}'"
    assert (
        book.description == description
    ), f"Description should be '{description}'"
