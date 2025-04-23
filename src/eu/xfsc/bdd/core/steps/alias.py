"""
Validate bash commands results
"""
import json
from typing import Any, Callable, Iterable

# pylint: disable=missing-function-docstring
import os
import re
from dataclasses import dataclass

from behave import \
    given  # pylint: disable=no-name-in-module # TODO:minor:fix typing


from eu.xfsc.bdd.core.utils.asserts import replace_alias_placeholder

@dataclass
class ContextType:
    text: str
    aliases: dict[str, Any]
    table: Iterable[dict[str, Any]]
    execute_steps: Callable[[str], Any]


@given("input text as alias {alias} provided")  # type: ignore[misc]
def add_alias_with_text_type(context: ContextType, alias: str) -> None:
    context.aliases[alias] = context.text.strip().format(**context.aliases)


@given("input json as alias {alias} provided")  # type: ignore[misc]
def add_alias_with_text_type(context: ContextType, alias: str) -> None:
    _data = json.loads(context.text)
    replaced = replace_alias_placeholder(_data, context.aliases)
    context.aliases[alias] = replaced


@given("alias {alias} in aliases' context")  # type: ignore[misc]
def assert_exists_alias(context: ContextType, alias: str) -> None:
    assert alias in context.aliases


@given("input Alias|Text|Description provided")  # type: ignore[misc]
def add_alias_with_text_type_as_multiline_table(context: ContextType) -> None:
    """
    Example::

        Feature: Trust List Management
          allow CRUD (create, read, update, delete) operations
          on the trust list at the Trusted Data Store

          Background:
            Given TSPA Keycloak is up
              And TSPA Server is up
              And input Alias|Text|Description provided
              | Alias           | Text                  | Description                              |
              | tf-domain-name  | trust.train1.xfsc.dev | X_NAME:TRAIN_ENV:jenkins-train           |
              | storage         | IPFS                  | X_NAME:TRAIN_ENV:jenkins-train           |
              | Storage         | IPFS                  | X_NAME:TRAIN_ENV:jenkins-train           |

              | tf-domain-name  | trust.train1.xfsc.dev | X_NAME:TRAIN_ENV:dev-use-train           |
              | storage         | local                 | X_NAME:TRAIN_ENV:dev-use-train           |
              | Storage         | Local                 | X_NAME:TRAIN_ENV:dev-use-train           |

              | tf-domain-name  | x.y.z.de              | X_NAME:TRAIN_ENV:dev-with-docker-compose |
              | storage         | local                 | X_NAME:TRAIN_ENV:dev-with-docker-compose |
              | Storage         | Local                 | X_NAME:TRAIN_ENV:dev-with-docker-compose |


    """
    for row in context.table:
        description: str = row['Description']
        match = re.search(r":([A-Z0-9_]+_ENV):([^:]+)", description)
        if match:
            env_name = match.group(1)
            parse_value = match.group(2)
            env_value = os.environ[env_name]
            if env_value != parse_value:
                continue

        context.aliases[row['Alias']] = row['Text'].format(**context.aliases)
