from abc import ABC, abstractmethod

from books.domain.entity.book import Book


class BookRepository(ABC):
    @abstractmethod
    def get(self, page: int, page_size: int, filters: object) -> list[Book]:
        pass

    @abstractmethod
    def get(self, book_id: str) -> Book:
        pass

    @abstractmethod
    def create(self, book: Book) -> Book:
        pass

    @abstractmethod
    def update(self, book_id: str, book: Book) -> Book:
        pass

    @abstractmethod
    def delete(self, book_id: str) -> Book:
        pass
