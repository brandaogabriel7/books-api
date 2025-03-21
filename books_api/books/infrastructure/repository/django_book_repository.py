from datetime import date

from books.domain.repository.book_repository import BookRepository

from books.domain.entity.book import Book

from books.domain.factory.book_factory import book_factory

from books.infrastructure.models.book_model import BookModel
from books.infrastructure.models.author_model import AuthorModel
from books.infrastructure.models.publisher_model import PublisherModel

import books.infrastructure.models.book_model_mapper as book_model_mapper


class DjangoBookRepository(BookRepository):
    def list(self, page: int, page_size: int, filters: object) -> list[Book]:
        pass

    def get(self, book_id: str) -> Book:
        retrieved_book = BookModel.objects.get(id=book_id)

        return book_model_mapper.book_entity(retrieved_book)

    def create(self, book: Book) -> Book:
        new_book = BookModel.objects.create(
            id=book.id,
            title=book.title,
            subtitle=book.subtitle,
            description=book.description,
            isbn10=book.isbn10.value,
            isbn13=book.isbn13.value,
            publish_date=date.fromisoformat(book.publishDate.value),
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

        created_book = book_model_mapper.book_entity(new_book)

        return created_book

    def update(self, book_id: str, book: Book) -> Book:
        existing_book = BookModel.objects.get(id=book_id)

        existing_book.title = book.title
        existing_book.subtitle = book.subtitle
        existing_book.description = book.description
        existing_book.isbn10 = book.isbn10.value
        existing_book.isbn13 = book.isbn13.value
        existing_book.publish_date = date.fromisoformat(book.publishDate.value)
        existing_book.number_of_pages = book.numberOfPages

        author_instances = [
            AuthorModel.objects.get_or_create(name=author)[0]
            for author in book.authors
        ]

        publisher_instances = [
            PublisherModel.objects.get_or_create(name=publisher)[0]
            for publisher in book.publishers
        ]

        existing_book.authors.set(author_instances)
        existing_book.publishers.set(publisher_instances)

        existing_book.save()

        return book_model_mapper.book_entity(existing_book)

    def delete(self, book_id: str) -> Book:
        book = BookModel.objects.get(id=book_id)

        deleted_book = book_model_mapper.book_entity(book)

        book.delete()

        return deleted_book
