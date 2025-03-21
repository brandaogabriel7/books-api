import pytest
import uuid

from datetime import date

from books.infrastructure.repository.django_book_repository import (
    DjangoBookRepository,
)
from books.infrastructure.models.book_model import BookModel
from books.infrastructure.models.author_model import AuthorModel
from books.infrastructure.models.publisher_model import PublisherModel

import books.infrastructure.models.book_model_mapper as book_model_mapper


@pytest.fixture
def book_repository_fixture(persisted_books_fixture: dict):
    return {
        "repository": DjangoBookRepository(),
        "persisted_books": persisted_books_fixture["persisted_books"],
    }
