"""
Generic BDD steps for:

- interpreting HTTP return codes like: 201, 404, 500
- match response payload: json, text ...
"""
# pylint: disable=missing-function-docstring

import json
import re
from dataclasses import dataclass

import requests
from behave import then  # pylint: disable=no-name-in-module

from eu.xfsc.bdd.core.steps import alias
from eu.xfsc.bdd.core.utils import asserts


@dataclass
class ContextType(alias.ContextType):
    requests_response: requests.Response


@then("get http 200:Success code")  # type: ignore[misc]
def _200(context: ContextType) -> None:
    status_code = context.requests_response.status_code
    assert status_code == 200, \
        (status_code, context.requests_response.content)


@then("get http 201:Created code")  # type: ignore[misc]
def _201(context: ContextType) -> None:
    status_code = context.requests_response.status_code
    assert status_code == 201, \
        (status_code, context.requests_response.content)


@then("get http 204:No Content code")  # type: ignore[misc]
def _204(context: ContextType) -> None:
    status_code = context.requests_response.status_code
    assert status_code == 204, \
        (status_code, context.requests_response.content)


@then("get http 409:Conflict code")  # type: ignore[misc]
def _409(context: ContextType) -> None:
    status_code = context.requests_response.status_code
    assert status_code == 409, \
        (status_code, context.requests_response.content)


@then("get http 404:Not Found")  # type: ignore[misc]
def _404(context: ContextType) -> None:
    status_code = context.requests_response.status_code
    assert status_code == 404, \
        (status_code, context.requests_response.content)


@then("get http 400:Bad Request")  # type: ignore[misc]
def _400(context: ContextType) -> None:
    status_code = context.requests_response.status_code
    assert status_code == 400, \
        (status_code, context.requests_response.content)


@then("get http 403:401 Unauthorized")  # type: ignore[misc]
def _403(context: ContextType) -> None:
    status_code = context.requests_response.status_code
    assert status_code == 403, \
        (status_code, context.requests_response.content)


@then("get http 401:401 Unauthorized")  # type: ignore[misc]
def _401(context: ContextType) -> None:
    status_code = context.requests_response.status_code
    assert status_code == 401, \
        (status_code, context.requests_response.content)


@then("requests response content match regexp")  # type: ignore[misc]
def regexp_match(context: ContextType) -> None:
    regexp = context.text.strip()
    content = context.requests_response.text
    assert re.search(regexp, content), f"{regexp=}\n, request output does not match {content=}"


@then("requests response content exact text match")  # type: ignore[misc]
def check_test_exact_match(context: ContextType) -> None:
    exact = context.text.strip()
    content = context.requests_response.text
    assert content == exact, f"{exact=}\n, request output does not match {content=}"


@then("requests response content exact json match")  # type: ignore[misc]
def check_json_exact_match(context: ContextType) -> None:
    response = context.requests_response
    if response.content:
        got = context.requests_response.json()
    else:
        got = {}

    if context.text.strip():
        expected = json.loads(context.text)
    else:
        expected = {}

    asserts.equality_for_json_like_data(
        got=got,
        expected=expected,
        aliases=context.aliases
    )
