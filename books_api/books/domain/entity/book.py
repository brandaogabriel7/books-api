from ..value_object.isbn10 import ISBN10
from ..value_object.isbn13 import ISBN13


class Book:
    def __init__(
        self, id: str, title: str, subtitle: str = None, description: str = None
    ) -> None:
        self.__id = id
        self.__title = title
        self.__subtitle = subtitle
        self.__description = description
        self.__authors = []
        self.__publishers = []

        self.__validate()

    @property
    def id(self) -> str:
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def subtitle(self) -> str:
        return self.__subtitle

    @property
    def description(self) -> str:
        return self.__description

    @property
    def authors(self) -> list[str]:
        return self.__authors

    @property
    def publishers(self) -> list[str]:
        return self.__publishers

    @property
    def isbn10(self) -> ISBN10:
        return self.__isbn10

    @property
    def isbn13(self) -> ISBN13:
        return self.__isbn13

    @property
    def publishDate(self) -> str:
        return self.__publishDate

    @property
    def numberOfPages(self) -> int:
        return self.__numberOfPages

    def __validate(self) -> None:
        if not self.__id or not self.__id.strip():
            raise ValueError("Book id is required")

        if not self.__title or not self.__title.strip():
            raise ValueError("Book title is required")

    def changeTitle(self, title: str) -> None:
        self.__title = title
        self.__validate()

    def changeSubtitle(self, subtitle: str) -> None:
        self.__subtitle = subtitle

    def changeDescription(self, description: str) -> None:
        self.__description = description

    def addAuthor(self, authorName: str) -> None:
        self.__authors.append(authorName)

    def removeAuthor(self, authorName: str) -> None:
        if authorName in self.__authors:
            self.__authors.remove(authorName)

    def addPublisher(self, publisherName: str) -> None:
        self.__publishers.append(publisherName)

    def removePublisher(self, publisherName: str) -> None:
        if publisherName in self.__publishers:
            self.__publishers.remove(publisherName)

    def changeISBN10(self, isbn10: str) -> None:
        self.__isbn10 = isbn10

    def changeISBN13(self, isbn13: str) -> None:
        self.__isbn13 = isbn13

    def changeNumberOfPages(self, numberOfPages: int) -> None:
        self.__numberOfPages = numberOfPages

    def changePublishDate(self, publishDate: str) -> None:
        self.__publishDate = publishDate
