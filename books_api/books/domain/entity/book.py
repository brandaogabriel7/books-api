from ..value_object.author import Author


class Book:
    def __init__(self, id: str, title: str, description: str = None) -> None:
        self.__id = id
        self.__title = title
        self.__description = description
        self.__authors = []

        self.__validate()

    @property
    def id(self) -> str:
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def description(self) -> str:
        return self.__description

    @property
    def authors(self) -> list[str]:
        return [author.name for author in self.__authors]

    @property
    def isbn(self) -> str:
        return self.__isbn

    def __validate(self) -> None:
        if not self.__id or not self.__id.strip():
            raise ValueError("Book id is required")

        if not self.__title or not self.__title.strip():
            raise ValueError("Book title is required")

    def changeTitle(self, title: str) -> None:
        self.__title = title
        self.__validate()

    def changeDescription(self, description: str) -> None:
        self.__description = description

    def addAuthor(self, author: Author) -> None:
        self.__authors.append(author)

    def removeAuthor(self, authorName: str) -> None:
        self.__authors = [
            author for author in self.__authors if author.name != authorName
        ]

    def changeISBN(self, isbn: str) -> None:
        if not isbn or not isbn.strip():
            raise ValueError("Book ISBN is required")

        self.__isbn = isbn
