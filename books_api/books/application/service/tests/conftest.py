import pytest
import uuid

from unittest.mock import Mock


@pytest.fixture
def open_library_client(
    open_library_api_isbn_fixture, open_library_api_work_fixture
) -> Mock:
    mock_api = Mock()
    mock_api.get_book_info.return_value = open_library_api_isbn_fixture
    mock_api.get_book_work.return_value = open_library_api_work_fixture

    return mock_api


@pytest.fixture
def open_library_api_work_fixture():
    return {
        "description": "This book guides its readers through the theory and practice of helping a community (with a focus on open source software communities) to achieve its goals. This advice is distilled from Jono Bacon's personal experiences with founding and building the LugRadio podcast / community / live events, the Jokosher audio editor project, and of course his current role as the Ubuntu Community Manager, with plenty of personal anecdotes that provide the rationale for his suggestions."
    }


@pytest.fixture
def open_library_api_isbn_fixture():
    return {
        "title": "The Art of Community",
        "subtitle": "Building the New Age of Participation (Theory in Practice)",
        "authors": ["Jono Bacon"],
        "publishers": ["O'Reilly"],
        "isbn10": "0596156715",
        "isbn13": "9780596156718",
        "publishDate": "2009-08-27",
        "numberOfPages": 364,
        "workKey": "/works/OL15058799W",
    }
