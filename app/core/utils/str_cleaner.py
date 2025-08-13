import re
from string import punctuation, whitespace


class StrNormalizer:
    def __init__(self, symbols: str | None = None) -> None:
        if not symbols:
            symbols = punctuation + whitespace
        self._symbols = symbols
        self._space_pattern = re.compile(r"[,\s]+")

    def clean_spaces(self, value: str | None) -> str | None:
        if not value:
            return value
        return self._space_pattern.sub(" ", value)

    def strip(self, value: str | None) -> str | None:
        if not value:
            return value
        return value.strip(self._symbols)

    def full_clean(self, value: str | None) -> str | None:
        if not value:
            return value
        cleaned = self.clean_spaces(value)
        cleaned = self.strip(cleaned)
        return cleaned


class AddressCleaner(StrNormalizer):
    def __init__(
        self,
        pattern_template: str | None = None,
        exclude_words: list[str] | None = None,
        symbols: str | None = None
    ) -> None:
        super().__init__(symbols=symbols)
        if not pattern_template:
            pattern_template = r"\b({words})\b\.?"

        self._pattern_template = pattern_template

        if not exclude_words:
            exclude_words = [
                "г", "город", "ул", "улица", "д", "дом", "офис", "оф", "кв",
                "квартира",
            ]

        self._exclude_words = exclude_words

        self.pattern = re.compile(self._build_pattern(), flags=re.IGNORECASE)

    def _build_pattern(self) -> str:
        words_pattern = "|".join(map(re.escape, self._exclude_words))
        return self._pattern_template.format(words=words_pattern)

    def full_clean(self, value: str | None) -> str | None:
        if not value:
            return value

        cleaned = self.pattern.sub("", value)
        cleaned = self.clean_spaces(cleaned)
        cleaned = self.strip(cleaned)
        return cleaned or None
