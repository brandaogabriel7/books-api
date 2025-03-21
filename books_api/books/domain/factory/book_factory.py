import uuid

from books.domain.entity.book import Book
from books.domain.value_object.isbn10 import ISBN10
from books.domain.value_object.isbn13 import ISBN13
from books.domain.value_object.publish_date import PublishDate


def book_factory(data: dict) -> Book:
    book = Book(
        id=data.get("id") if data.get("id") else str(uuid.uuid4()),
        title=data.get("title"),
        subtitle=data.get("subtitle"),
        description=data.get("description"),
    )

    authors = data.get("authors", [])
    for author in authors:
        book.addAuthor(author)

    publishers = data.get("publishers", [])
    for publisher in publishers:
        book.addPublisher(publisher)

    book.changeISBN10(ISBN10(data.get("isbn10")))
    book.changeISBN13(ISBN13(data.get("isbn13")))
    book.changePublishDate(PublishDate(data.get("publishDate")))
    book.changeNumberOfPages(data.get("numberOfPages"))

    return book
