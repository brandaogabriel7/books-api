import pytest

from .isbn10 import ISBN10


@pytest.mark.parametrize(
    "isbn10",
    ["123456789029347928837", "12345", "1234567899234", None, "", "   "],
)
def test_createISBN10_invalid(isbn10: str):
    with pytest.raises(ValueError):
        ISBN10(isbn10)


@pytest.mark.parametrize(
    "isbn10",
    ["1234567890", "1234567899", "123456789X"],
)
def test_createISBN10_success(isbn10: str):
    isbn = ISBN10(isbn10)
    assert isbn.value == isbn10, f"Value should be '{isbn10}'"
