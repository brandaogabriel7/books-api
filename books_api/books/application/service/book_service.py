from books.infrastructure.open_library.open_library_client import (
    OpenLibraryClient,
)

from books.domain.factory.book_factory import book_factory

from books.domain.entity.book import Book


class BookService:
    def __init__(self, open_library_client: OpenLibraryClient) -> None:
        self.__open_library_client = open_library_client

    def enrich_book_data(self, book: Book) -> Book:
        isbn = None
        if book.isbn10 is not None:
            isbn = book.isbn10.value
        elif book.isbn13 is not None:
            isbn = book.isbn13.value

        if isbn is None:
            return book

        book_info = self.__open_library_client.get_book_info(isbn)

        if book_info is None:
            return book

        work_info = self.__open_library_client.get_book_work(
            book_info["workKey"]
        )

        enriched_book_data = {
            "id": book.id,
            "title": book_info["title"],
            "subtitle": book_info["subtitle"],
            "description": (
                work_info["description"] if work_info is not None else None
            ),
            "authors": book_info["authors"],
            "publishers": book_info["publishers"],
            "isbn10": book_info["isbn10"],
            "isbn13": book_info["isbn13"],
            "publishDate": book_info["publishDate"],
            "numberOfPages": book_info["numberOfPages"],
        }

        return book_factory(enriched_book_data)
