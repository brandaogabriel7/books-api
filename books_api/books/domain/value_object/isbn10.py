class ISBN10:
    def __init__(self, isbn10: str) -> None:
        if not isbn10 or not isbn10.strip() or len(isbn10) != 10:
            raise ValueError("Invalid ISBN10")

        self.__value = isbn10

    @property
    def value(self) -> str:
        return self.__value
