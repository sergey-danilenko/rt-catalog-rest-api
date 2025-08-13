from dishka import Provider, Scope, provide

from app.core.utils.str_cleaner import StrNormalizer, AddressCleaner


class UtilsProvider(Provider):
    scope = Scope.APP

    @provide
    def get_str_normalizer(self) -> StrNormalizer:
        return StrNormalizer()

    @provide
    def get_address_cleaner(self) -> AddressCleaner:
        return AddressCleaner()
