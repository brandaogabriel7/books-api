from books.domain.entity.book import Book
from books.infrastructure.models.book_model import BookModel
from books.domain.factory.book_factory import book_factory


def book_entity(book_model: BookModel) -> Book:
    return book_factory(
        {
            "id": str(book_model.id),
            "title": book_model.title,
            "subtitle": book_model.subtitle,
            "description": book_model.description,
            "authors": [author.name for author in book_model.authors.all()],
            "publishers": [
                publisher.name for publisher in book_model.publishers.all()
            ],
            "isbn10": book_model.isbn10,
            "isbn13": book_model.isbn13,
            "publishDate": (
                book_model.publish_date.isoformat()
                if book_model.publish_date
                else None
            ),
            "numberOfPages": book_model.number_of_pages,
        }
    )
