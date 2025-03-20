import pytest
from .author import Author


def test_createAuthor_failWithoutName():
    with pytest.raises(ValueError) as e:
        Author(None)
    assert str(e.value) == "Author name is required", "Should fail without name"


def test_createAuthor_success():
    author = Author("Author name")
    assert author.name == "Author name", "Name should be 'Author name'"
