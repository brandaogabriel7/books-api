from books.domain.repository.book_repository import BookRepository
from books.domain.entity.book import Book
from books.domain.factory.book_factory import book_factory

from books.infrastructure.models.book_model import BookModel
from books.infrastructure.models.author_model import AuthorModel
from books.infrastructure.models.publisher_model import PublisherModel


class DjangoBookRepository(BookRepository):
    def get(self, page: int, page_size: int, filters: object) -> list[Book]:
        pass

    def get(self, book_id: str) -> Book:
        pass

    def create(self, book: Book) -> Book:
        new_book = BookModel.objects.create(
            id=book.id,
            title=book.title,
            subtitle=book.subtitle,
            description=book.description,
            isbn10=book.isbn10,
            isbn13=book.isbn13,
            publish_date=book.publishDate,
            number_of_pages=book.numberOfPages,
        )

        author_instances = [
            AuthorModel.objects.get_or_create(name=author)[0]
            for author in book.authors
        ]

        publisher_instances = [
            PublisherModel.objects.get_or_create(name=publisher)[0]
            for publisher in book.publishers
        ]

        new_book.authors.set(author_instances)
        new_book.publishers.set(publisher_instances)

        created_book = book_factory(
            {
                "id": new_book.id,
                "title": new_book.title,
                "subtitle": new_book.subtitle,
                "description": new_book.description,
                "authors": [author.name for author in new_book.authors.all()],
                "publishers": [
                    publisher.name for publisher in new_book.publishers.all()
                ],
                "isbn10": new_book.isbn10,
                "isbn13": new_book.isbn13,
                "publishDate": new_book.publish_date,
                "numberOfPages": new_book.number_of_pages,
            }
        )

        return created_book

    def update(self, book_id: str, book: Book) -> Book:
        pass

    def delete(self, book_id: str) -> Book:
        pass
