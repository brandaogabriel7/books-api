import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from unittest.mock import patch


@pytest.fixture
def book_api_fixture(persisted_books_fixture: dict):
    with patch(
        "books.infrastructure.open_library.open_library_client.OpenLibraryClient.get_book_info"
    ) as mock_get_book_info, patch(
        "books.infrastructure.open_library.open_library_client.OpenLibraryClient.get_book_work"
    ) as mock_get_book_work:
        mock_get_book_info.return_value = None
        mock_get_book_work.return_value = None
        yield {
            "client": APIClient(),
            "persisted_books": persisted_books_fixture["persisted_books"],
        }
