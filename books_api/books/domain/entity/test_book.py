import pytest

from ..value_object.author import Author

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
def test_changeBookTitle(title: str):
    book = Book("123", "Old title")
    book.changeTitle(title)
    assert book.title == title, "Title should be updated"


@pytest.mark.parametrize("title", [None, "", "   "])
def test_changeBookTitle_shouldFailWithoutTitle(title: str):
    book = Book("123", "Old title")
    with pytest.raises(ValueError) as e:
        book.changeTitle(title)
    assert str(e.value) == "Book title is required", "Should fail without title"


def test_createBook_success():
    book = Book("123", "Title")
    assert book.id == "123", "Id should be '123'"
    assert book.title == "Title", "Title should be 'Title'"


@pytest.mark.parametrize(
    "description",
    ["this is a book description", "this is another book description"],
)
def test_createBook_sucessWithDescription(description: str):
    book = Book("123", "Title", description)
    assert book.id == "123", "Id should be '123'"
    assert book.title == "Title", "Title should be 'Title'"
    assert (
        book.description == description
    ), "Description should be 'description'"


@pytest.mark.parametrize(
    "description,", ["new description", "other description"]
)
def test_changeBookDescription(description: str):
    book = Book("123", "Title", "old description")
    book.changeDescription(description)
    assert book.description == description, "Description should be updated"


@pytest.mark.parametrize("authorName", [["Author name", "Another author name"]])
def test_addBookAuthors(authorName: str):
    book = Book("123", "Title", "Description")
    for name in authorName:
        book.addAuthor(Author(name))
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
        book.addAuthor(Author(name))
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
        book.addAuthor(Author(name))
        assert name in book.authors, f"Author '{name}' should be added"

    book.removeAuthor("Unexisting author")
    assert len(book.authors) == len(authors), "Authors should not be removed"


@pytest.mark.parametrize("isbn", [None, "", "   "])
def test_changeBookISBN_shouldFailWithoutISBN(isbn: str):
    book = Book("123", "Title")
    with pytest.raises(ValueError) as e:
        book.changeISBN(isbn)
    assert str(e.value) == "Book ISBN is required", "Should fail without ISBN"


def test_changeBookISBN():
    book = Book("123", "Title")
    isbn = "1234567890"
    book.changeISBN(isbn)
    assert book.isbn == isbn, "ISBN should be updated"

    isbn = "0987654321"
    book.changeISBN(isbn)
    assert book.isbn == isbn, "ISBN should be updated"
