import pytest

from books.application.service.book_service import BookService
from books.infrastructure.open_library.open_library_client import (
    OpenLibraryClient,
)

from books.domain.factory.book_factory import book_factory


@pytest.mark.parametrize(
    "book_data",
    [
        {
            "title": "The Art of Community",
            "isbn10": "0596156715",
        },
        # {
        #     "title": "The Art of Community",
        #     "isbn13": "9780596156718",
        # },
    ],
)
def test_enrich_book_data_with_open_library(
    open_library_client: OpenLibraryClient,
    book_data: dict,
):
    book_service = BookService(OpenLibraryClient())

    book = book_factory(book_data)

    enriched_book = book_service.enrich_book_data(book)

    assert enriched_book.title == "The Art of Community"
    assert (
        enriched_book.subtitle
        == "Building the New Age of Participation (Theory in Practice)"
    )
    assert (
        enriched_book.description
        == "This book guides its readers through the theory and practice of helping a community (with a focus on open source software communities) to achieve its goals. This advice is distilled from Jono Bacon's personal experiences with founding and building the LugRadio podcast / community / live events, the Jokosher audio editor project, and of course his current role as the Ubuntu Community Manager, with plenty of personal anecdotes that provide the rationale for his suggestions."
    )
    assert enriched_book.authors == ["Jono Bacon"]
    assert enriched_book.publishers == ["O'Reilly"]
    assert enriched_book.isbn10.value == "0596156715"
    assert enriched_book.isbn13.value == "9780596156718"
    assert enriched_book.publishDate.value == "2009-08-27"
    assert enriched_book.numberOfPages == 364


def test_not_enrich_book_data_withou_isbn(
    open_library_client: OpenLibraryClient,
):
    book_service = BookService(OpenLibraryClient())

    book = book_factory({"title": "The Art of Community"})

    enriched_book = book_service.enrich_book_data(book)

    assert enriched_book.title == "The Art of Community"
    assert enriched_book.subtitle == None
    assert enriched_book.description == None
    assert enriched_book.authors == []
    assert enriched_book.publishers == []
    assert enriched_book.isbn10 == None
    assert enriched_book.isbn13 == None
    assert enriched_book.publishDate == None
    assert enriched_book.numberOfPages == None
