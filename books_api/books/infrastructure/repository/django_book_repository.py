from books.domain.repository.book_repository import BookRepository
from books.domain.entity.book import Book
from books.domain.factory.book_factory import book_factory
from books.infrastructure.models.book_model import BookModel


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

        return book_factory(
            {
                "id": new_book.id,
                "title": new_book.title,
                "subtitle": new_book.subtitle,
                "description": new_book.description,
                "isbn10": new_book.isbn10,
                "isbn13": new_book.isbn13,
                "publishDate": new_book.publish_date,
                "numberOfPages": new_book.number_of_pages,
            }
        )

    def update(self, book_id: str, book: Book) -> Book:
        pass

    def delete(self, book_id: str) -> Book:
        pass
