from datetime import datetime, timezone


class PublishDate:
    def __init__(self, value: str):
        self._validate(value)
        self.__value = value

    def _validate(self, value: str):
        if not value:
            raise ValueError("Publish date cannot be empty")
        try:
            date = datetime.strptime(value, "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
            if date > datetime.now(timezone.utc):
                raise ValueError("Publish date cannot be in the future")
        except ValueError:
            raise ValueError("Invalid publish date format")

    @property
    def value(self) -> str:
        return self.__value
