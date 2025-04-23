"""
Collection of matchers, e.g. match response payload: json
"""
from typing import Any, Tuple

import json
import re

import jmespath

JSON_COMMENT = "#"
IN = "in"
IGNORE = "ignore"


def _interpret_comments_in_compared_json_with_jmespath(
        got: dict[str, Any],
        expected: dict[str, Any]) -> Tuple[dict[str, Any], dict[str, Any]]:
    """
    Example::

        {
            "issuanceDate": "2024-02-20T21:30:48.070741921",
            "status": 200,
            "proof": {
            {
                "created": "always random value",
                "jws": "always random value",
                "msg": "static value"
            }
            "#": {
              "in": {
                "": [
                  {
                    "ignore": ["issuanceDate"]
                  }
                ],
                "proof": [
                  {
                    "ignore": ["created", "jws"]
                  }
                ]
              }
            }
    """

    for expression, rules in expected[JSON_COMMENT][IN].items():
        if expression:
            value_expected = jmespath.search(expression, expected)
            value_got = jmespath.search(expression, got)
        else:
            value_expected = expected
            value_got = got

        for rule in rules:
            ignore_fields = rule.get(IGNORE)
            if ignore_fields:
                for ignore_field in ignore_fields:
                    value_expected[ignore_field] = value_got[ignore_field]

    return got, expected


def _interpret_comments_in_compared_json(
        got: dict[str, Any],
        expected: dict[str, Any]) -> Tuple[dict[str, Any], dict[str, Any]]:
    # pylint: disable=line-too-long
    """

    Exemple 1:

    ... code-block:: json

        {
            "message": "Trust list not available in IPFS store.",
            "timestamp": "2024-02-20T21:30:48.070741921",
            "status": 200,
            "#": {
                "match:timestamp:with:regexp": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\.\\d{8,9}$"
            }
        }


    Exemple 2:

    ... code-block:: json

        {
            "issuanceDate": "2024-02-20T20:58:01.927507421Z",
            "issuer": "did:web:essif.iao.fraunhofer.de",
            "proof": {
                "created": "2024-02-20T20:58:01.947482818Z",
                "jws": "eyJhbGe7HxYhS",
                "proofPurpose": "assertionMethod",
                "type": "JsonWebSignature2020",
                "verificationMethod": "did:web:essif.iao.fraunhofer.de#test"
            },
            "#": {
                "in": {
                    "": [
                        {
                            "ignore": ["issuanceDate"]
                        }
                    ],
                    "proof": [
                        {
                            "ignore": ["created", "jws"]
                        }
                    ]
                }
            }
        }
    """
    # pylint: enable=line-too-long
    if JSON_COMMENT not in expected:
        return got, expected

    if IN in expected[JSON_COMMENT]:
        got, expected = _interpret_comments_in_compared_json_with_jmespath(
            got, expected
        )

    for key, pattern in expected[JSON_COMMENT].items():
        try:
            # "match:timestamp:with:regexp"
            match, key_name, with_, regexp = key.split(":")
            if (match, with_, regexp) != ("match", "with", "regexp"):
                raise NotImplementedError(key)

            if re.search(pattern, got[key_name]):
                expected[key_name] = got[key_name]
            else:
                print(f"[PRINT:DEBUG] {pattern=} does not match {got[key_name]=}")
        except ValueError:
            # ValueError: not enough values to unpack (expected 4, got 1)
            pass

    expected.pop(JSON_COMMENT)

    return got, expected


def _sort_json_like_data(data: Any) -> Any:
    if isinstance(data, list):
        return sorted(data)

    if isinstance(data, dict):
        for k, v in sorted(data.items()):
            if isinstance(v, dict):
                data[k] = _sort_json_like_data(v)
                continue

            if isinstance(v, list):
                data[k] = sorted(v)
                continue

            data[k] = v

    return data


def replace_alias_placeholder(data: Any, aliases: dict[str, Any]) -> Any:
    """
    Example::

        {
            "k": "{placeholder}"
        }

    Will be translated into::

        {
            'k': "long.long.placeholder_value"
        }


    """
    if not data:
        return data

    if isinstance(data, list):
        return [replace_alias_placeholder(i, aliases) for i in data]

    if isinstance(data, dict):
        for k, v in sorted(data.items()):
            if isinstance(v, dict):
                data[k] = replace_alias_placeholder(v, aliases)
                continue

            if isinstance(v, list):
                data[k] = replace_alias_placeholder(v, aliases)
                continue

            data[k] = replace_alias_placeholder(v, aliases)

    if data and isinstance(data, str):
        data = data.format(**aliases)

    return data


def equality_for_json_like_data(  # pylint: disable=missing-function-docstring
        got: dict[str, Any],
        expected: dict[str, Any],
        aliases: dict[str, Any]
) -> None:
    _got = _sort_json_like_data(got)
    _expected = replace_alias_placeholder(_sort_json_like_data(expected), aliases)

    _got, _expected = _interpret_comments_in_compared_json(_got, _expected)

    if _got != _expected:
        print(f"[PRINT:WARNING] _got: {json.dumps(_got, indent=4)}")
        print(f"[PRINT:WARNING] _expected: {json.dumps(_expected, indent=4)}")
        raise AssertionError("request output does not match jsons ☝️")
