import pytest

from books.domain.entity.book import Book


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
