"""
Trust Framework Pointer Model
"""
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class TrustFrameworkPointer(str):
    """
    DNS pointer record (PTR for short)

    It deviates from the normal usage related to IP
     (https://www.cloudflare.com/learning/dns/dns-records/dns-ptr-record/)
    instead it provides the domain name associated with schema address.

    Example::

        An example dig command to query the PTR record:
            ``dig PTR did-web.test.train.trust-scheme.de``

    """

    def __new__(cls, value: str, *_: Any, **__: Any) -> "TrustFrameworkPointer":
        """
        Extent the string type
        """
        return super().__new__(cls, value)

    @classmethod
    def from_text(cls, text: str) -> set["TrustFrameworkPointer"]:
        """
        Parse multiline test to extract Trust Framework Pointers

        >>> sorted(TrustFrameworkPointer.from_text("point1 point2".replace(" ", "\\n")))
        ['point1', 'point2']
        """
        return set(cls(host) for host in text.splitlines())

    @classmethod
    def __get_pydantic_core_schema__(
            cls, _source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))
