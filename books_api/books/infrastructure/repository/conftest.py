import pytest

from books.infrastructure.repository.django_book_repository import (
    DjangoBookRepository,
)
from books.infrastructure.models.book_model import BookModel
from books.infrastructure.models.author_model import AuthorModel
from books.infrastructure.models.publisher_model import PublisherModel


@pytest.fixture
def book_repository_fixture():

    yield {"repository": DjangoBookRepository()}

    BookModel.objects.all().delete()
    AuthorModel.objects.all().delete()
    PublisherModel.objects.all().delete()
