class ISBN13:
    def __init__(self, isbn13: str) -> None:
        if not isbn13 or not isbn13.strip() or len(isbn13) != 13:
            raise ValueError("Invalid ISBN13")

        self.__value = isbn13

    @property
    def value(self) -> str:
        return self.__value

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, ISBN13):
            return False
        return self.value == o.value
