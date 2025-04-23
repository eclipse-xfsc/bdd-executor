"""
Issuer Details Model
"""
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

from .decentralized_identifiers import Did


class Issuer(str):
    """
    "IssuerDetails" describes the DID or URI of the issuer credential

    examples::

        "issuer": "https://example.edu/issuers/14"
        "issuer": "http://example.org/credentials/23894"
        "issuer": "did:example:ebfeb1f712ebc6f1c276e12ec21",

    >>> Issuer("https://example.edu/issuers/14")
    'https://example.edu/issuers/14'
    >>> Issuer("http://example.org/credentials/23894")
    'http://example.org/credentials/23894'
    >>> Issuer("did:example:abcdef01f712ebc6f1c276e12ec21")
    'did:example:abcdef01f712ebc6f1c276e12ec21'
    >>> Issuer("wrong")
    Traceback (most recent call last):
    ...
    ValueError: Not valid Issuer, see https://www.w3.org/TR/vc-data-model/#issuer
    >>> Issuer.validate("wrong")
    False
    """
    def __new__(cls, value: str, *_: Any, **__: Any) -> "Issuer":
        """
        Extent the string type
        """

        cls.validate(value, raise_exception=True)

        return super().__new__(cls, value)

    @staticmethod
    def validate(value: str, raise_exception: bool = False) -> bool:
        """
        when ``raise_exception`` is ``True`` raise exception if not valid or return ``False``
        """
        if Did.validate(value):
            return True

        if value.lower().startswith('https://'):
            # It is a URI https
            return True

        if value.lower().startswith('http://'):
            # It is a URI https
            return True

        if raise_exception:
            raise ValueError('Not valid Issuer, see https://www.w3.org/TR/vc-data-model/#issuer')

        return False

    @classmethod
    def __get_pydantic_core_schema__(
            cls, _source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))
