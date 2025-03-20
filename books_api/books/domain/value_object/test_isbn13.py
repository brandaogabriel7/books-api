import pytest

from books.domain.value_object.isbn13 import ISBN13


@pytest.mark.parametrize(
    "isbn13",
    ["123456789029347928837", "12345", "1234567899232323234", None, "", "   "],
)
def test_createisbn13_invalid(isbn13: str):
    with pytest.raises(ValueError):
        ISBN13(isbn13)


@pytest.mark.parametrize(
    "isbn13",
    ["1234567890123", "1234567899232", "1234567899234"],
)
def test_createisbn13_success(isbn13: str):
    isbn = ISBN13(isbn13)
    assert isbn.value == isbn13, f"Value should be '{isbn13}'"
