import uuid

from books.domain.entity.book import Book


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

    book.changeISBN10(data.get("isbn10"))
    book.changeISBN13(data.get("isbn13"))
    book.changePublishDate(data.get("publishDate"))
    book.changeNumberOfPages(data.get("numberOfPages"))

    return book
