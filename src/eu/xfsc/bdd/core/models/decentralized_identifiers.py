"""
Decentralized Identifiers (DIDs) Model
"""
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class Did(str):
    """
    Decentralized Identifiers (DIDs)

    >>> Did('did:method:id')
    'did:method:id'
    >>> Did('not-did:method:id')
    Traceback (most recent call last):
    ...
    ValueError: Not valid DID, see https://www.w3.org/TR/did-core/#did-syntax
    >>> Did('did+method:id')
    Traceback (most recent call last):
    ...
    ValueError: Not valid DID, see https://www.w3.org/TR/did-core/#did-syntax
    """
    def __new__(cls, value: str, *_: Any, **__: Any) -> "Did":
        """
        Extend string type
        """
        cls.validate(value, raise_exception=True)

        return super().__new__(cls, value)

    @staticmethod
    def validate(value: str, raise_exception: bool = False) -> bool:
        """
        when ``raise_exception`` is ``True`` raise exception if not valid or return ``False``
        """
        if value.count(":") >= 2 and value.lower().startswith("did:"):
            return True

        if raise_exception:
            raise ValueError('Not valid DID, see https://www.w3.org/TR/did-core/#did-syntax')

        return False

    @classmethod
    def __get_pydantic_core_schema__(
            cls, _source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))
