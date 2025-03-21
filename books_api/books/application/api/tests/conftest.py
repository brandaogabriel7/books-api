import pytest
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.fixture
def book_api_fixture(persisted_books_fixture: dict):
    return {
        "client": APIClient(),
        "persisted_books": persisted_books_fixture["persisted_books"],
    }
